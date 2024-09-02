import os
import sys 
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.append(parent_directory)
import pytest
from interpreter import remove_comments, distance, interpolate_line, check_gcode, check_mcode, process, has_semi_colon, set_last_block_command, get_last_block_command

# Test remove_comments function
def test_remove_comments():
    assert remove_comments("G01 X1 Y2 ; This is a comment") == "G01 X1 Y2 "
    assert remove_comments("G01 X1 Y2 (Another comment)") == "G01 X1 Y2 "
    assert remove_comments("G01 X1 Y2") == "G01 X1 Y2"

# Test distance function
def test_distance():
    assert distance((0, 0), (3, 4)) == 5.0
    assert distance((1, 2), (4, 6)) == 5.0

# Test interpolate_line function
def test_interpolate_line():
    start_point = (0, 0)
    end_point = (3, 4)
    max_delta_distance = 1.0
    assert interpolate_line(start_point, end_point, max_delta_distance) == \
        [[0.6, 0.8], [1.2, 1.6], [1.7999999999999998, 2.4000000000000004], [2.4, 3.2], [3.0, 4.0]]

# Test check_gcode function
def test_check_gcode():
    current_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    feed_rate = [0.0, 0.0]
    assert check_gcode('G00', ['X1', 'Y2'], current_attributes, feed_rate) == ([0.0, 2.0, 0.0, 0, 0.0], [])
    # Add more test cases for check_gcode

# Test check_mcode function
def test_check_mcode():
    current_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    max_spindle_speed = 1000.0
    assert check_mcode('M03', ['S500'], current_attributes, max_spindle_speed) == [0.0, 0.0, 0.0, 0, 1000.0]
    # Add more test cases for check_mcode

# Test process function
def test_process():
    current_attributes = [0.0, 0.0, 0.0, 0, 0.0]
    feed_rate = [0.0, 0.0]
    max_spindle_speed = 1000.0
    gcodes = ['G00', 'G01']
    mcodes = ['M03', 'M06']
    assert process("G01 X1 Y2", current_attributes, feed_rate, max_spindle_speed, gcodes, mcodes) == \
    ([1.0, 2.0, 0.0, 0, 0.0], [[0.25, 0.5, 0.0, 0, 0.0], [0.5, 1.0, 0.0, 0, 0.0], [0.75, 1.5, 0.0, 0, 0.0], [1.0, 2.0, 0.0, 0, 0.0]])
    # Add more test cases for process

# Test has semi colon function
def test_valid_has_semi_colon():
    gcode_line = "M04 S500;"
    
    assert has_semi_colon(gcode_line) == True

# Test has semi colon function invalid
def test_invalid_has_semi_colon():
    gcode_line = "G02 X20 Y10"

    assert has_semi_colon(gcode_line) == False

# Test setter and getter functions
def test_setter_getter():
    command_gcode = "G00"
    set_last_block_command(command_gcode)
    
    assert get_last_block_command() == command_gcode
'''
# Run the tests
if __name__ == "__main__":
    pytest.main()
'''