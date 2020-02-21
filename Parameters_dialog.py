# -*- coding: utf-8 -*-

import os

from qgis.core import *
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QAction, QFileDialog, QDialog, QMessageBox
from PyQt5.QtGui import QIcon, QColor, QDoubleValidator, QIntValidator, QRegExpValidator

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'OSM_SAA_Parameters_dialog_base.ui'))


class ParametersDialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(ParametersDialog, self).__init__(parent)     
        self.setupUi(self)
        self.pushButton_SetJavaPath.clicked.connect(self.clickOnSetJavaPath)
        
        # doubleValidator = QDoubleValidator()
        # intValidator = QIntValidator()
        doubleValidator = QRegExpValidator(QRegExp("[+-]?\\d*[\\.]?\\d+"))
        intValidator = QRegExpValidator(QRegExp("\\d*"))
        
        self.lineEdit_compatibilityAngle.setValidator(doubleValidator)
        self.lineEdit_maxSearchDistance.setValidator(doubleValidator)
        self.lineEdit_isolateDistance.setValidator(doubleValidator)
        self.lineEdit_equalTollerance.setValidator(doubleValidator)
        self.lineEdit_significantAngle.setValidator(doubleValidator)
        self.lineEdit_Iteration.setValidator(intValidator)
        
    def clickOnSetJavaPath(self):
        defaultPath = 'C:/Program Files (x86)/Common Files/Oracle/Java/javapath/java.exe'
        fullFileName, filter_string = QFileDialog.getOpenFileName(None,"LOAD", defaultPath, "Homologous SW (*.exe *.sh);;EXE (*.exe);;SH (*.sh)");
        if (fullFileName != ""):
            self.lineEdit_JavaPath.setText(fullFileName)            
        
    def getParameters(self):
        parameters={}                         
        parameters["param1"] = self.comboBox_Transformation.currentText()
        parameters["param2"] = self.lineEdit_compatibilityAngle.text()
        parameters["param3"] = self.lineEdit_maxSearchDistance.text()
        parameters["param4"] = self.lineEdit_isolateDistance.text()
        parameters["param5"] = self.lineEdit_equalTollerance.text()
        parameters["param6"] = self.lineEdit_significantAngle.text()
        parameters["param7"] = self.lineEdit_Iteration.text()
        parameters["param8"] = self.lineEdit_JavaPath.text()
        return parameters
        
    def closeEvent(self, event):
        pass

        
    def setParameters(self, parameters):       
        index = self.comboBox_Transformation.findText(parameters["param1"])
        if index >= 0:
            self.comboBox_Transformation.setCurrentIndex(index)        
        self.lineEdit_compatibilityAngle.setText(parameters["param2"])
        self.lineEdit_maxSearchDistance.setText(parameters["param3"])
        self.lineEdit_isolateDistance.setText(parameters["param4"])
        self.lineEdit_equalTollerance.setText(parameters["param5"])
        self.lineEdit_significantAngle.setText(parameters["param6"])
        self.lineEdit_Iteration.setText(parameters["param7"])
        self.lineEdit_JavaPath.setText(parameters["param8"])
    
