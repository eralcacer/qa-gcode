import math
import os
import sys
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.append(parent_directory)
from interpreter import process
class TestGCodeInterpreter:
    def setup_method(self, method):
        # Define initial attributes
        self.current_attributes = [0, 0, 0, 0, 0]
        self.feed_rate = [200, 200]
        self.max_spindle_speed = 200
        self.gcodes = ['G02', 'G2', 'G03', 'G3', 'G00', 'G0', 'G01', 'G1', 'G41', 'G42']
    
    # Test case: G00 valid
    def test_valid_g00(self):
        gcode_line = "G00 X1 Y2"
        result = [1.0, 2.0, 0.0, 0.0, 0.0]
        new_attributes, arc_points = process(gcode_line,self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert new_attributes == result

    # Test case: G0 valid
    def test_valid_g0(self):
        gcode_line = "G0 X40 Z50"
        result = [40.0, 0, 50.0, 0, 0]
        new_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert new_attributes == result

    # Test case: G01 valid
    def test_valid_g01(self):
        gcode_line = "G01 X400 Z20"
        result = [400, 0, 20, 0, 0]
        new_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert new_attributes == result

    # Test case: G1 valid
    def test_valid_g1(self):
        gcode_line = "G1 Y400 Z20"
        result = [0, 400.0, 20, 0, 0]
        new_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert new_attributes == result

    # Test case: G01 invalid
    def test_invalid_g01(self):
        gcode_line = "G01 T4"
        new_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert new_attributes == [0, 0, 0, 0, 0]

    # Test case: G02 clockwise arc
    def test_valid_g02_command(self):
        gcode_line = "G02 X10 Y20 I5 J5"
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert len(arc_points) == 41 # Verify that there are 41 arc points

    # Test case: Invalid G02 command with missing parameters
    def test_missing_parameters_g02_command(self):
        gcode_line = "G02 X10 Y20 Z5"  # Missing parameters and G-Code not given properly
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert arc_points is False  # Verify that arc_points is False (indicating failure to process the command)

    # Test case: Invalid G02 command with non-valid circle parameters
    def test_invalid_circle_parameters_g02_command(self):
        gcode_line = "G02 X10 Y20 I200 J2000"  # Invalid I and J parameters for forming a circle
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert arc_points == [] # Verify that arc_points is False (indicating failure to form a valid circle)
    
    # Test case: G03 counterclockwise arc
    def test_valid_g03_command(self):
        gcode_line = "G03 X30 Y20 I0 J10"
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert len(arc_points) == 21 # Verify that there are 21 arc points
    
    # Test case: Invalid G03 command with missing parameters
    def test_missing_parameters_g03_command(self):
        gcode_line = "G03 X30 Y20 Z5"  # Missing parameters and G-Code not given properly
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert arc_points is False # Verify that arc_points is False (indicating failure to process the command)
    
    # Test case: Invalid G03 command with non-valid circle parameters
    def test_invalid_circle_parameters_g03_command(self):
        gcode_line = "G03 X30 Y20 I200 J2000"  # Invalid I and J parameters for forming a circle
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert arc_points == [] # Verify that arc_points is False (indicating failure to form a valid circle)

    # Test case: Invalid G41 command with non-valid parameters
    def test_invalid_parameters_g41_command(self):
        gcode_line = "G41 X30"  # Invalid I and J parameters for forming a circle
        updated_attributes, arc_points = process(gcode_line, self.current_attributes, self.feed_rate, self.max_spindle_speed, self.gcodes, [])
        assert arc_points == False # Verify that arc_points is False (indicating failure to form a valid circle)
