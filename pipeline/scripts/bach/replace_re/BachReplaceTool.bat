@echo off
echo y|xcopy g:\pipeline\Python36/d/e/r/k c:\Python36\
pause
pushd "C:\Python36"
start cmd /k "python3 G:\pipeline\scripts\bach\replace_re\batch_reference_tool.py"