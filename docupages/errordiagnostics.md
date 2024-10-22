# Error Diagnostics
> Released Oct 15, 2024
## [Home](https://github.com/sjapanwala/pyrun) | [Recent Update](updates.md)

### Overview
- Error Diagnostics is a built-in feature of Pyrun that analyzes and reports errors in Python code. It is designed to behave like the GCC compiler, providing a clean, clear breakdown of where errors occur in your code, so you can quickly identify and fix issues.

- This tool is useful for catching and displaying errors with relevant line numbers, error types, and pinpointed locations within the code. It’s perfect for debugging during development.

### Features
- Error Breakdown: Shows the exact line number and code snippet where an error occurred.
- Error Type Identification: Detects common Python errors like ZeroDivisionError, IndexError, and others.
- Syntax Highlighting: Highlights problematic code for easier reading and understanding of errors.
- Step-by-Step Debugging: Helps to trace the flow of your program to pinpoint the root cause of an issue.
- Easy Integration: You just need to pass the filename as an argument to enable error diagnostics.

### Error Diagnostics Usage
- This is the basic function, where the errors are listed like the GCC Compiler
- Add the filename as an arguement, `py <filename>`

### Example I/O
- Calling a buggy function, will show you where the function is
- Will also show where the error in the function takes place like it does below
```sh
 ERR!  Error on Line 3 Detected
~ ZeroDivisionError: division by zero

    10 |
->  11 | buggy_function()
       |
     2 |  
->   3 |     result = 10 / 0
       |              ~~~^~~
     4 |
```

### Supported Errors
- ZeroDivisionError
- IndexError
- NameError
- TypeError
- SyntaxError
- AttributeError
- And many more common exceptions