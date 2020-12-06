@echo off
pushd %~dp0
call .venv/scripts/activate.bat

call pyside2-rcc -o src/main/python/app_rc.py -g python -compress 3 src/main/resources/sources/qml.qrc

fbs run