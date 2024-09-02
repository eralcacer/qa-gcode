import argparse
import interpreter as inter
from validate_codes import validate_codes
parser = argparse.ArgumentParser(description='gcode_interpreter')
parser.add_argument('input_file', type=str, help='enter the input file name')
#parser.add_argument('output_file', type=int, help='enter the output file name')
args = parser.parse_args()
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
feed_rate = [100, 100]
tools_count = 1
file_path = 'gcode.txt'
def print_pretty(cur_attributes):
    global feed_rate
    header_format = "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<15}\t{:<15}\t{:<10}"
    row_format = "{:<10.2f}\t{:<10.2f}\t{:<10.2f}\t{:<10}\t{:<15}\t{:<15}\t{:<10}"

    print(header_format.format("x_coord", "y_coord", "z_coord", "tool", "spindle_speed", "feed_rate", "tool_comp"))
    print(row_format.format(cur_attributes[0], cur_attributes[1], cur_attributes[2], int(cur_attributes[3]),
                             str(int(cur_attributes[4]))+'/'+str(max_spindle_speed),
                             str(feed_rate[0])+'/'+str(feed_rate[1]), inter.tool_comp))

with open(file_path, 'w') as file:
    pass
Machine_Dimension_X = float(input("enter the x dimension lower limit: ") or machine_dimensions['x'][0] )
Machine_Dimension_Xu = float(input("enter the x dimension upper limit: ") or machine_dimensions['x'][1] )
Machine_Dimension_Y = float(input("enter the y dimension lower limit: ") or machine_dimensions['y'][0] )
Machine_Dimension_Yu = float(input("enter the y dimension upper limit: ") or machine_dimensions['y'][1] )
Machine_Dimension_Z = float(input("enter the z dimension lower limit: ") or machine_dimensions['z'][0] )
Machine_Dimension_Zu = float(input("enter the z dimension upper limit: ") or machine_dimensions['z'][1] )

tools_count = float(input("enter the number of tools: ") or tools_count)
Max_Machine_Speed = float(input("enter Max machine Speed: ") or max_spindle_speed)
Max_feed_rate = float(input("enter Max feed rate: ") or feed_rate[1])

machine_dimensions['x'] = [Machine_Dimension_X, Machine_Dimension_Xu]
machine_dimensions['y'] = [Machine_Dimension_Y, Machine_Dimension_Yu]
machine_dimensions['z'] = [Machine_Dimension_Z, Machine_Dimension_Zu]
max_spindle_speed = Max_Machine_Speed
feed_rate[0],feed_rate[1] = Max_feed_rate, Max_feed_rate

error = None
with open(args.input_file, 'r') as gcode_line:
    print("Max machine speed", Max_Machine_Speed, " feed rate", Max_feed_rate, " dimesions", machine_dimensions)
    with open(file_path, 'w') as file:
        line_no = 0
        for line in gcode_line:
            append_to_file = True
            multiple_line = True
            middle_points = []
            line_no += 1
            print('-'*20+'line_no: '+str(line_no)+ '\t' + line.split(';')[0].strip()+'-'*20)
            line_string = ""
            line_string += str(line)
            prev_attributes = current_attributes.copy()
            cur_attributes, middle_points = inter.process(line_string, current_attributes, feed_rate, max_spindle_speed, gcodes, mcodes)
            if cur_attributes == False or middle_points == False: 
                error = 'Error at line ' + str(line_no) + ' of the G-Code.'
                print(error,'Syntax')
                break
            if len(line_string)==0 or (';' in line_string and line_string.index(';') == 0):
                print('empty line')
                continue
            isValid, error_validate = validate_codes(mcodes, gcodes, prev_attributes, line_string, tools_count, feed_rate, cur_attributes, machine_dimensions, max_spindle_speed, middle_points, inter.tool_comp)
            if isValid == False:
                if middle_points != None and len(middle_points)!=0 and 'middle'in error_validate:
                    for i in middle_points:
                        print_pretty(i)
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
                if multiple_line:
                    for i in middle_points[:-1]:
                        with open('gcode.txt', 'a') as file:
                            print_pretty(i)
                            file.write(str(i) + '\n')
                with open('gcode.txt', 'a') as file:
                    print_pretty(current_attributes)
                    file.write(str(current_attributes) + '\n')
        with open('gcode.txt', 'r') as file:
            updated_content = file.read()

    with open('gcode.txt', 'r') as file:
        existing_content = file.read()
#if error is None:
#    with open('gcode.txt', 'r') as file:
#        for line in file:
#            print(line)
