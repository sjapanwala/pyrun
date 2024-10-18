# Pyrun
> A Python addon that makes the interpreter experienct better

# <center> [Welcome](#what-is-pyrun) | [Installation](#installation) | [Usage](#usage) | [Help](#help-me)
<p align="center">
<img src="https://img.shields.io/badge/Active_Development-green">
<img src="https://img.shields.io/badge/Tested-Unix-white">
<img src="https://img.shields.io/badge/python3-yellow">
<img src="https://img.shields.io/badge/Version-0.1 BETA-red">
</p>
![Screenshot 2024-10-17 at 4 46 34 PM](https://github.com/user-attachments/assets/2a55e6b5-4d61-4fad-a57e-bddcc64443d1)


<img src="https://github.com/user-attachments/assets/dbcf13f1-66a8-4d3c-b55f-fe48f96181d7">
<div style="display: flex; justify-content: space-between; width: 100%;">
    <p style="margin: 0;">Pyrun's Interpreter Addon</p>
    <p style="margin: 0;">Pythons Standard Interpreter</p>
</div>

## What Is Pyrun?
PyRun is an innovative command-line tool designed to streamline Python development by enhancing error handling and debugging processes. Built to assist both novice and experienced developers, PyRun offers an intuitive interface for running Python scripts while providing detailed feedback on any errors encountered during execution.
Key Features:

- Automatic Error Detection: PyRun runs your Python scripts and captures any errors that arise, generating a comprehensive report that highlights the exact lines of code causing issues.
- Syntax Highlighting: Error reports are formatted with syntax highlighting for easy readability, allowing developers to quickly identify and understand their mistakes.
- Contextual Information: Alongside error details, PyRun provides the surrounding lines of code, giving developers the necessary context to effectively troubleshoot problems.
- [NOT RELEASED] Test Case Management: Users can create and run test cases against their scripts, ensuring that their code behaves as expected under various scenarios.
- Customizable Command-Line Options: PyRun supports various arguments to tailor its functionality, making it adaptable to different development workflows.

## Installation
### Some Prerequisites 🚀
- **Python**: Version 3.6 or higher
  - You can install Python from [python.org](https://www.python.org/downloads/).
- **pip**: Python package manager (included with Python installation)
  - Check if pip is installed by running:
  ```pip3 --version```
- **Dependencies**: This project requires the following Python libraries:
  - `pygments` (install script will prompt installation)

### Installation ⬇
> NOTE: for deletion, you have to run this command again or run 'sudo py --del'

```sh
curl -s -o install.sh https://raw.githubusercontent.com/sjapanwala/pyrun/refs/heads/main/install.sh && bash install.sh
```
## Usage
Using Pyrun is super simple, instead of typing python, or python3 everytime you go to run your python file.

Simply Run This Command
```zsh
```



## Help Me
### Some FAQ 🙋
**if you have a question not listed here, please open an** ***Issue*** **, and we will resolve it ASAP**
-  **What if I have an alias, or another program running the 'py' prefix?**
    - If you would like to change the prefix, you would have to alter the `install.sh` file.
    1. Run the install command, but abort it with `ctrl + c`.
    2. Using a text editior of your choice, change the `$TARGET_PATH` change the `py` to the prefix of your choice.
    > Keep in mind: since the prefix is changes, every command you run, `py` will need to be substituted with the prefix of your choice 
