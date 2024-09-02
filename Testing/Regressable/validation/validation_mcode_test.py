import os
import sys
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.append(parent_directory)
from validate_codes import validate_codes
class TestMcodeValidate(object):  
    def setup_method(self, method):
        # Define initial attributes
        self.valid = True
        self.invalid = False
        self.mcodes = ['M06', 'M03', 'M04', 'M05', 'M6', 'M3', 'M4', 'M5']
        self.gcodes = ['G0', 'G00', 'G1', 'G01', 'G02', 'G2', 'G03', 'G3']
        self.tools_count = 3
        self.machine_dimensions = {
            'x': [0, 100],
            'y': [0, 100],
            'z': [0, 100]
        }
        self.feed_rate = 70
        self.cur_attributes = [0,0,0,0,0]
        self.middle_points = []
        self.tool_comp = 0
    
    def test_m03outboundSpeed_boundary(self):
        prev_attributes = [100.02, 50.02, 0.0, 0, 100]
        gcode_line = 'M03 S700; this is a comment'
        max_spindle_speed = 200 
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)
        
        assert isValid == self.invalid

    def test_m03inboundSpeed_boundary(self):
        prev_attributes = [100.02, 50.02, 0.0, 0, 100]
        gcode_line = 'M03 S700; this is a comment'
        max_spindle_speed = 700
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.valid
    
    def testm04(self):
        prev_attributes = [100.02, 50.02, 0.0, 1, 100]
        gcode_line = 'M04 S100'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       

        assert isValid == self.valid
        
    def testm05Valid2(self):
        prev_attributes = [100.02, 50.02, 0.0, 1, 100]
        gcode_line = 'M05'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       

        assert isValid == self.valid
        
    def testm05Valid3(self):
        prev_attributes = [100.02, 50.02, 0.0, 1, -100]
        gcode_line = 'M05'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       
        
        assert isValid == self.valid
        
    def testm04Invalid(self):
        prev_attributes = [100.02, 50.02, 0.0, 0, 100]
        gcode_line = 'M04 S400'
        max_spindle_speed = 100       
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       

        assert isValid == self.invalid
        
    def testm06(self):
        prev_attributes = [100.02, 50.02, 0.0, 0, 100]
        gcode_line = 'M06 T3'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       

        assert isValid == self.valid
        
    def testm06Invalid1(self):
        prev_attributes = [100.02, 50.02, 0.0, 0, 100]
        gcode_line = 'M06 T4'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       
        
        assert isValid == self.invalid
        
    def testm06Invalid2(self):
        prev_attributes = [100.02, 50.02, 0.0, 1, 100]
        gcode_line = 'M06 T0'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       

        assert isValid == self.invalid

    def testm06Invalid3(self):
        prev_attributes = [100.02, 50.02, 0.0, 1, 100]
        gcode_line = 'M06 T0; This is a coment'
        max_spindle_speed = 100
        isValid, error_check = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)       

        assert isValid == self.invalid
    
    def test03NegativeSpeed(self):
        prev_attributes = [100.0,0,50.0,1,100]
        gcode_line = 'M03 S-500'
        max_spindle_speed = 100
        response_value, middle_points = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)

        assert response_value == self.invalid

    def test06NegativeTool(self):
        prev_attributes = [100.0,0,50.0,1,100]
        gcode_line = 'M06 T-5'
        max_spindle_speed = 100
        response_value, middle_points = validate_codes(self.mcodes, self.gcodes, prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, max_spindle_speed, self.middle_points, self.tool_comp)

        assert response_value == self.invalid
