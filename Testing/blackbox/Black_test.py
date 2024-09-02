import os
import subprocess
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

def test_invalid_firmware():
    
    gcode_file_name = 'Complete_invalid.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'Error' in output:
        op_flag = True
    display_test_result("test_invalid_firmware", op_flag)
    assert op_flag == eop_flag

def test_valid_firmware():
    gcode_file_name = 'Complete_valid.gcode'
    gcode_file_name = os.path.join(parent_directory, 'test_gcode_validate', gcode_file_name)
    cmd_argument = gcode_file_name
    # Run the Python script with specific command-line arguments and fixed input
    output = run_python_script(script_path, cmd_argument, input_text)
    eop_flag = True
    op_flag = False
    if 'error' not in output.lower():
        op_flag = True
    display_test_result("test_valid_firmware", op_flag)
    assert op_flag == eop_flag

'''
if __name__ == "__main__":
    # invalid/error Test case
    test_invalid_firmware()
    # valid test case
    test_valid_firmware()
'''