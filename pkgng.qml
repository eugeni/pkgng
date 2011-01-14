import QtQuick 1.0

Rectangle {
    id: page
    width: 640
    height: 480

    property variant loadScreenData

    Rectangle {
        id: loadScreen
        width: 200
        height: 50
        visible: true

        anchors.centerIn: parent

        Text {
            id: loadScreenProgress
            color: "black"
            text: "Loading medias..."
            verticalAlignment:Text.AlignTop
            anchors.fill: parent
        }
    }

    Rectangle {
        id: searchView
        visible: false
        anchors.fill: parent


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
            anchors.right: searchView.right
            height: searchView.height

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

    Component.onCompleted: {
        loadScreenData = {
            'loadScreenProgress': loadScreenProgress,
            'loadScreen': loadScreen,
            'loadScreenNext': searchView,
        }
        controller.loadMedias(page)
    }

    states: State {
        name: "showSearchView"; when: searchView.visible == true
        PropertyChanges { target: searchBox; focus: true }
    }

}
