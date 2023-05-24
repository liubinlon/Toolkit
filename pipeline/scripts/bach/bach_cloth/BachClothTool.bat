@echo off
echo y|xcopy Z:\Script\Toolkit\pipeline\Python36/d/e/r/k c:\Python36\
pause
pushd "C:\Python36"
start cmd /k "python3 C:\Users\aoyue\Desktop\pipeline\scripts\bach\bach_cloth\batch_cloth_tool.py"