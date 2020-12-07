@ECHO off
call %~dp0.venv/scripts/activate
python -m pybuild.build run true
pause