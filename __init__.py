#-----------------------------------------------------------
# Copyright (C) 2020 Xmpli Ltd.
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QAction, QMessageBox
from .Modules.widgets import SearchWidget, SettingsWidget, WidgetManager
from .Modules.logging import addLogEntry, setSessionIdentifier
from .Modules.config import Config

def classFactory(iface):
    return LocusQGIS(iface)


class LocusQGIS:
    def __init__(self, iface):
        self.iface = iface

        # Set up the toolbar menu options
        self.menu = self.tr(u'&Xmpli')
        self.toolbar = self.iface.addToolBar(u'LocusQGIS')
        self.toolbar.setObjectName(u'LocusQGIS')

        # Initialise config
        Config()

        # Setup logging for session
        setSessionIdentifier()
        addLogEntry('Plugin Initialised')

        # Initialise the widget manager
        WidgetManager(self)

    def initGui(self):
        self.action = QAction('Open', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    # Unload the plugin from QGIS
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def onClosePlugin(self):
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        self.pluginIsActive = False

    # Call Qt's Translation API
    def tr(self, message):
        return QCoreApplication.translate('LocusQGIS', message)

    def run(self):
        # Set the default widget to the search widget
        self.dockwidget = SearchWidget.widget(self.iface)
        self.dockwidget.closingPlugin.connect(self.onClosePlugin)

        # Load the widget
        WidgetManager.ChangeWidget(self.dockwidget, False)
