import math
from itertools import islice
from interpreter import tool_comp
center = [None, None]
radius = 0
def validateGcodeFunctions(prev_attributes, cur_attributes, gcode_line, machine_dimensions, feed_rate, middle_points, tool_comp):
    global center, radius
    ins = gcode_line[1:]
    code = gcode_line[0]
    Rflag = False
    if code.upper() in ['G00', 'G0', 'G1', 'G01']:
        start = [prev_attributes[0], prev_attributes[1]]
        end = [cur_attributes[0], cur_attributes[1]]
        valid_points = []
        for i in ins:
            inst = i[0].upper()
            point = float(i[1:]) + tool_comp
            is_valid, error_check = validate_dimesions_feed(machine_dimensions, i[0].upper(), point, feed_rate)

            if is_valid == False:
                return is_valid, error_check
        for points in middle_points:
            x, y = points[:2]
            valid_points += [points]
            valid_x, error_check_x = validate_dimesions_feed(machine_dimensions, 'X', x, feed_rate)        
            valid_y, error_check_y = validate_dimesions_feed(machine_dimensions, 'Y', y, feed_rate)
            if valid_x == False or valid_y == False:
                middle_points[:] = valid_points
                if valid_x == False:
                    return valid_x, f'{error_check_x} in the line points'
                return valid_y, f'{error_check_y} in the line points'      
            is_point_on_line, error_check_p = validate_point_on_line(points[:2], start, end)
            if valid_x and valid_y:
                if is_point_on_line == False:
                    middle_points[:] = valid_points
                    return is_point_on_line, f'{error_check_p} in the line points'
                else:
                    continue
        return True, 'no error'

    if code.upper() in ['G02', 'G2', 'G03', 'G3']:
        x, y = 0, 0
        valid_points = []
        for i in ins:
            point = float(i[1:]) + tool_comp
            inst = i[0].upper()
            if 'X' in i.upper():
                x = point
            if 'Y' in i.upper():
                y = point
            if 'I' in i.upper():
                center[0] = point
            if 'J' in i.upper():
                center[1] = point
            is_valid, error_check = validate_dimesions_feed(machine_dimensions, inst, point, feed_rate)
            if is_valid == False:
                return is_valid, error_check
            if 'R' in i.upper():
                Rflag = True
                radius = float(i[1:])
                tolerance = 1e-2
                if center[0] == None and center[1] == None:
                    prev_center_x, prev_center_y, _, prev_feed_rate, prev_tool_diameter = prev_attributes
                    center[0] = (prev_center_x + x) / 2.0
                    center[1] = (prev_center_y + y) / 2.0
                    distance_to_center = math.sqrt((x - prev_center_x) ** 2 + (y - prev_center_y) ** 2)/2
                    if abs(distance_to_center - radius) > tolerance:
                        return False, 'error radius != len(prev-cur)/2'
                    # return True, 'no error'
                elif radius < 0:
                     return False, 'check radius, cannot be negative'
                else:
                    prev_center_x, prev_center_y, _, prev_feed_rate, prev_tool_diameter = prev_attributes
                    distance_to_center1 = math.sqrt((center[0] - prev_center_x) ** 2 + (center[1] - prev_center_y) ** 2)/2
                    distance_to_center2 = math.sqrt((center[0] - prev_center_x) ** 2 + (center[1] - prev_center_y) ** 2)/2
                    if abs(distance_to_center1 - radius) > tolerance and abs(distance_to_center2 - radius) > tolerance and abs(distance_to_center1 - radius) != abs(distance_to_center2 - radius):
                        return False, 'check radius, prev, cur and center values'

        if Rflag == False:
            if center[0] !=None and center[1] != None:
                prev_x, prev_y, _, prev_feed_rate, prev_tool_diameter = prev_attributes
                radius = math.sqrt((prev_x - center[0]) ** 2 + (prev_y - center[1]) ** 2)
                if center[0] != prev_x + abs(prev_x - x)/2 or center[1] != prev_y + abs(prev_y - y)/2:
                    return False, 'check center != midpoint of prev, cur value as radius not provided'
            else:
                return False, 'check both center and radius are not provided'
        for points in middle_points:
            x, y = points[:2]
            valid_points += [points]
            valid_x, error_check_x = validate_dimesions_feed(machine_dimensions, 'X', x, feed_rate)        
            valid_y, error_check_y = validate_dimesions_feed(machine_dimensions, 'Y', y, feed_rate)
            if valid_x == False or valid_y == False:
                middle_points[:] = valid_points
                if valid_x == False:
                    return valid_x, f'{error_check_x} in the middle points'
                return valid_y, f'{error_check_y} in the middle points'      
            is_point_on_arc, error_check_p = validate_point_on_arc(points[:2], center, radius)
            if valid_x and valid_y:
                if is_point_on_arc == False:
                    middle_points[:] = valid_points
                    return is_point_on_arc, f'{error_check_p} in the middle points'
                else:
                    continue
        return True, 'no error'

    if code.upper() in ['G40', 'G41', 'G42']:
        inst = 'D'
        point = abs(tool_comp)
        is_valid, error_check = validate_dimesions_feed(machine_dimensions, inst, point, feed_rate)
        if is_valid == False: 
            return False, f'Tool compensation is out of range, Invalid D value'
        return True, 'no error'

