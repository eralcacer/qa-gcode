import os
import subprocess
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
script_path = os.path.join(parent_directory, 'app_cmd.py')
input_text = '\n' * 10

def display_test_result(test_name, result):
    status = "Passed" if result else "Failed"
    print(f"{test_name}: {status}")

def run_python_script(script_path, cmd_argument, input_text):
    # Prepare command-line arguments
    command = ['python', script_path, cmd_argument]

    # Start the process
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Send input text to the script's standard input
    output, _ = process.communicate(input_text)
    return output.splitlines()[-1]

def test_invalid_Tool_compensation_left():
    
    gcode_file_name = 'g41_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'Tool compensation is out of range' in output:
        op_flag = True
    display_test_result("test_invalid_Tool_compensation_left", op_flag)
    assert op_flag == eop_flag

def test_invalid_Tool_compensation_right():
    gcode_file_name = 'g42_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name

    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)

    eop_flag = True
    op_flag = False
    if 'Tool compensation is out of range' in output:
        op_flag = True
    display_test_result("test_invalid_Tool_compensation_right", op_flag)
    assert op_flag == eop_flag

def test_invalid_M3():
    gcode_file_name = 'm3_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name

    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' in output:
        op_flag = True
    display_test_result("test_invalid_M3", op_flag)
    assert op_flag == eop_flag

def test_invalid_M4():
    gcode_file_name = 'm4_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' in output:
        op_flag = True
    display_test_result("test_invalid_M4", op_flag)
    assert op_flag == eop_flag

def test_invalid_M6():
    gcode_file_name = 'm6_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' in output:
        op_flag = True
    display_test_result("test_invalid_M6", op_flag)
    assert op_flag == eop_flag

def test_invalid_line_points_generated():
    gcode_file_name = 'line_points_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'line points' in output:
        op_flag = True
    display_test_result("test_invalid_line_points_generated", op_flag)
    assert op_flag == eop_flag

def test_invalid_arc_points_generated():
    gcode_file_name = 'arc_points_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'middle points' in output:
        op_flag = True
    display_test_result("test_invalid_arc_points_generated", op_flag)
    assert op_flag == eop_flag

def test_radius_invalid():
    gcode_file_name = 'rad_invalid_error.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error radius' in output:
        op_flag = True
    display_test_result("test_radius_invalid", op_flag)
    assert op_flag == eop_flag

def test_invalid_x_dimension():
    gcode_file_name = 'x_dim_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'x boundary error' in output:
        op_flag = True
    display_test_result("test_invalid_x_dimension", op_flag)
    assert op_flag == eop_flag

def test_invalid_y_dimension():
    gcode_file_name = 'y_dim_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'y boundary error' in output:
        op_flag = True
    display_test_result("test_invalid_y_dimension", op_flag)
    assert op_flag == eop_flag

def test_invalid_z_dimension():
    gcode_file_name = 'z_dim_invalid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'z boundary error' in output:
        op_flag = True
    display_test_result("test_invalid_z_dimension", op_flag)
    assert op_flag == eop_flag

def test_valid_arc_points_generated():
    gcode_file_name = 'arc_points_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_arc_points_generated", op_flag)
    assert op_flag == eop_flag

def test_valid_Tool_compensation_left():
    
    gcode_file_name = 'g41_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_Tool_compensation_left", op_flag)
    assert op_flag == eop_flag

def test_valid_Tool_compensation_right():
    
    gcode_file_name = 'g42_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_Tool_compensation_right", op_flag)
    assert op_flag == eop_flag

def test_valid_line_points_generated():
    gcode_file_name = 'line_points_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_line_points_generated", op_flag)
    assert op_flag == eop_flag

def test_valid_M3():
    gcode_file_name = 'm3_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name

    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_M3", op_flag)
    assert op_flag == eop_flag

def test_valid_M4():
    gcode_file_name = 'm4_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name

    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_M4", op_flag)
    assert op_flag == eop_flag

def test_valid_M6():
    gcode_file_name = 'm6_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_M6", op_flag)
    assert op_flag == eop_flag

def test_radius_valid():
    gcode_file_name = 'rad_valid_error.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_radius_valid", op_flag)
    assert op_flag == eop_flag

def test_valid_dimensions():
    gcode_file_name = 'dim_valid_err.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_dimensions", op_flag)
    assert op_flag == eop_flag

def test_valid_block():
    gcode_file_name = 'block_valid_sequence_commands.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_block_sequence_commands", op_flag)
    assert op_flag == eop_flag

def test_invalid_block():
    gcode_file_name = 'block_invalid_sequence_commands.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = False
    op_flag = True
    if 'error' in output.lower():
        op_flag = False
    display_test_result("test_invalid_block_sequence_commands", op_flag)
    assert op_flag == eop_flag

'''
if __name__ == "__main__":
    # invalid/error Test cases
    test_invalid_Tool_compensation_left()
    test_invalid_Tool_compensation_right()
    test_invalid_M3()
    test_invalid_M4()
    test_invalid_M6()
    test_invalid_line_points_generated()
    test_invalid_arc_points_generated()
    test_radius_invalid()
    test_invalid_x_dimension()
    test_invalid_y_dimension()
    test_invalid_z_dimension()
    test_invalid_block()
    # valid test cases
    test_valid_arc_points_generated()
    test_valid_Tool_compensation_left()
    test_valid_Tool_compensation_right()
    test_valid_line_points_generated()
    test_valid_M3()
    test_valid_M4()
    test_valid_M6()
    test_radius_valid()
    test_valid_dimensions()
    test_valid_block()
'''    
