import os
import sys 
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.append(parent_directory)
import pytest
from validate_codes import validate_codes
from validateGcode_Function import validateGcodeFunctions
from validateMcode_Function import validateMcodeFunctions
# Mock classes or functions for dependencies (if any)

# Test validate_codes function
def test_validate_codes_for_Mcode():
    mcodes = ['M03', 'M06']
    gcodes = ['G00', 'G01']
    prev_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    gcode_line = "M03 S500"
    tools_count = 1
    feed_rate = [0.0, 0.0]
    cur_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    machine_dimensions = {
    'x': [0, 100],
    'y': [0, 100],
    'z': [0, 100]
}
    max_spindle_speed = 1000.0
    middle_points = []
    tool_comp = 0.0
    value, error = validate_codes(mcodes, gcodes, prev_attributes, gcode_line, tools_count, feed_rate, cur_attributes,
                          machine_dimensions, max_spindle_speed, middle_points, tool_comp)
    assert value == True

def test_validate_codes_for_Gcode():
    mcodes = ['M03', 'M06']
    gcodes = ['G00', 'G01']
    prev_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    gcode_line = "G01 X10 Y20 F100"
    tools_count = 1
    feed_rate = [0.0, 0.0]
    cur_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    machine_dimensions = {
    'x': [0, 100],
    'y': [0, 100],
    'z': [0, 100]
}
    max_spindle_speed = 1000.0
    middle_points = []
    tool_comp = 0.0
    value, error = validate_codes(mcodes, gcodes, prev_attributes, gcode_line, tools_count, feed_rate, cur_attributes,
                          machine_dimensions, max_spindle_speed, middle_points, tool_comp)
    assert value == False

# test_validate_gcode_functions.py
import pytest
from validateGcode_Function import validateGcodeFunctions, validate_point_on_line, validate_point_on_arc, validate_dimesions_feed

# Mock classes or functions for dependencies (if any)

# Test validate_dimesions_feed function
def test_validate_dimesions_feed_for_X():
    machine_dimensions = {'x': [0, 100], 'y': [0, 100], 'z': [0, 50]}
    inst = 'X'
    point = 120
    feed_rate = [0, 100]
    assert validate_dimesions_feed(machine_dimensions, inst, point, feed_rate) == (False, ' x boundary error')

# Add more test cases for validate_dimesions_feed with different values of inst and point

# Test validate_point_on_line function
def test_validate_point_on_line():
    point = [10, 20]
    start_point = [0, 0]
    end_point = [30, 40]
    assert validate_point_on_line(point, start_point, end_point) == (False, 'Point is not on the line')

# Add more test cases for validate_point_on_line with different values of point, start_point, and end_point

# Test validate_point_on_arc function
def test_validate_point_on_arc():
    point = [15, 25]
    center = [10, 20]
    radius = 5
    assert validate_point_on_arc(point, center, radius) == (False, 'point generate wrongly')

# Test validateGcodeFunctions function
def test_validateGcodeFunctions_for_G01():
    prev_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    cur_attributes = [10.0, 20.0, 0.0, 0, 0.0]
    gcode_line = ['G01', 'X30', 'Y40', 'F100']
    machine_dimensions = {'x': [0, 100], 'y': [0, 100], 'z': [0, 50]}
    feed_rate = [0, 100]
    middle_points = []
    tool_comp = 0.0
    assert validateGcodeFunctions(prev_attributes, cur_attributes, gcode_line, machine_dimensions, feed_rate, middle_points, tool_comp) == (True, 'no error')

# Test validateMcodeFunctions function
def test_validateMcodeFunctions_for_M03_with_valid_speed():
    prev_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    ins = ['M03', 'S1000']
    tools_count = 10
    max_spindle_speed = 2000
    assert validateMcodeFunctions(prev_attributes, ins, tools_count, max_spindle_speed) == (True, 'no error')

# Test validateMcodeFunctions function for invalid speed
def test_validateMcodeFunctions_for_M03_with_invalid_speed():
    prev_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    ins = ['M03', 'S2500']
    tools_count = 10
    max_spindle_speed = 2000
    assert validateMcodeFunctions(prev_attributes, ins, tools_count, max_spindle_speed) == (False, ' error Spindle speed')

# Test validateMcodeFunctions function for valid tool number
def test_validateMcodeFunctions_for_M06_with_valid_tool():
    prev_attributes = [0.0, 0.0, 0.0, 1, 0.0]
    ins = ['M06', 'T2']
    tools_count = 10
    max_spindle_speed = 2000
    assert validateMcodeFunctions(prev_attributes, ins, tools_count, max_spindle_speed) == (True, 'no error')


# Test validateMcodeFunctions function for invalid tool number
def test_validateMcodeFunctions_for_M06_with_invalid_tool():
    prev_attributes = [0.0, 0.0, 0.0, 1, 0.0]
    ins = ['M06', 'T12']
    tools_count = 10
    max_spindle_speed = 2000
    assert validateMcodeFunctions(prev_attributes, ins, tools_count, max_spindle_speed) == (False, ' error Tool')
'''
if __name__ == "__main__":
    pytest.main()
'''