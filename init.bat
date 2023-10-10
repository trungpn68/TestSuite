@echo off
setlocal

rem Run the first batch file
call setup.bat

rem Run the second batch file
call create_venv.bat

endlocal
