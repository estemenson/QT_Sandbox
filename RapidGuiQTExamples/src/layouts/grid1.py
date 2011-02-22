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
        #self.grabGesture(Qt.SwipeGesture)
        #self.grabGesture(Qt.PanGesture)
        #self.grabGesture(Qt.PinchGesture)
        self.initUI()
        self.my_touch_points = {} #keep track of each scribble
        self.current_touch_Id = None
        self.current_touch_index = 0
#        self.resetMatrix()
#    def resetMatrix(self):
#        self._matrix = QMatrix()
#        self._delta = QPointF()#self.width()/2,self.height()/2)
#        self.rotationAngle = 0.0
#        self.scaleFactor = self.currentStepScaleFactor = 1
#        self._matrix.translate(self._delta.x(), self._delta.y())
#        self._matrix.rotate(self.rotationAngle)
#        self._matrix.scale(self.currentStepScaleFactor * self.scaleFactor,\
#                           self.currentStepScaleFactor * self.scaleFactor)
        
    def initUI(self):

        self.setWindowTitle('grid layout')
        grid = QGridLayout()
        #=======================================================================
        # for i in names:
        #    button = QtGui.QPushButton(i)
        #    if j == 2:
        #        grid.addWidget(QtGui.QLabel(''), 0, 2)
        #    else: grid.addWidget(button, pos[j][0], pos[j][1])
        #    j = j + 1
        #=======================================================================
        self.setLayout(grid)

    def event(self,event):
        try:
            type = event.type()
            if type == QEvent.Gesture:
                return self.gestureEvent(event)
            if type == QEvent.TouchBegin:
                self.current_touch_Id = uuid.uuid1()
                self.my_touch_points[self.current_touch_Id] =\
                                                [event.touchPoints()[0].pos()]
                return True
            if type == QEvent.TouchUpdate:
                self.my_touch_points[self.current_touch_Id].append(\
                        event.touchPoints()[++self.current_touch_index].pos())
                return True
            if type == QEvent.TouchEnd:
                self.my_touch_points[self.current_touch_Id].append(\
                        event.touchPoints()[++self.current_touch_index].pos())
                self.current_touch_index = 0
                return True
            return QWidget.event(self, event)
        finally:
            self.update()
#    def gestureEvent(self, e):
#        if e.gesture(Qt.PanGesture):
#            self.panTriggered(e.gesture(Qt.PanGesture))
#        elif e.gesture(Qt.SwipeGesture):
#            self.swipeTriggered(e.gesture(Qt.SwipeGesture))
#        elif e.gesture(Qt.PinchGesture):
#            self.pinchTriggered(e.gesture(Qt.PinchGesture))
#        return True
#    def panTriggered(self,gesture):
#        if (gesture.state() == Qt.GestureFinished):
#            print('Pan gestured finished!!')
#            self._delta = gesture.delta()
##            for v in self.my_touch_points.values():
##                for i in v:
##                    i *= self._delta 
#            self.update()
#    def pinchTriggered(self,gesture):
#        changeFlags = gesture.changeFlags();
#        if changeFlags & QPinchGesture.RotationAngleChanged:
#            value = gesture.property("rotationAngle").toReal()[0]
#            lastValue = gesture.property("lastRotationAngle").toReal()[0]
#            self.rotationAngle += value - lastValue
#            print('Rotation: %f' % self.rotationAngle)
##        if (changeFlags & QPinchGesture.ScaleFactorChanged):
##            value = gesture.property("scaleFactor").toReal()[0]
##            self.currentStepScaleFactor = value
##            self.scaleFactor *= self.currentStepScaleFactor
##            print('Scale: %f' % self.scaleFactor)
#        if (gesture.state() == Qt.GestureFinished):
#            print('Pinch gesture finished!!')
#            self.resetMatrix()
##            self._delta = QPointF()
##            self.rotationAngle = 0.0
##            self.scaleFactor = self.currentStepScaleFactor = 1
#        self.update()
#p.translate(ww/2, wh/2);
#p.translate(horizontalOffset, verticalOffset);
#p.rotate(rotationAngle);
#p.scale(currentStepScaleFactor * scaleFactor, currentStepScaleFactor * scaleFactor);
#p.translate(-iw/2, -ih/2);
#p.drawImage(0, 0, currentImage)

#    def swipeTriggered(self, gesture):
#        if (gesture.state() == Qt.GestureFinished):
#            if gesture.horizontalDirection() == QSwipeGesture.Left\
#                    or gesture.verticalDirection() == QSwipeGesture.Up:
#                print('Swipe up or left')
#            else:
#                print('Swipe down or right')
#        self.update()

#    def resizeEvent(self, e):
#        self.update()
 
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        size = self.size()
#        self._matrix.translate(self._delta.x(), self._delta.y())
#        self._matrix.rotate(self.rotationAngle)
#        self._matrix.scale(self.currentStepScaleFactor * self.scaleFactor,\
#                           self.currentStepScaleFactor * self.scaleFactor)
#            mat.rotate(45)
#            mat.scale(self._delta.x(), self._delta.y())
#        qp.setMatrix(self._matrix)
        
#        for pos in self.my_touch_points:
#            qp.drawPoint(pos)
        for k in self.my_touch_points.keys():
            qp.drawPolyline(*self.my_touch_points[k])
#        if self.my_touch_points:
#            qp.drawPolyline(*self.my_touch_points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = Example()
    ex.resize(500,500)
    ex.show()
    sys.exit(app.exec_())
