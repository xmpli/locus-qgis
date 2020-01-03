import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, Qt
from qgis.gui import QgsMapToolEmitPoint
from .config import Config
from .api import API
import urllib.parse


class SearchWidget():
    SearchDock, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), '../UI/Search.ui'))

    class widget(QtWidgets.QDockWidget, SearchDock):
        closingPlugin = pyqtSignal()

        def __init__(self, iface, parent=None):
            super(SearchWidget.widget, self).__init__(parent)
            self.setupUi(self)
            self.canvas = iface.mapCanvas()

            pointTool = QgsMapToolEmitPoint(self.canvas)
            pointTool.canvasClicked.connect(self.setLocation)
            self.canvas.setMapTool(pointTool)

            self.options = {
                'category': '',
                'method': 'list_categories',
                'search_text': '',
                'location': {
                    'x': 0,
                    'y': 0,
                }
            }

            options = API.makeCall(self.options)
            self.options['category'] = options[0]
            self.options['method'] = 'category_search'

            for option in options:
                if isinstance(option, str):
                    self.categoryCombo.addItem(option)

            self.categoryCombo.activated[str].connect(self.categoryChanged)
            self.modeCombo.activated[str].connect(self.methodChanged)

            # Open the settings widget on button click
            widget = SettingsWidget.widget()
            self.settingsButton.clicked.connect(lambda: WidgetManager.ChangeWidget(widget, False))

            self.runButton.clicked.connect(self.runQuery)

        def setLocation(self):
            point = self.canvas.getCoordinateTransform().toMapCoordinates(self.canvas.mouseLastXY())
            self.options['location'] = {
                'x': point[0],
                'y': point[1],
            }
            print(point[0])

        def runQuery(self):
            point = self.canvas.getCoordinateTransform().toMapCoordinates(self.canvas.mouseLastXY())
            self.options['location'] = {
                'x': point[0],
                'y': point[1],
            }
            self.options['search_text'] = urllib.parse.quote(self.searchField.text(), safe='')
            print(self.options)
            API.makeCall(self.options, debug=True)

        def categoryChanged(self, category):
            self.options['category'] = category

        def methodChanged(self, option):
            self.options['method'] = callPoints[option]

        def closeEvent(self, event):
            self.closingPlugin.emit()
            event.accept()

class SettingsWidget():
    SettingsDock, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), '../UI/Settings.ui'))

    class widget(QtWidgets.QDockWidget, SettingsDock):
        closingPlugin = pyqtSignal()

        def __init__(self, parent=None):
            super(SettingsWidget.widget, self).__init__(parent)
            self.settings = Config.getConfig()
            self.setupUi(self)
            self.endpointField.setText(self.settings['endpoint'])
            self.saveButton.clicked.connect(self.updateConfig)
            self.cancelButton.clicked.connect(self.returnToSearch)

        def updateConfig(self):
            endpoint = self.endpointField.text()
            self.settings['endpoint'] = endpoint
            Config.updateConfig(self.settings)
            self.returnToSearch()

        def returnToSearch(self):
            # Go back to the main search widget
            widget = SearchWidget.widget()
            WidgetManager.ChangeWidget(widget, False)

        def closeEvent(self, event):
            self.closingPlugin.emit()
            event.accept()

class WidgetManager():
    main = None

    def __init__(self, plugin):
        WidgetManager.main = plugin

    @staticmethod
    def ChangeWidget(new_widget, docked=True, init_script=None):
        WidgetManager.main.dockwidget = new_widget
        WidgetManager.main.dockwidget.closingPlugin.connect(WidgetManager.main.onClosePlugin)
        if docked:
            WidgetManager.main.iface.addDockWidget(Qt.LeftDockWidgetArea, WidgetManager.main.dockwidget)
        if init_script is not None:
            init_script()
        WidgetManager.main.dockwidget.show()
