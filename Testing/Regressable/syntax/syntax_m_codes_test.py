import os
import sys
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.append(parent_directory)
from interpreter import process
class TestMcodeValidate(object):  
    def setup_method(self, method):
        # Define initial attributes
        self.valid = True
        self.invalid = False
        self.mcodes = ['M06', 'M03', 'M04', 'M05', 'M6', 'M3', 'M4', 'M5']
        self.gcodes = ['G01', 'G1', 'G00', 'G0', 'G02', 'G2', 'G03', 'G3']
        self.tools_count = 3
        self.machine_dimensions = {
            'x': [0, 100],
            'y': [0, 100],
            'z': [0, 100]
        }
        self.feed_rate = [70, 70]
        self.cur_attributes = [0,0,0,1,100]
    
    def test_valid_m03(self):
        gcode_line = 'M03 S700; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
        
        assert response_value == [0,0,0,1,700]

    def test_valid_m3(self):
        gcode_line = 'M3 S150; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
        
        assert response_value == [0,0,0,1,150]

    def test_invalid_m03(self):
        gcode_line = 'M03 X8'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)

        assert response_value == False

    def test_valid_m04(self):
        gcode_line = 'M04 S60; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
        
        assert response_value == [0,0,0,1,-60]
    
    def test_valid_m4(self):
        gcode_line = 'M4 S60; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
        
        assert response_value == [0,0,0,1,-60]

    def test_invalid_m04(self):
        gcode_line = 'M04 R10'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)

        assert response_value == False

    def test_valid_m05(self):
        gcode_line = 'M05 ; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
        
        assert response_value == [0,0,0,1,0]
    
    def test_valid_m5(self):
        gcode_line = 'M5; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
        
        assert response_value == [0,0,0,1,0]

    def test_invalid_m05(self):
        gcode_line = 'M05 X8'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)

        assert response_value == False

    def test_valid_m06(self):
        gcode_line = 'M06 T8; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
    
        assert response_value == [0,0,0,8,100]

    def test_valid_m6(self):
        gcode_line = 'M6 T4; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
    
        assert response_value == [0,0,0,4,100]

    def test_invalid_m06(self):
        gcode_line = 'M06 Z990; this is a comment'
        response_value, middle_points = process(gcode_line, self.cur_attributes, self.feed_rate, 100, self.gcodes, self.mcodes)
    
        assert response_value == False
