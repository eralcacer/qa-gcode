from ast import Break
from pickle import FALSE
from xmlrpc.client import boolean
from flask import Flask, render_template, request, redirect, url_for
from validate_codes import validate_codes
import interpreter as inter
import re

app = Flask(__name__)
gcodes = [ 'G00', 'G0', 'G01', 'G1', 'G02', 'G2', 'G03', 'G3', 'G40', 'G41', 'G42']# 'G04', 'G4', 'G28', 'G29'
mcodes = [ 'M06', 'M03', 'M04', 'M05', 'M6', 'M3', 'M4', 'M5']
current_attributes = [0,0,0,1,0]
tools = []
machine_dimensions = {
    'x': [0, 100],
    'y': [0, 100],
    'z': [0, 100]
}
max_spindle_speed = 100
feed_rate = [100,100]
tools_count = 1
file_path = 'gcode.txt'

with open(file_path, 'w') as file:
    pass
    
@app.route('/', methods=['GET', 'POST'])
def home():
    global machine_dimensions, max_spindle_speed, feed_rate, tools_count, tools

    if request.method == 'POST':
        machine_dimensions['x'][0] = float(request.form['xl']) if request.form['xl'] else 0
        machine_dimensions['x'][1] = float(request.form['xu']) if request.form['xu'] else 100
        machine_dimensions['y'][0] = float(request.form['yl']) if request.form['yl'] else 0
        machine_dimensions['y'][1] = float(request.form['yu']) if request.form['yu'] else 100
        machine_dimensions['z'][0] = float(request.form['zl']) if request.form['zl'] else 0
        machine_dimensions['z'][1] = float(request.form['zu']) if request.form['zu'] else 100
        tools_count = int(request.form['tools']) if request.form['tools'] else 1
        for i in range(1,tools_count+1):
            tools += ['T'+str(i)]
        max_spindle_speed = float(request.form['max_speed']) if request.form['max_speed'] else 100
        feed_rate[0] = float(request.form['feed_rate']) if request.form['feed_rate'] else 100
        feed_rate[1] = feed_rate[0]
        return redirect(url_for('gcode_input'))

    return render_template('home.html')

@app.route('/gcode_input', methods=['GET', 'POST'])
def gcode_input():
    global gcodes, mcodes, machine_dimensions, max_spindle_speed, current_attributes
    error = None
    rows = []

    if request.method == 'POST':
        multiple_line = True
        append_to_file = True
        gcode_line = request.files['gcode_line']
        line_no = 0
        for line in gcode_line:
            multiple_line = True
            line_no += 1
            line_string = ""
            line_string += str(line.decode('utf-8'))
            prev_attributes = current_attributes.copy()
            cur_attributes, middle_points = inter.process(line_string, current_attributes, feed_rate, max_spindle_speed, gcodes, mcodes)
            if cur_attributes == False or middle_points == False:
                error = 'Error at line ' + str(line_no) + ' of the G-Code. '
                print(error,'Syntax')
                break
            isValid, error_validate = validate_codes(mcodes, gcodes, prev_attributes, line_string, tools_count, feed_rate, cur_attributes, machine_dimensions, max_spindle_speed, middle_points, inter.tool_comp)
            if isValid == False:
                error = f'Error at line {str(line_no)} of the G-Code. Instruction {inter.remove_comments(line_string)} {error_validate}'
                print(error)
                break
            
            if cur_attributes == []:
                append_to_file = False
            if middle_points == None:
                multiple_line = False
            if cur_attributes != []:
                current_attributes = cur_attributes
                
            if append_to_file:
                rows.append(f'Line {line_no}: {line_string}')
                if multiple_line:
                    for i in middle_points[:-1]:
                        with open('gcode.txt', 'a') as file:
                            file.write(str(i) + '\n')
                            
                        midAttr = i.copy()
                        midAttr[4] = f'{midAttr[4]}/{max_spindle_speed}'
                        midAttr.append(f'{feed_rate[0]}/{feed_rate[1]}')
                        midAttr.append(inter.tool_comp)
                        rows.append(midAttr) 
                        
                with open('gcode.txt', 'a') as file:
                    file.write(str(current_attributes) + '\n')
                
                attr = current_attributes.copy()
                attr[4] = f'{attr[4]}/{max_spindle_speed}'
                attr.append(f'{feed_rate[0]}/{feed_rate[1]}')
                attr.append(inter.tool_comp)
                rows.append(attr)
                
        columns = ['x_coord', 'y_coord', 'z_coord', 'tool', 'spindle_speed', 'feed_rate', 'tool_comp']
        return render_template('gcode_input.html', columns = columns, error = error, rows = rows, uploaded = True)

    return render_template('gcode_input.html', uploaded = False)

@app.route('/reset_file', methods=['POST'])
def reset_file():
    global current_attributes, machine_dimensions, max_spindle_speed, feed_rate, tools_count, tools

    current_attributes = [0,0,0,1,0]
    tools = []
    machine_dimensions = {
        'x': [0, 100],
        'y': [0, 100],
        'z': [0, 100]
    }
    max_spindle_speed = 100
    feed_rate = [100,100]
    tools_count = 0
    inter.tool_comp = 0
    inter.last_block_ins=None
    inter.block_flag = True
    inter.t_block_flag = True
    
    with open('gcode.txt', 'w') as file:
        pass  

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
