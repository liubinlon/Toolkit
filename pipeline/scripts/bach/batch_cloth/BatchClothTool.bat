@echo off
echo y|xcopy D:\pipeline\Python36/d/e/r/k c:\Python36\
pause
pushd "C:\Python36"
start cmd /k "python3 D:\pipeline\scripts\batch\batch_cloth\batch_cloth_tool.py"