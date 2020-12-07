import QtQuick 2.15
import QtQuick.Controls 2
import QtQuick.Window 2.15

Window {
    width: 450
    height: 900
    visible: true
    title: qsTr("Hello QML World")

    Button {
        anchors.fill: parent
        text: "Test Button"
    }
}
