'''
Created on Feb 24, 2011

@author: stevenson
'''

from PyQt4.QtCore import Qt, QSize, SIGNAL, SLOT, pyqtSlot
from PyQt4.QtGui import (QGridLayout, QApplication, QDialog, QLayout,
                         QMessageBox,QGroupBox,QSpinBox,QSlider,QDial,
                         QProgressBar,QLabel,QComboBox,QDialogButtonBox)
import sys


class DynamicLatout(QDialog):
    def __init__(self):
        super(DynamicLatout, self).__init__()
        self.rotableWidgets = []
        self.createRotableGroupBox()
        self.createOptionsGroupBox()
        self.createButtonBox()
    
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.rotableGroupBox, 0, 0)
        self.mainLayout.addWidget(self.optionsGroupBox, 1, 0)
        self.mainLayout.addWidget(self.buttonBox, 2, 0)
        self.setLayout(self.mainLayout)
    
        self.mainLayout.setSizeConstraint(QLayout.SetMinimumSize)
    
        self.setWindowTitle("Dynamic Layouts")
    
    @pyqtSlot(int, name='buttonsOrientationChanged')
    def buttonsOrientationChanged(self, index):
        self.mainLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.setMinimumSize(0, 0)
        orientation = Qt.Orientation(
                    self.buttonsOrientationComboBox.itemData(index).toInt()[0])
    
        if orientation == self.buttonBox.orientation():
            return
    
        self.mainLayout.removeWidget(self.buttonBox)
    
        spacing = self.mainLayout.spacing()
    
        oldSizeHint = self.buttonBox.sizeHint() + QSize(spacing, spacing)
        self.buttonBox.setOrientation(orientation)
        newSizeHint = self.buttonBox.sizeHint() + QSize(spacing, spacing)
    
        if orientation == Qt.Horizontal:
            self.mainLayout.addWidget(self.buttonBox, 2, 0)
            self.resize(self.size() + QSize(-oldSizeHint.width(), newSizeHint.height()))
        else:
            self.mainLayout.addWidget(self.buttonBox, 0, 3, 2, 1)
            self.resize(self.size() + QSize(newSizeHint.width(), -oldSizeHint.height()))
    
        self.mainLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

    @pyqtSlot(name='rotateWidgets')
    def rotateWidgets(self):
        assert(len(self.rotableWidgets) % 2 == 0)
    
        for widget in self.rotableWidgets:
            self.rotableLayout.removeWidget(widget)
    
        self.rotableWidgets.insert(0, self.rotableWidgets.pop())
    
        n = len(self.rotableWidgets)
        i = 0
        while i < n / 2:
            self.rotableLayout.addWidget(self.rotableWidgets[n - i - 1], 0, i)
            self.rotableLayout.addWidget(self.rotableWidgets[i], 1, i)
            i += 1
         

    @pyqtSlot(name='help')
    def help(self):
        QMessageBox.information(self, "Dynamic Layouts Help",
                                "This example shows how to change layouts "
                                   "dynamically.")
    def createRotableGroupBox(self):
        self.rotableGroupBox = QGroupBox("Rotable Widgets")
    
        self.rotableWidgets.append(QSpinBox())  
        self.rotableWidgets.append(QSlider())
        self.rotableWidgets.append(QDial())
        self.rotableWidgets.append(QProgressBar())
        n = len(self.rotableWidgets)
        i = 0
        while i < n:
            self.connect(self.rotableWidgets[i], SIGNAL("valueChanged(int)"),
                         self.rotableWidgets[(i + 1) % n],SLOT("setValue(int)"))
            i += 1
        
        self.rotableLayout = QGridLayout()
        self.rotableGroupBox.setLayout(self.rotableLayout)
    
        self.rotateWidgets()

    def createOptionsGroupBox(self):
        self.optionsGroupBox = QGroupBox("Options")
    
        self.buttonsOrientationLabel = QLabel("Orientation of buttons:")
    
        self.buttonsOrientationComboBox = QComboBox()
        self.buttonsOrientationComboBox.addItem("Horizontal", Qt.Horizontal)
        self.buttonsOrientationComboBox.addItem("Vertical", Qt.Vertical)
    
        self.connect(self.buttonsOrientationComboBox, 
                     SIGNAL("currentIndexChanged(int)"),
                     SLOT("buttonsOrientationChanged(int)"))
    
        self.optionsLayout = QGridLayout()
        self.optionsLayout.addWidget(self.buttonsOrientationLabel, 0, 0)
        self.optionsLayout.addWidget(self.buttonsOrientationComboBox, 0, 1)
        self.optionsLayout.setColumnStretch(2, 1)
        self.optionsGroupBox.setLayout(self.optionsLayout)

    def createButtonBox(self):
        self.buttonBox = QDialogButtonBox()
    
        self.closeButton = self.buttonBox.addButton(QDialogButtonBox.Close)
        self.helpButton = self.buttonBox.addButton(QDialogButtonBox.Help)
        self.rotateWidgetsButton = self.buttonBox.addButton("Rotate &Widgets",
                                                    QDialogButtonBox.ActionRole)
    
        self.connect(self.rotateWidgetsButton, SIGNAL("clicked()"), self, 
                     SLOT("rotateWidgets()"))
        self.connect(self.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.helpButton,SIGNAL("clicked()"),self, SLOT("help()"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dl = DynamicLatout()
    dl.resize(500, 500)
    dl.show()
    sys.exit(app.exec_())

