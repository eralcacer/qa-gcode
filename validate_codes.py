import re
import interpreter as inter
from validateMcode_Function import validateMcodeFunctions
from validateGcode_Function import validateGcodeFunctions

def validate_codes(mcodes, gcodes, prev_attributes, gcode_line, tools_count, feed_rate, cur_attributes, machine_dimensions, max_spindle_speed, middle_points, tool_comp):
    gcode_line = inter.remove_comments(gcode_line)
    ins = re.findall(r'[a-zA-Z]-?[\d.]+|[a-zA-Z]', gcode_line)
    g_or_m_code = None
    for i, code in enumerate(ins):
        if code.upper() in gcodes or code.upper() in mcodes:
            g_or_m_code = code.upper()
            ins.pop(i)
            break
    # ins = [g_or_m_code] + ins
    if g_or_m_code == None:
        g_or_m_code = inter.get_last_block_command()
        ins = [g_or_m_code] + ins
    else:
        ins = [g_or_m_code] + ins
    if g_or_m_code in mcodes:
        return validateMcodeFunctions(prev_attributes, ins, tools_count, max_spindle_speed)  
    elif g_or_m_code in gcodes:
        # Call gcode validation function for boundaries
        return validateGcodeFunctions(prev_attributes, cur_attributes, ins, machine_dimensions, feed_rate, middle_points, tool_comp)
