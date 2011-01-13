import Qt 4.7

ListView {
    id: listPackages
    anchors.fill: parent

    model: listPackagesModel

    delegate: Component {
        Rectangle {
            width: listPackages.width
            height: 40
            id: listItem
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
                hoverEnabled: true
                onClicked: { controller.thingSelected(model.thing) }
                onEntered: { listItem.color = (model.thing.is_title)?"#4565b3":"#ddd" }
                onExited: { listItem.color = (model.thing.is_title)?"#4767b5":"#fff" }
            }
        }
    }
}
