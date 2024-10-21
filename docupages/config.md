# Configurations
> Released Oct 21, 2024
## [Home](https://github.com/sjapanwala/pyrun) | [Recent Update](updates.md)
## Config File
> this will providde a littl bit of customizability
### Creating The Config
- the config file should be located under `~/.config/pyrun`, pyrun cannot detect any other locations, unless modified in the source code.

### No Config Created
- if a config is not created, the application will continue to run, but run off a preset config.

### Structuring The Config
```json
{
  "StartScript":true,
  "STDOUT": true,
  "ColoredSyntax":true
}
```
### Config Tags and Usages
#### **StartScript**
  - Run script on end of execution
  - Expected As a Bool
    - `"true" -> X` 
    - `true -> ✓`
#### **STDOUT**
  ```txt
  pyrun: No Errors Found!
  <-- STDOUT -->
  ```
  - show this as an output before the STDOUT of the script
  - Expected As a Bool
    - `"true" -> X` 
    - `true -> ✓`
#### **ColoredSyntax**
  - Colorizes Python3 syntax when being displayed in terminal
  - Expected As a Bool
    - `"true" -> X` 
    - `true -> ✓`
