import Qt 4.7

ListView {
    id: listCategories
    anchors.fill: parent

    model: listCategoriesModel

    delegate: Component {
        Rectangle {
            width: listCategories.width
            height: 40
            id: listItem
            color: "cyan"

            Item {
                width: 400; height: 40

                    Text {
                        id: title
                        elide: Text.ElideRight
                        text: model.category.name
                        color: "black"
                        font.bold: true
                        anchors.leftMargin: 10
                        anchors.fill: parent
                        verticalAlignment: Text.AlignVCenter
                    }
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onClicked: { controller.categorySelected(model.category) }
            }
        }
    }
}
