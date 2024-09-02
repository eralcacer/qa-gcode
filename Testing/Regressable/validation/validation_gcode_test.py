import os
import sys
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.append(parent_directory)
from validate_codes import validate_codes
class TestGcodeValidate(object):
    def setup_method(self, method):
        # Define initial attributes
        self.valid = True
        self.invalid = False
        self.mcodes = ['M06', 'M03', 'M04', 'M05', 'M6', 'M3', 'M4', 'M5']
        self.gcodes = ['G0', 'G00', 'G1', 'G01', 'G02', 'G2', 'G03', 'G3', 'G41', 'G42']
        self.tools_count = 0
        self.machine_dimensions = {
            'x': [0, 100],
            'y': [0, 100],
            'z': [0, 100]
        }
        self.feed_rate = [200, 200]
        self.max_spindle_speed = 100
        self.cur_attributes = [0, 0, 0, 0, 0]
        self.prev_attributes = [0, 0, 0, 0, 0]
        self.middle_points = []
        self.tool_comp = 0

    ## G00 boundary test cases
    def test_g00_negative_x_boundary(self):
        gcode_line = 'G00 X-10 Y11 Z10'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g00_exceeds_x_boundary(self):
        gcode_line = 'G00 X110 Y11 Z10'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid


    def test_g00_negative_y_boundary(self):
        gcode_line = 'G00 X10 Y-11 Z10'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g00_exceeds_y_boundary(self):
        gcode_line = 'G00 X10 Y110 Z10'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    def test_g00_negative_z_boundary(self):
        gcode_line = 'G00 X10 Y11 Z-10'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g00_exceeds_z_boundary(self):
        gcode_line = 'G00 X10 Y11 Z110'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    ## G01 boundary test cases
    def test_g01_negative_x_boundary(self):
        gcode_line = 'G01 X-10 Y11 Z10 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_exceeds_x_boundary(self):
        gcode_line = 'G01 X110 Y11 Z10 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_negative_y_boundary(self):
        gcode_line = 'G01 X10 Y-11 Z10 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_exceeds_y_boundary(self):
        gcode_line = 'G01 X10 Y110 Z10 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_negative_z_boundary(self):
        gcode_line = 'G01 X10 Y11 Z-10 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_exceeds_z_boundary(self):
        gcode_line = 'G01 X10 Y11 Z110 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_point_not_on_line(self):
        gcode_line = 'G01 X10 Y11 Z11 F100'
        self.middle_points = [[15, 20, 0, 1, 100.0], [0.7861, 0.1698, 0, 1, 100.0],[0.7861, 0.1698, 0, 1, 100.0],[0.7861, 0.1698, 0, 1, 100.0]]
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_point_not_on_line_y_boundary(self):
        gcode_line = 'G01 X10 Y11 Z11 F100'
        self.middle_points = [[15, -20, 0, 1, 100.0], [0.7861, 0.1698, 0, 1, 100.0],[0.7861, 0.1698, 0, 1, 100.0],[0.7861, 0.1698, 0, 1, 100.0]]
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_point_not_on_line_x_boundary(self):
            gcode_line = 'G01 X10 Y11 Z11 F100'
            self.middle_points = [[-15, 20, 0, 1, 100.0], [0.7861, 0.1698, 0, 1, 100.0],[0.7861, 0.1698, 0, 1, 100.0],[0.7861, 0.1698, 0, 1, 100.0]]
            isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

            assert isValid == self.invalid

    def test_g01_negative_feed_rate(self):
        gcode_line = 'G01 X10 Y11 Z10 F-100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g01_exceeds_feed_rate(self):
        gcode_line = 'G01 X10 Y11 Z10 F210'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    ## G02 boundary test cases
    def test_g02_negative_x_boundary(self):
        gcode_line = 'G02 X-10 Y20 R10 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g02_exceeds_x_boundary(self):
        gcode_line = 'G02 X200 Y50 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g02_negative_y_boundary(self):
        gcode_line = 'G02 X10 Y-50 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g02_exceeds_y_boundary(self):
        gcode_line = 'G02 X10 Y200 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g02_no_center_calculate(self):
            gcode_line = 'G02 X10 Y20 R15'
            isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

            assert isValid == self.invalid

    def test_g02_center_not_midpoint(self):
            gcode_line = 'G02 X10 Y20 I10 J20'
            isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

            assert isValid == self.invalid

    def test_g02_point_not_on_arc(self):
        gcode_line = 'G02 X8 Y8 R5 F100'
        self.middle_points = [[0.4645, 0.4645, 0, 1, 100.0], [0.7861, 0.1698, 0, 1, 100.0], [1.1321, -0.0958, 0, 1, 100.0], [1.5, -0.3301, 0, 1, 100.0], [1.8869, -0.5315, 0, 1, 100.0], [2.2899, -0.6985, 0, 1, 100.0], [2.7059, -0.8296, 0, 1, 100.0], [3.1318, -0.924, 0, 1, 100.0], [3.5642, -0.981, 0, 1, 100.0], [4.0, -1.0, 0, 1, 100.0], [4.4358, -0.981, 0, 1, 100.0], [4.8682, -0.924, 0, 1, 100.0], [5.2941, -0.8296, 0, 1, 100.0], [5.7101, -0.6985, 0, 1, 100.0], [6.1131, -0.5315, 0, 1, 100.0], [6.5, -0.3301, 0, 1, 100.0], [6.8679, -0.0958, 0, 1, 100.0], [7.2139, 0.1698, 0, 1, 100.0], [7.5355, 0.4645, 0, 1, 100.0], [7.8302, 0.7861, 0, 1, 100.0], [8.0958, 1.1321, 0, 1, 100.0], [8.3301, 1.5, 0, 1, 100.0], [8.5315, 1.8869, 0, 1, 100.0], [8.6985, 2.2899, 0, 1, 100.0], [8.8296, 2.7059, 0, 1, 100.0], [8.924, 3.1318, 0, 1, 100.0], [8.981, 3.5642, 0, 1, 100.0], [9.0, 4.0, 0, 1, 100.0], [8.981, 4.4358, 0, 1, 100.0], [8.924, 4.8682, 0, 1, 100.0], [8.8296, 5.2941, 0, 1, 100.0], [8.6985, 5.7101, 0, 1, 100.0], [8.5315, 6.1131, 0, 1, 100.0], [8.3301, 6.5, 0, 1, 100.0], [8.0958, 6.8679, 0, 1, 100.0], [7.8302, 7.2139, 0, 1, 100.0]]
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_g02_point_not_in_boundary(self):
            gcode_line = 'G02 X8 Y8 R5 F100'
            self.middle_points = [[-0.4645, 0.4645, 0, 1, 100.0], [0.7861, 0.1698, 0, 1, 100.0], [1.1321, -0.0958, 0, 1, 100.0], [1.5, -0.3301, 0, 1, 100.0], [1.8869, -0.5315, 0, 1, 100.0], [2.2899, -0.6985, 0, 1, 100.0], [2.7059, -0.8296, 0, 1, 100.0], [3.1318, -0.924, 0, 1, 100.0], [3.5642, -0.981, 0, 1, 100.0], [4.0, -1.0, 0, 1, 100.0], [4.4358, -0.981, 0, 1, 100.0], [4.8682, -0.924, 0, 1, 100.0], [5.2941, -0.8296, 0, 1, 100.0], [5.7101, -0.6985, 0, 1, 100.0], [6.1131, -0.5315, 0, 1, 100.0], [6.5, -0.3301, 0, 1, 100.0], [6.8679, -0.0958, 0, 1, 100.0], [7.2139, 0.1698, 0, 1, 100.0], [7.5355, 0.4645, 0, 1, 100.0], [7.8302, 0.7861, 0, 1, 100.0], [8.0958, 1.1321, 0, 1, 100.0], [8.3301, 1.5, 0, 1, 100.0], [8.5315, 1.8869, 0, 1, 100.0], [8.6985, 2.2899, 0, 1, 100.0], [8.8296, 2.7059, 0, 1, 100.0], [8.924, 3.1318, 0, 1, 100.0], [8.981, 3.5642, 0, 1, 100.0], [9.0, 4.0, 0, 1, 100.0], [8.981, 4.4358, 0, 1, 100.0], [8.924, 4.8682, 0, 1, 100.0], [8.8296, 5.2941, 0, 1, 100.0], [8.6985, 5.7101, 0, 1, 100.0], [8.5315, 6.1131, 0, 1, 100.0], [8.3301, 6.5, 0, 1, 100.0], [8.0958, 6.8679, 0, 1, 100.0], [7.8302, 7.2139, 0, 1, 100.0]]
            isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

            assert isValid == self.invalid

    def test_g02_negative_feed_rate(self):
        gcode_line = 'G02 X10 Y10 R5 F-100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    def test_g02_exceeds_feed_rate(self):
        gcode_line = 'G02 X10 Y10 R5 F210'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    def test_invalid_g02_negative_radius(self):
        gcode_line = 'G02 X10 Y10 R-5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    ## G03 boundary test cases
    def test_g03_negative_x_boundary(self):
        gcode_line = 'G03 X-10 Y10 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    def test_g03_exceeds_x_boundary(self):
        gcode_line = 'G03 X110 Y10 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    def test_g03_negative_y_boundary(self):
        gcode_line = 'G03 X10 Y-10 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    def test_g03_exceeds_y_boundary(self):
        gcode_line = 'G03 X10 Y110 R5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    def test_g03_point_not_on_arc(self):
        gcode_line = 'G03 X8 Y8 R5 F100'
        self.middle_points = [[0.4645, 0.4645, 0, 1, 100.0], [0.7861, 0.1698, 0, 1, 100.0], [1.1321, -0.0958, 0, 1, 100.0], [1.5, -0.3301, 0, 1, 100.0], [1.8869, -0.5315, 0, 1, 100.0], [2.2899, -0.6985, 0, 1, 100.0], [2.7059, -0.8296, 0, 1, 100.0], [3.1318, -0.924, 0, 1, 100.0], [3.5642, -0.981, 0, 1, 100.0], [4.0, -1.0, 0, 1, 100.0], [4.4358, -0.981, 0, 1, 100.0], [4.8682, -0.924, 0, 1, 100.0], [5.2941, -0.8296, 0, 1, 100.0], [5.7101, -0.6985, 0, 1, 100.0], [6.1131, -0.5315, 0, 1, 100.0], [6.5, -0.3301, 0, 1, 100.0], [6.8679, -0.0958, 0, 1, 100.0], [7.2139, 0.1698, 0, 1, 100.0], [7.5355, 0.4645, 0, 1, 100.0], [7.8302, 0.7861, 0, 1, 100.0], [8.0958, 1.1321, 0, 1, 100.0], [8.3301, 1.5, 0, 1, 100.0], [8.5315, 1.8869, 0, 1, 100.0], [8.6985, 2.2899, 0, 1, 100.0], [8.8296, 2.7059, 0, 1, 100.0], [8.924, 3.1318, 0, 1, 100.0], [8.981, 3.5642, 0, 1, 100.0], [9.0, 4.0, 0, 1, 100.0], [8.981, 4.4358, 0, 1, 100.0], [8.924, 4.8682, 0, 1, 100.0], [8.8296, 5.2941, 0, 1, 100.0], [8.6985, 5.7101, 0, 1, 100.0], [8.5315, 6.1131, 0, 1, 100.0], [8.3301, 6.5, 0, 1, 100.0], [8.0958, 6.8679, 0, 1, 100.0], [7.8302, 7.2139, 0, 1, 100.0]]
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    def test_g03_negative_feed_rate(self):
        gcode_line = 'G03 X10 Y10 R5 F-100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
    
    def test_g03_exceeds_feed_rate(self):
        gcode_line = 'G03 X10 Y10 R5 F210'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_invalid_g03_negative_radius(self):
        gcode_line = 'G03 X10 Y10 R-5 F100'
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_invalid_g41(self):
        gcode_line = 'G41 D200'
        self.tool_comp = -200
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid

    def test_invalid_g42(self):
        gcode_line = 'G42 D200'
        self.tool_comp = 200
        isValid, check_error = validate_codes(self.mcodes, self.gcodes, self.prev_attributes, gcode_line, self.tools_count, self.feed_rate, self.cur_attributes, self.machine_dimensions, self.max_spindle_speed, self.middle_points, self.tool_comp)

        assert isValid == self.invalid
