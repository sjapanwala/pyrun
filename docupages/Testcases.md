# Testcases
> Released Oct 21, 2024
## [Home](https://github.com/sjapanwala/pyrun) | [Recent Update](updates.md)
## Testcase Usage
> The Testcase function is to test the I/O of a Python Script, Mostly for educational purposes.

### How To Setup Testcase File
- Test Cases can be recieved as anyform of input python can receive.
- Every `odd line` is the Input and every `even line` is the expected output the script is supposed to output. (assume lines start at 1)
```txt
10 5
15
10 5
5
```
> in this case the input is 10 and 5, the expected is 15
### How To Setup Python Script
- This is the script the user/programmer will be performing the testcases on
- the testcase function will deposit values from an `input()` function
- The testcase function will read the output as a `STDOUT` (so a print statement)
```py
def addition(x,y): # this is the function that will be run
  return x + y

def main():
  x,y = map(int, input().split()) # the input can be customized, depends on how the instructor is expecting the output.
  print(addition(x,y)) # the output on this is what is being expected

if __name__ == "__main__":
  main()
```

### Terminal Output
- if a testcase is passed, you will be notified like this``` ✓ | Testcase (#case): Passed (timetaken seconds)```
```txt
✔ | TestCase 1: Passed (0.00089s)
✔ | TestCase 2: Passed (0.00105s)
✔ | TestCase 3: Passed (0.00110s)
✔ | TestCase 4: Passed (0.00111s)

✔ All Cases Passed.
```
- if a test case is failed the output will be similiar.
- the failed test case will create a simple `feedback.txt` file that will give the programmer a hint, show the expected value to help them get on track.
```txt
✘ | TestCase 1: Failed
✘ | TestCase 2: Failed
✘ | TestCase 3: Failed
✘ | TestCase 4: Failed

✘ 4 Test Cases Failed.
Feedback Provided Under 'feedback.txt'
```
> this is what the ```feedback.txt``` file looks like...
```txt
--- CASE 3---
 60 20
Expected Output: 80
Actual Output: 40
--- END OF CASE ---
...
```