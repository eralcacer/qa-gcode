import math
import G02_G03
import re

tool_comp = 0.0
last_block_ins=None
block_flag = True
t_block_flag = True
def remove_comments(line):
    try:
        ind = line.index(';')
        l = line[:ind]
        return l
    except:
        l = line
    try:
        ind = line.index('(')
        l = line[:ind]
        return l
    except:
        l = line
    return line
import math

def has_semi_colon(line):
    global block_flag
    try:
        ind = line.index(';')
        if ind:
            return True
    except:
        l = line
        return False

def set_last_block_command(code):
    global last_block_ins, block_flag, t_block_flag
    last_block_ins = code
    block_flag = t_block_flag

def get_last_block_command():
    return last_block_ins

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def interpolate_line(start_point, end_point, max_delta_distance):
    total_distance = distance(start_point, end_point)

    # Determine the number of points based on the specified delta_distance
    num_points = int(total_distance / max_delta_distance) + 1

    # Ensure that num_points is at least 2 to include both start and end points
    num_points = max(num_points, 2)

    # Calculate the actual delta_distance based on the adjusted num_points
    delta_distance = total_distance / (num_points - 1)

    x_start, y_start = start_point
    x_end, y_end = end_point

    x_step = (x_end - x_start) / (num_points - 1)
    y_step = (y_end - y_start) / (num_points - 1)

    points = []
    for i in range(num_points):
        points += [ [x_start + i * x_step, y_start + i * y_step] ]
    return points[1:]

def check_gcode(code, ins, current_attributes, feed_rate):
    global tool_comp
    middle_points = []
    set_last_block_command(code)
    if feed_rate[0] == 0:
        feed_rate[0] = feed_rate[1]
    flag = True
    if code.upper() == 'G00' or code.upper() == 'G0':
        feed_rate[0] = feed_rate[1]
        cord = ins[1:]
        for i in cord:
            if 'X' in i.upper():
                x = current_attributes[0]
                current_attributes[0] = float(i[1:])
                if tool_comp != 0 and x != current_attributes[0]:
                    current_attributes[0] += tool_comp
            elif 'Y' in i.upper():
                y = current_attributes[1]
                current_attributes[1] = float(i[1:])
                if tool_comp != 0 and y != current_attributes[1] :
                    current_attributes[1] += tool_comp
            elif 'Z' in i.upper():
                current_attributes[2] = float(i[1:])
            else:
                flag = False

    elif code.upper() == 'G01'or code.upper() == 'G1':
        cord = ins[1:]
        start_point = (current_attributes[0], current_attributes[1])
        for i in cord:
            if 'X' in i.upper():
                x = current_attributes[0]
                current_attributes[0] = float(i[1:])
            elif 'Y' in i.upper():
                y = current_attributes[1]
                current_attributes[1] = float(i[1:])
            elif 'Z' in i.upper():
                current_attributes[2] = float(i[1:])
            elif 'F' in i.upper():
                feed_rate[0] = float(i[1:])
            else:
                flag = False
        current_attributes[0] = round(current_attributes[0]+ tool_comp, 4)
        current_attributes[1] = round(current_attributes[1]+ tool_comp, 4)
        end_point = (current_attributes[0], current_attributes[1])
        max_delta_distance = 0.5 
        points = interpolate_line(start_point, end_point, max_delta_distance)
        for i in points:
            x = round(i[0], 4)
            y = round(i[1], 4)
            middle_points += [[x, y, current_attributes[2], current_attributes[3], current_attributes[4]]]

    elif code.upper() == 'G02' or code.upper() == 'G2' or code.upper() == 'G03' or code.upper() == 'G3':
        cord = ins[1:]
        start_point = (current_attributes[0], current_attributes[1]) 
        end_point = [0,0]
        center_point = None
        radius = None
        angle_increment = 5
        cnt = 0
        i_j_cnt = 0
        for i in cord:
            if 'X' in i.upper():
                end_point[0] = float(i[1:])
                cnt += 1
            elif 'Y' in i.upper():
                end_point[1] = float(i[1:])
                cnt += 1
            elif 'I' in i.upper():
                center_point = [0, 0]
                center_point[0] = float(i[1:])
                i_j_cnt += 1
            elif 'J' in i.upper():
                center_point[1] = float(i[1:])
                i_j_cnt += 1
            elif 'R' in i.upper():
                radius = float(i[1:])
            elif 'F' in i.upper():
                feed_rate[0] = float(i[1:])
            else:
                flag = False
        if cnt !=2 and i_j_cnt != 2:
            flag = False
        clockwise = True
        if code.upper() == 'G03' or code.upper() == 'G3':
            clockwise = False
        current_attributes[0] = round(end_point[0]+ tool_comp, 4)
        current_attributes[1] = round(end_point[1]+ tool_comp, 4)
        end_point = (current_attributes[0], current_attributes[1])
        if center_point is not None:
            center_point = tuple(center_point)
        points = G02_G03.generate_arc_points(start_point, end_point, center_point, clockwise, radius, angle_increment)
        for i in points:
            x = round(i[0], 4)
            y = round(i[1], 4)
            middle_points += [[x, y, current_attributes[2], current_attributes[3], current_attributes[4]]]

    elif code.upper() == 'G40':
        cord = ins[1:]
        if len(cord) != 0:
            flag = False
        else:
            tool_comp = 0.0

    elif code.upper() == 'G41':
        cord = ins[1:]
        for i in cord:
            if 'D' in i.upper():
                tool_comp += -float(i[1:])
            else:
                flag = False

    elif code.upper() == 'G42':
        cord = ins[1:]
        for i in cord:
            if 'D' in i.upper():
                tool_comp += float(i[1:])
            else:
                flag = False
    else:
        flag = False
    if not flag:
        return current_attributes, flag
    return current_attributes, middle_points

