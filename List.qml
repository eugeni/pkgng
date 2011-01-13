import Qt 4.7

ListView {
    id: pythonList
    anchors.fill: parent

    model: pythonListModel

    delegate: Component {
        Rectangle {
            width: pythonList.width
            height: 40
            color: (model.thing.is_title)?"#4867b5":"#fff"

            Item {
                width: 400; height: 40
                anchors.centerIn: parent
                visible: model.thing.is_title

                    Text {
                        anchors.centerIn: parent
                        id: category
                        font.weight: Font.Bold
                        text: model.thing.name
                        color: "white"
                        verticalAlignment: Text.AlignBottom
                    }
            }

            Item {
                width: 400; height: 40
                visible: !model.thing.is_title

                    Text {
                        id: title
                        elide: Text.ElideRight
                        text: model.thing.name
                        color: "black"
                        font.bold: true
                        anchors.leftMargin: 10
                        anchors.fill: parent
                        verticalAlignment: Text.AlignVCenter
                    }
                    Text {
                        id: subtitle
                        elide: Text.ElideRight
                        text: model.thing.description
                        color: "red"
                        anchors.leftMargin: 10
                        anchors.topMargin: 25
                        anchors.fill: parent
                        verticalAlignment: Text.AlignBottom
                    }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: { controller.thingSelected(model.thing) }
            }
        }
    }
}
