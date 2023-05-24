@echo off
echo y|xcopy Z:\Script\Toolkit\pipeline\Python36/d/e/r/k c:\Python36\
pause
pushd "C:\Python36"
start cmd /k "python3 Z:\Script\Toolkit\pipeline\scripts\bach\bach_cache\bach_cache_tool.py"