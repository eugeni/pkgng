import QtQuick 1.0

Rectangle {
    id: page
    width: 640
    height: 480

    Rectangle {
        id: menu
        width: 100
        height: 480

        Text {
            id: getPackages
            font.weight: Font.Bold
            color: "black"
            text: "Get packages"
            verticalAlignment: Text.AlignTop
            anchors.fill: parent
        }
    }

    Rectangle {
        id: content
        anchors.left: menu.right
        anchors.right: page.right
        height: page.height

        SearchBox {
            id: searchBox
            focus: true
            width: 540
            height: 40
            anchors.fill: parent
        }

        ListPackages {
            id: list
            anchors.topMargin: 40
        }
    }
}
