import QtQuick 1.0

Rectangle {
    id: page
    width: 640
    height: 480

    SearchBox {
        id: searchBox
        focus: true
        width: 640
        height: 40
        anchors.fill: parent
    }

    List {
        id: list
        anchors.topMargin: 40
    }
}