def check_mcode(code, ins, current_attributes, max_spindle_speed):
    global last_block_ins
    flag = True
    set_last_block_command(code)
    if code.upper() == 'M03' or code.upper() == 'M3':
        
        con = ins[1:]
        S_value = max_spindle_speed
        for i in con:
            if 'S' in i.upper():
                S_value = float(i[1:])
            else:
                flag = False
        current_attributes[4] = S_value
    elif code.upper() == 'M04' or code.upper() == 'M4':
        
        con = ins[1:]
        S_value = -max_spindle_speed
        for i in con:
            if 'S' in i.upper():
                S_value = -float(i[1:])
            else:
                flag = False
        current_attributes[4] = S_value
    elif code.upper() == 'M05' or code.upper() == 'M5':
        con = ins[1:]
        S_value = 0
        for i in con:
            if 'S' in i.upper():
                S_value = float(i[1:])
            else:
                flag = False
        #current_attributes[4] = S_value
        current_attributes[4] = 0
    elif code.upper() == 'M06' or code.upper() == 'M6':
        con = ins[1:]
        T_value = 1
        for i in con:
            if 'T' in i.upper():
                T_value = int(i[1:])
            else:
                flag = False
        current_attributes[3] = T_value
    else:
        flag = False
    if not flag:
        return flag
    return current_attributes    
        
def process(line, current_attributes, feed_rate, max_spindle_speed, gcodes, mcodes):
    global t_block_flag
    t_block_flag = has_semi_colon(line)
    line = remove_comments(line)
    try:
        ins = re.findall(r'[a-zA-Z]-?[\d.]+|[a-zA-Z]', line)
        if not ins and not last_block_ins:
            return current_attributes, None  # No codes found

        g_or_m_code = None
        for i, code in enumerate(ins):
            if code.upper() in gcodes or code.upper() in mcodes:
                g_or_m_code = code.upper()
                ins.pop(i)
                break
        if g_or_m_code == None and not block_flag:
                g_or_m_code = last_block_ins
        if g_or_m_code:
            ins = [g_or_m_code] + ins
            if g_or_m_code in gcodes:
                current_attributes, middle_points = check_gcode(g_or_m_code, ins, current_attributes, feed_rate)
                return current_attributes, middle_points
            elif g_or_m_code in mcodes:
                current_attributes = check_mcode(g_or_m_code, ins, current_attributes, max_spindle_speed)
                return current_attributes, None
        else:
            return False, None
    except:
        return [], False
