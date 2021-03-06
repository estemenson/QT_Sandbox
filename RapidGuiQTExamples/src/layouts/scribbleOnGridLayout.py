'''
Created on 2011-02-18

@author: hotsoft
'''
import sys
#from PyQt4 import QtCore
from PyQt4.QtCore import (QEvent, Qt, QPointF)
from PyQt4.QtGui import (QWidget, QGridLayout, QApplication, QTouchEvent, QGestureEvent, QPainter, QSwipeGesture, QPanGesture, QMatrix, QPinchGesture)
import uuid
class Example(QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.initUI()
        self.my_touch_points = {} #keep track of each scribble
        self.current_touch_Id = None
        
    def initUI(self):

        self.setWindowTitle('grid layout')
        grid = QGridLayout()
        self.setLayout(grid)

    def event(self,event):
        try:
            type = event.type()
            if type == QEvent.Gesture:
                return self.gestureEvent(event)
            if type == QEvent.TouchBegin:
                id = self.current_touch_Id = uuid.uuid1()
                t = event.touchPoints()[0]
                self.my_touch_points[id]={t.id():[t.pos()]}
                return True
            if type == QEvent.TouchUpdate:
                id = self.current_touch_Id
                for t in event.touchPoints():
                    if t.id() not in self.my_touch_points[id]:
                        self.my_touch_points[id][t.id()] = []
                    self.my_touch_points[id][t.id()].append(t.pos())
                return True
            if type == QEvent.TouchEnd:
                id = self.current_touch_Id
                for t in event.touchPoints():
                    self.my_touch_points[id][t.id()].append(t.pos())
                return True
            return QWidget.event(self, event)
        finally:
            self.update()
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
        qp.setPen(Qt.red)
#        size = self.size()
        for k in self.my_touch_points.keys():
            for k1 in self.my_touch_points[k].keys():
                qp.drawPolyline(*self.my_touch_points[k][k1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = Example()
    ex.resize(500,500)
    ex.show()
    sys.exit(app.exec_())
