import Qt 4.7

ListView {
    id: pythonList
    width: 640
    height: 480

    model: pythonListModel

    delegate: Component {
        Rectangle {
            width: pythonList.width
            height: 40
            color: ((index % 2 == 0)?"#222":"#111")

            Item {
                width: 400; height: 40
                anchors.centerIn: parent

                    Text {
                        id: category
                        font.bold: true
                        text: model.thing.name
                        color: "white"
                        verticalAlignment: Text.AlignBottom
                        visible: model.thing.is_title
                    }
            }

            Item {
                width: 400; height: 40

                    Text {
                        id: title
                        elide: Text.ElideRight
                        text: model.thing.name
                        color: "white"
                        font.bold: true
                        anchors.leftMargin: 10
                        anchors.fill: parent
                        verticalAlignment: Text.AlignVCenter
                        visible: !model.thing.is_title
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
                        visible: !model.thing.is_title
                    }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: { controller.thingSelected(model.thing) }
            }
        }
    }
}
