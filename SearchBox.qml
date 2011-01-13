import QtQuick 1.0

FocusScope {
    id: searchBox

    Rectangle {
        id: box
        color: "white"
        anchors.fill: parent

        Text {
            id: searchText
            anchors.fill: parent
            text: "Search packages"
            color: "grey"
        }

        TextInput {
            id: textInput
            focus: true
            selectByMouse: true
            anchors.leftMargin: 9
        }

        states: State {
            name: "hasText"; when: textInput.text != ''
            PropertyChanges { target: searchText; opacity: 0 }
        }

        transitions: [
            Transition {
                from: ""; to: "hasText"
                NumberAnimation { exclude: searchText; properties: "opacity" }
            },
            Transition {
                from: "hasText"; to: ""
                NumberAnimation { properties: "opacity" }
            }
        ]
    }
}
