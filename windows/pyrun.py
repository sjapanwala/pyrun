#!/usr/bin/env python3

# import sections
from os import sys
import os
import subprocess
import time
import json
import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

# global vars
allowed_files = [".py"]
readfile = ".pyout"
allowed_args = ["help","--ns", "--v","--new","--del"]
version = 0.21
config_path = "~/.config/pyrun/pyrun.json"
# this little thing check if your system is runnng python3 or python
python_startvar="py"  

def get_config(config_path,arg):
    config_path = os.path.expanduser(config_path)
    """
    This function reads the config file and updates the global variables"""
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {
            "ColoredSyntax":True,
            "STDOUT":True,
            "StartScript": True
        }
    global startscript
    startscript = config["StartScript"]
    global colored_syntax
    colored_syntax = config["ColoredSyntax"]
    global stdout
    stdout = config["STDOUT"]
    if arg == "printconfig":
        print(config)
        exit(0)
    elif arg == "verifyconfig":
        if stdout != True or False:
            print("Config Error: STDOUT must be True or False")
            exit(1)
def get_errors(filename):
    """
    This function runs the python file chosen, and creates a intermediate text script that store the errors that the script has, only creates the file if errors exist, else no files created. the file is deleted afterwards

    input:
        filename (str) -> this is the name of the file to run, is taken by an argv
    output:
        status (bool) -> returns a boolean value, returns true if error is caught
    """
    script_args = sys.argv[2:]  # Everything after the filename
    result = subprocess.run(
        [python_startvar, filename] + script_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.stderr:
        with open(readfile, "w") as error_file:
            error_file.write(result.stderr)
        return True
    else:
        return False
    
def read_errors(filename):
    """
    This function reads the error file created by get_errors and parses the error information.
    It returns a list of tuples containing the line number, variable line, and error description.

    indexing of information

    0 -> line number of error
    1 -> contents of line number
    2 -> standard error msg outputted by interpreter

    input:
        filename (str) -> name of the file (used to match the format)
    output:
        errors (list) -> returns a list of errors with their details
    """
    errors = []
    with open(readfile, "r") as file:
        lines = file.readlines()

        i = 0
        while i < len(lines):
            if lines[i].startswith('  File '):
                error_info = lines[i].strip()
                variable_line = ""
                error_desc_lines = []

                # Extract line number using regex
                match = re.search(r'line (\d+)', error_info)
                if match:
                    line_number = match.group(1)
                else:
                    line_number = "Unknown"

                # Variable line (if present)
                if i + 1 < len(lines) and not lines[i + 1].startswith('  File '):
                    variable_line = lines[i + 1].strip()
                    i += 1

                # Collecting error description lines
                while i < len(lines) and not lines[i].startswith('  File ') and lines[i].strip():
                    error_desc_lines.append(lines[i].strip())
                    i += 1

                error_desc = " ".join(error_desc_lines).strip()
                error_message_index = error_desc.rfind("^")
                error_desc = error_desc[error_message_index+1:]

                errors.append((line_number, variable_line, error_desc))
            else:
                i += 1
    return errors


def colorize_error_with_syntax(code):
    """
    Add syntax highlighting to the code part of the error tuple using Pygments.
    
    Arguments:
        error (tuple): A tuple containing (line number, code, error description)
    
    Returns:
        tuple: A tuple with the line number, syntax-highlighted code, and description
    """
    if colored_syntax:
        return highlight(code, PythonLexer(), TerminalFormatter()).strip()
    else:
        return code

def underline_error(error):
    """
    Reads the last line of the error file and strips it of any newline characters.
    
    input:
        error (list): A list of tuples containing (line number, code, error description)
    
    output:
        str: The last line of the error file, stripped of any newline characters
    """
    with open(readfile, "r") as file:
        lines = file.readlines()
        return (lines[-2].rstrip())

def display_error_stack(errors, filename, underline):
    """
    Displays the error stack of a given Python file with line numbers, syntax highlighting, and error indicators.
    
    Args:
        errors (list): A list of tuples containing (line number, code, error description)
        filename (str): The name of the file to display
        underline (str): The underline string from the error output file
    
    Returns:
        None
    """
    test = 2
    print(f"\033[47m\033[91m ERR! \033[0m\033[91m Error on Line \033[33m{errors[-1][0]}\033[91m Detected\033[0m\033[33m\033[0m\n\033[97m{errors[-1][-1]}\n")
    
    # Read the entire file content into a list of lines
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.rstrip() for line in file]

    # Determine the maximum number of digits in the line numbers
    max_line_number_length = len(str(len(lines)))

    def format_line_number(line_number):
        """Format the line number with padding to align columns."""
        return f"{line_number:>{max_line_number_length}}"

    for error in errors:
        test -= 1
        try:
            # Validate that the first element of the error is a valid number
            if error[0].isdigit():
                error_line_num = int(error[0]) - 1  # Adjust for 0-based indexing
            else:
                #print(f"Invalid line number: {error[0]}")
                continue

            # Determine the context lines
            pre_line = max(0, error_line_num - 1)
            curr_line = error_line_num
            post_line = min(len(lines) - 1, error_line_num + 1)

            # Display previous line if it exists
            if colored_syntax:
                pre_line_space = len(lines[pre_line]) - len(lines[pre_line].lstrip())
            else:
                pre_line_space = 0
            if pre_line < curr_line:
                print(f'    \033[90m{format_line_number(pre_line + 1)}\033[0m | {((" ") * (pre_line_space) )}{colorize_error_with_syntax(lines[pre_line])}')

            # Display current line with error indicator\
            if colored_syntax:
                curr_line_space = len(lines[curr_line]) - len(lines[curr_line].lstrip())
            else:
                curr_line_space = 0
            print(f'\033[91m->  {format_line_number(curr_line + 1)} | \033[0m{((" ") * (curr_line_space) )}{colorize_error_with_syntax(lines[curr_line])}')
            if underline and test < 1:
                #if test < 1:
                    underline_position = len(f'{format_line_number(curr_line + 1)} | ') + curr_line_space  # Adjust for line number and space
                    print(f'\033[91m{" " * underline_position}\033[91m{underline}')
            # Display next line if it exists
            if colored_syntax:
                post_line_space = len(lines[post_line]) - len(lines[post_line].lstrip())
            else:
                post_line_space = 0
            if post_line > curr_line:
                print(f'    \033[90m{format_line_number(post_line + 1)}\033[0m | {((" ") * (post_line_space) )}{colorize_error_with_syntax(lines[post_line])}')
            #print(f"    {(len(str((post_line)))+1)*"-"}|")
        except (ValueError, IndexError) as e:
            # Handle cases where error[0] is not a valid number or index out of bounds
            print(f"Error processing the error stack: {e}")

