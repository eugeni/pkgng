import Qt 4.7

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
        width: 640
        height: 480
        anchors.fill: parent

        SearchBox {
            id: searchBox
            focus: true
            width: 540
            height: 40
            anchors.top: searchView.top
        }

        Rectangle {
            id: listPackagesRect
            anchors.top: searchBox.bottom
            width: searchView.width - listCategoriesRect.width
            height: searchView.height - searchBox.height
            x: 0
            ListPackages {
                id: listPackages
                anchors.fill: parent
            }
        }

        Rectangle {
            id: listCategoriesRect
            width: 200
            height: searchView.height - searchBox.height
            anchors.left: listPackagesRect.right
            anchors.top: searchBox.bottom
            ListCategories {
                id: listCategories
                anchors.fill: parent
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
