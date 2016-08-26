from __future__ import division
import sys
import os
import time
from PyQt4 import QtCore, QtGui, uic
from dic import uiStrings

qtCreatorFile = "MAP.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def printout(self):
        print str(self.comboBox_Profiles.currentText())
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.commandLinkButton_Run.clicked.connect(self.runHM)
        
    def runHM(self):
        profiles	= uiStrings.get(str(self.comboBox_Profiles.currentText()))
        videos		= uiStrings.get(str(self.comboBox_Videos.currentText()))
        nFs			= (str(self.spinBox_NF.value()))
        QPs			= (str(self.comboBox_QP.currentText()))
        sRanges		= (str(self.comboBox_SR.currentText()))
        size_L1		= uiStrings.get(str(self.comboBox_L1Size.currentText()))
        size_Ll		= uiStrings.get(str(self.comboBox_LLSize.currentText()))
        ass_L1		= (str(self.comboBox_L1Ass.currentText()))
        ass_Ll		= (str(self.comboBox_LLAss.currentText()))
        cache_word	= (str(self.comboBox_Word.currentText()))
        
        timeDef = time.strftime("%y_%m_%d-%H:%M")
        callHM =  "python profilingCallsCacheHM.py " + profiles + " " +  videos + " " +  nFs + " " +  QPs + " " +  sRanges + " " +  size_L1 + " " +  size_Ll + " " +  ass_L1 + " " +  ass_Ll + " " +  cache_word + " " + timeDef
        
        print "callHM: " + callHM
        os.system(callHM)
        callPie = "python pie.py " + timeDef
        os.system(callPie)
       
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle('MAP-HEVC');
    window.show()
    sys.exit(app.exec_())
