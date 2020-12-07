@ECHO off
REM del /Q /F /S build
REM del /Q /F /S dist
call %~dp0.venv/scripts/activate
python -m pybuild.build run false true
REM cd dist/fxrc
REM for %v in (*.*) do if not %v==VCRUNTIME140.dll upx %v
pause