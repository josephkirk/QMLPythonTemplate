# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 5.15.2
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xba\
<\
RCC>\x0a  <qresourc\
e prefix=\x22/\x22>\x0a  \
  <file>main.qml\
</file>\x0a    <fil\
e>qml.qrc</file>\
\x0a    <file>qtqui\
ckcontrols2.conf\
</file>\x0a    <fil\
e>resources/plac\
eholder.svg</fil\
e>\x0a  </qresource\
>\x0a</RCC>\x0a\
\x00\x00\x01F\
;\
 This file can b\
e edited to chan\
ge the style of \
the application\x0d\
\x0a; Read \x22Qt Quic\
k Controls 2 Con\
figuration File\x22\
 for details:\x0d\x0a;\
 http://doc.qt.i\
o/qt-5/qtquickco\
ntrols2-configur\
ation.html\x0d\x0a\x0d\x0a[C\
ontrols]\x0d\x0aStyle=\
Material\x0d\x0a\x0d\x0a[Mat\
erial]\x0d\x0aTheme=Da\
rk\x0d\x0a; Accent=Blu\
eGrey\x0d\x0a; Primary\
=Indigo\x0d\x0a; Foreg\
round=Shade50\x0d\x0a;\
 Background=Shad\
e50\x0d\x0a\
\x00\x00\x00\x94\
i\
mport QtQuick 2.\
15\x0d\x0aimport QtQui\
ck.Window 2.15\x0d\x0a\
\x0d\x0aWindow {\x0d\x0a    \
width: 640\x0d\x0a    \
height: 480\x0d\x0a   \
 visible: true\x0d\x0a\
    title: qsTr(\
\x22Hello World\x22)\x0d\x0a\
}\x0d\x0a\
\x00\x00\x00\x00\
\
"

qt_resource_name = b"\
\x00\x07\
\x08?Xc\
\x00q\
\x00m\x00l\x00.\x00q\x00r\x00c\
\x00\x09\
\x0alxC\
\x00r\
\x00e\x00s\x00o\x00u\x00r\x00c\x00e\x00s\
\x00\x15\
\x08\x1e\x16f\
\x00q\
\x00t\x00q\x00u\x00i\x00c\x00k\x00c\x00o\x00n\x00t\x00r\x00o\x00l\x00s\x002\x00.\
\x00c\x00o\x00n\x00f\
\x00\x08\
\x08\x01Z\x5c\
\x00m\
\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
\x00\x0f\
\x05\xf3b\x07\
\x00p\
\x00l\x00a\x00c\x00e\x00h\x00o\x00l\x00d\x00e\x00r\x00.\x00s\x00v\x00g\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x5c\x00\x00\x00\x00\x00\x01\x00\x00\x02\x08\
\x00\x00\x01v9\x1a,\xee\
\x00\x00\x00,\x00\x00\x00\x00\x00\x01\x00\x00\x00\xbe\
\x00\x00\x01v8\xd6\xc9m\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01v9\x22\x0e#\
\x00\x00\x00\x14\x00\x02\x00\x00\x00\x01\x00\x00\x00\x05\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00r\x00\x00\x00\x00\x00\x01\x00\x00\x02\xa0\
\x00\x00\x01v8\xd6\xc9n\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()