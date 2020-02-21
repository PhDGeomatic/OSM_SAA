# -*- coding: utf-8 -*-

import os

from qgis.core import *
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QAction, QFileDialog, QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'OSM_SAA_Save_dialog_base.ui'))


class SaveDialog(QDialog, FORM_CLASS):
    
    def __init__(self, iface, layers, current_Dir, parent=None):
        """Constructor."""
        super(SaveDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        self.iface = iface
        self.fullFileName = None
        self.selectedLayer = None
        self.useCanvasExtent = True
        self.current_Dir = current_Dir
        self.downloadExtent = None
        
        self.setupUi(self)
        
        self.updateComboBox()
        self.updateDownloadArea()
        
        self.pushButton_OutputFile.clicked.connect(self.clickOnSave)
        self.radioButton_CanvasExtent.toggled.connect(self.clickOnRadioButton);
        self.radioButton_LayerExtent.toggled.connect(self.clickOnRadioButton);
        self.comboBox_Layers.currentIndexChanged.connect(self.changedComboBox)
        
    def showEvent(self, event):
        self.updateDownloadArea()
        self.updateComboBox()
        
    def updateComboBox(self):
        self.comboBox_Layers.clear()
        layers = QgsProject.instance().mapLayers().values()
        if len(layers) == 0:
            self.comboBox_Layers.setEnabled(False)
            self.radioButton_LayerExtent.setEnabled(False)
            self.selectedLayer = None            
        else:
            self.radioButton_LayerExtent.setEnabled(True)
            for layer in layers:
                if (layer.type() == QgsMapLayer.VectorLayer):
                    if (layer.geometryType() == QgsWkbTypes.PolygonGeometry):
                        self.comboBox_Layers.addItem(layer.name(), layer)
                        
            if self.useCanvasExtent:
                self.comboBox_Layers.setEnabled(False)
            else:
                self.comboBox_Layers.setEnabled(True)
        
    def updateDownloadArea(self):
        if self.useCanvasExtent:
            canvasExtent = self.iface.mapCanvas().extent()
            self.downloadExtent = canvasExtent
            areaExtent = canvasExtent.height() * canvasExtent.width()
            print(str(canvasExtent.height()) + " " + str(canvasExtent.width()))
            self.label_area.setText(str(round(areaExtent,3)) + ' m2' + ' [' + str(round(areaExtent/1000000,3)) + ' Km2]')
        else:
            if self.selectedLayer:
                layerExtent = self.selectedLayer.extent()
                self.downloadExtent = layerExtent
                areaExtent = layerExtent.height() * layerExtent.width()
                self.label_area.setText(str(round(areaExtent,3)) + ' m2' + ' [' + str(round(areaExtent/1000000,3)) + ' Km2]')
        
    def changedComboBox(self):
        if self.comboBox_Layers.count() > 0:
            index = self.comboBox_Layers.currentIndex();
            self.selectedLayer = self.comboBox_Layers.itemData(index)
            self.updateDownloadArea()
        
    def clickOnSave(self):
        self.fullFileName, filter_string = QFileDialog.getSaveFileName(None, "Select output file", self.current_Dir, '*.shp')
        if (self.fullFileName != ""):
            if not self.fullFileName.endswith(".shp"):
                self.fullFileName = self.fullFileName + ".shp"
            self.lineEdit_outputFile.setText(self.fullFileName)
        
    def clickOnRadioButton(self):
        self.updateDownloadArea()
        self.changedComboBox()
        self.useCanvasExtent = self.radioButton_CanvasExtent.isChecked()
        if self.useCanvasExtent:
            self.comboBox_Layers.setEnabled(False)
        else:
            self.comboBox_Layers.setEnabled(True)
            
        
