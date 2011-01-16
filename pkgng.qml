import Qt 4.7

Rectangle {
    id: page
    width: 640
    height: 480
    state: "showLoadView"

    property variant loadScreenData
    property variant searchScreenData

    Rectangle {
        id: loadScreen
        width: 200
        height: 50
        opacity: 1

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
        opacity: 0
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
        searchScreenData = {
            'textInput': searchBox.textInput,
        }
        controller.init(page)
    }

    states: [
        State {
            name: "showLoadView"
            PropertyChanges { target: loadScreen; opacity: 1; visible: true }
            PropertyChanges { target: searchView; opacity: 0; rotation: 180 }
        },
        State {
            name: "showSearchView"
            PropertyChanges { target: loadScreen; opacity: 0; visible: true; rotation: -180 }
            PropertyChanges { target: searchView; opacity: 1; visible: true }
            PropertyChanges { target: searchBox; focus: true }
        }
    ]

    transitions: [
        Transition {
            PropertyAnimation {
                target: searchView
                properties: "scale,opacity,rotate,visible"
                duration: 1000
            }
        }
    ]
}