def validate_point_on_arc(point, center, radius):
    center_x ,center_y = center
    point_x, point_y = point
    tolerance = 1e-2
    r = math.sqrt((point_x - center_x) ** 2 + (point_y - center_y) ** 2)
    if abs(abs(r) - abs(radius)) > tolerance:
        return False, 'point generate wrongly'
    return True, 'no error'

def validate_point_on_line(point, start_point, end_point):
    x, y = point
    x1, y1 = start_point
    x2, y2 = end_point
    # Calculate the distance between the point and the line formed by start_point and end_point
    distance_ps = math.sqrt((y - y1)**2 + (x - x1)**2)
    distance_pe = math.sqrt((y2 - y)**2 + (x2 - x)**2)
    distance_se = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    tolerance = 1e-2
    distance = abs(distance_ps+distance_pe-distance_se)
    if distance > tolerance:
        return False, 'Point is not on the line'
    return True, 'No error'

def validate_dimesions_feed(machine_dimensions, inst, point, feed_rate):
        global center
        if inst == 'X' and (point < machine_dimensions['x'][0] or point > machine_dimensions['x'][1]):
            return False, ' x boundary error' # Check x boundary
        elif inst == 'I' and  (point < machine_dimensions['x'][0] or point > machine_dimensions['x'][1]):
            return False, ' center_x boundary error' # Check center_x boundary
        elif inst == 'Y' and (point < machine_dimensions['y'][0] or point > machine_dimensions['y'][1]):
            return False, ' y boundary error' # Check y boundary
        elif inst == 'J' and  (point < machine_dimensions['y'][0] or point > machine_dimensions['y'][1]):
            return False, ' center_y boundary error' # Check center_y boundary
        elif inst == 'Z' and (point < machine_dimensions['z'][0] or point > machine_dimensions['z'][1]):
            return False, ' z boundary error' # Check z boundary
        elif inst == 'F' and point > feed_rate[1]:
            return False, 'feed rate value cannot be greater than the maximum feed rate allowed' # Check f boundary
        elif inst == 'F' and point == 0:
            return False, 'feed rate value cannot be 0' # Check f is not 0
        elif inst == 'F' and point < 0:
            return False, 'feed value cannot be negative' # Check f is negative
        elif inst == 'D' and (point < machine_dimensions['x'][0] or point > machine_dimensions['x'][1] or point < machine_dimensions['y'][0] or point > machine_dimensions['y'][1]):
            return False, ' Tool compensation error' # Tool compensation out of the boundary
        return True, 'no error'