def runtestcases(filename,testcasefile):
    # first we need to check if the file will even run
    print(f"\033[97mRunning {filename} With {testcasefile}\n\033[0m\033[3mPress Enter To Run\033[0m")
    if get_errors(filename) ==  True:
        errors = read_errors(filename)
        underline = underline_error(errors)
        display_error_stack(errors,filename,underline)
        exit(1)
    else:
        if os.path.exists("feedback.txt") == True:
            os.system("del feedback.txt")
        with open(testcasefile, 'r') as f:
            lines = f.readlines()

        if len(lines) % 2 != 0:
            print("Format Error: Test case file should have even number of lines")
            return
        test_case_validity = True
        cases_failed = 0
        for i in range(0, len(lines), 2):
            starttime = time.time()
            input_data = lines[i].strip()
            expected_output = lines[i + 1].strip()

            process = subprocess.Popen(
                [f'{python_startvar}', filename],  
                stdin=subprocess.PIPE,  
                stdout=subprocess.PIPE,  
                stderr=subprocess.PIPE,  
                text=True   
            )

            
            endtime = time.time()

            output, error = process.communicate(input_data)

            if error:
                print(f"Error in test {i//2 + 1}:")
                #print(error.strip())
                exit(1)
                continue

            if output.strip() == expected_output:
                print(f"\033[92m✔\033[0m | TestCase {i//2 + 1}: \033[92mPassed\033[0m \033[90m({endtime - starttime:.5f}s)\033[0m")
                feedback = f"--- CASE {i//2 + 1}--- \n {input_data}\nExpected Output: {expected_output}\nActual Output: {output.strip()}\n"
                with open('feedback.txt', "a") as testcase_result:
                    testcase_result.write(feedback)
            else:
                print(f"\033[91m✘\033[0m | TestCase {i//2 + 1}: \033[91mFailed\033[0m")
                test_case_validity = False
                cases_failed += 1
                feedback = f"--- CASE {i//2 + 1}--- \n {input_data}\nExpected Output: {expected_output}\nActual Output: {output.strip()}\n"
                with open('feedback.txt', "a") as testcase_result:
                    testcase_result.write(feedback)
        if test_case_validity:
            print("\n\033[92m✔\033[0m All Cases Passed.")
            passed_cases = (len(lines) // 2 - cases_failed)
            percentage_passed = (passed_cases / (len(lines) // 2)) * 100
            print(f"Passed Percentage: {percentage_passed:.2f}%\nFeedback Provided Under '\033[92mfeedback.txt\033[0m'")
            with open('feedback.txt', "a") as testcase_result:
                    testcase_result.write(f'\n\n --- SUMMARY ---\nPassed Cases: {passed_cases}\nFailed Cases: {cases_failed}\nPassed Percentage: {percentage_passed}')
        else:
            passed_cases = (len(lines) // 2 - cases_failed)
            percentage_passed = (passed_cases / (len(lines) // 2)) * 100
            print(f"\n\033[91m✘\033[0m {cases_failed} Test Cases Failed.\nPassed Percentage: {percentage_passed:.2f}%\nFeedback Provided Under '\033[92mfeedback.txt\033[0m'")


        

        

def help_func():
    """
    Prints the help menu for pyrun.
    
    The help menu includes information about the usage of pyrun, valid arguments, and a brief description of each argument.
    """
    print("""
\033[94m    ____        \033[93m____            
\033[94m   / __ \\__  __\033[93m/ __ \\__  ______ 
\033[94m  / /_/ / / / \033[93m/ /_/ / / / / __ \\
\033[94m / ____/ /_/ \033[93m/ _, _/ /_/ / / / /
\033[94m/_/    \\__, /\033[93m_/ |_|\\__,_/_/ /_/ 
\033[94m      /____/                    \n
\033[97m Welcome To \033[94mPy\033[93mrun\033[0m
    Pyrun is an addon for the standard Python Interpreter 
    designed to aid in Python Development.
    Inspiration taken from the GCC compiler.
          
    \033[97mUsage: \033[34m<ARG1> \033[33m<ARG2> \033[33m<ARG3> \033[90m<External Arg Required By Running File>\033[0m   
        Filename:  Add a file name to run in standard mode
        Arguement: Add a listed arg, to run script in a special mode
          
    \033[97mValid Arguements:\033[0m
         help    Launches Help Menu
         --ns    Normal Start, Is Default Already
         --v     Check Version
         --new   Update App
         --del   Delete App
         --rt    Run Test Cases, Pipe The Outputs And Diff Testcases
         --new   Update Application (sudo access required)
         --del   Delete Application (sudo access required)
          """)
    
def version_help():
    """
    Prints the version of pyrun
    """
    print(f"Pyrun Version \033[92m{version}\033[0m\nTo Run Update, Run \033[92m'sudo py --new'\033[0m")

def update_script():
    """
    Updates the script to the latest version
    """
    if os.geteuid() != 0:
        print('\033[4m\033[94mpy\033[93mrun\033[0m: This Action Requires Sudo Access, Please run \033[32m"sudo py --new"\033[0m.')
        sys.exit(1)
    else:
        try:
            result = subprocess.run(
                ["sudo", "curl", "-s", "-o", "/usr/local/bin/py", "https://raw.githubusercontent.com/sjapanwala/pyrun/refs/heads/main/unix/pyrun.py"],
                check=True
            )
            print('\033[4m\033[94mpy\033[93mrun\033[0m: \033[32mUpdated Successfully\033[0m.\nUpdates:')
            #os.system("curl -s addupdatelink")
        except subprocess.CalledProcessError as e:
            print(f'\033[4m\033[94mpy\033[93mrun\033[0m: \033[31mFailed To Update {e}\033[0m.')
            sys.exit(1)
def delete_script():
    """
    Deletes the script
    """
    if os.geteuid() != 0:
        print('\033[4m\033[94mpy\033[93mrun\033[0m: This Action Requires Sudo Access, Please run \033[32m"sudo py --del"\033[0m.')
        sys.exit(1)
    else:
        try:
            result = subprocess.run(
                ["sudo", "rm", "/usr/local/bin/py"],
                check=True
            )
            print('\033[4m\033[94mpy\033[93mrun\033[0m: \033[37mWe Are Sad To See You Go :(. \nIf Theres Something We Can Make Right Please Let Us Know!\033[0m\n\033[92mDeleted Successfully\033[0m')
        except subprocess.CalledProcessError as e:
            print(f'\033[4m\033[94mpy\033[93mrun\033[0m: \033[31mFailed To Delete {e}\033[0m.')
            sys.exit(1)

def main():
    get_config(config_path,None)
    if len(sys.argv) < 2:
        print('\033[4m\033[94mpy\033[93mrun\033[0m: \033[91mNo Arguement Given\033[0m\nPlease provide a \033[4mFilename\033[0m or an \033[4mArgument\033[0m.')
        exit(1)
    elif sys.argv[1] == "help":
        help_func()
        exit()

    elif sys.argv[1] == "--v":
            version_help()
            exit(0)

    elif sys.argv[1] == "--new":
            update_script()
            exit(0)

    elif sys.argv[1] == "--del":
            delete_script()
            exit(0)
    elif sys.argv[1] == "--rt":
        runtestcases(sys.argv[2],sys.argv[3])



    # this runs the basic script of runnning a python file in standard
    elif sys.argv[1] not in allowed_args:
        file_to_run = sys.argv[1]
        #print("\033[90mNo File Arg Detected, Staring In Normal Mode\033[0m")
        if os.path.exists(file_to_run):
            if file_to_run[file_to_run.rfind("."):] not in allowed_files:
                print(f'\033[4m\033[94mpy\033[93mrun\033[0m: \033[91mFile Doesnt Qualify\033[0m\nThe file \033[4m"{file_to_run}"\033[0m is not a standard Python File\033[0m.')
                exit(1)
            if get_errors(file_to_run) == False:
                if startscript:
                    if stdout:
                        print(f'\033[4m\033[94mpy\033[93mrun\033[0m:\033[92m No Errors Found! \n\033[90m<-- STDOUT -->\033[0m\n')
                    #print(f'\033[4m\033[94mpy\033[93mrun\033[0m:\033[92m\033[0m Running {file_to_run}\n')
                    additional_args = ' '.join(sys.argv[2:])
                    os.system(f"{python_startvar} {file_to_run} {additional_args}")
                    exit(0)
            else:
                errors = read_errors(sys.argv[1])
                #print(errors)
                underline = underline_error(errors)
                display_error_stack(errors,sys.argv[1],underline)
                exit(1)
        else:
            print(f'\033[4m\033[94mpy\033[93mrun\033[0m: \033[91mFile Doesnt Exist\033[0m\nThe file \033[4m"{file_to_run}"\033[0m doesnt exist\033[0m.')
            exit(1)
    elif sys.argv[1] in allowed_args:
        pass
    else:
        print(f'\033[4m\033[94mpy\033[93mrun\033[0m: \033[92mArg Too Ambigious\033[0m\n')

        



if __name__ == "__main__":
    main()
