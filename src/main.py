#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Std libs
import os
import sys
from pathlib import Path
import logging as log

# Qt Import
from PySide2 import (
    QtCore, QtGui, QtWidgets,
    QtQml, QtQuick, QtWebEngine,
    Qt3DCore, Qt3DRender, Qt3DExtras)

# Qt Alias
Q3DC = Qt3DCore.Qt3DCore
Q3DR = Qt3DRender.Qt3DRender
Q3DE = Qt3DExtras.Qt3DExtras
QC = QtCore
QG = QtGui
QW = QtWidgets
QML = QtQml
QWE = QtWebEngine
QQ = QtQuick
Qt = QC.Qt
Property = QC.Property
Signal = QC.Signal
Slot = QC.Slot
# Resources import
from libs import py_rc

# ENVs

loggerLevel = log.INFO

# init logging
log.basicConfig(level=loggerLevel)

def main():
    app = QG.QGuiApplication(sys.argv)
    # QWE.QtWebEngine.initialize()
    QC.QCoreApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling)
    engine = QML.QQmlApplicationEngine()
    engine.load("qrc:/main.qml")
    if not engine.rootObjects():
        sys.exit("Failed to load ui!")
    app.exec_()

if __name__ == "__main__":
    main()
