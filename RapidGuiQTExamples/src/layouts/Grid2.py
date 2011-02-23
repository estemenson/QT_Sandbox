'''
Created on 2011-02-18

@author: hotsoft
'''
import sys
#from PyQt4 import QtCore
from PyQt4.QtCore import QEvent, QPointF, Qt
from PyQt4.QtGui import (QWidget, QGridLayout, QApplication, QTouchEvent,\
    QGestureEvent, QPainter, QSwipeGesture, QPanGesture, QMatrix,\
    QPinchGesture, QSpacerItem)
import uuid
TOUCH_ACCURACY = 50
ROW_OR_COLUMN_RANGE = 20
ROW = 'row'
COLUMN = 'column'
class Example(QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.grabGesture(Qt.PanGesture)
        self.initUI()
        self.my_touch_points = {} #keep track of each scribble
        self.current_touch_Id = None
        self.panningDirection = []
        
    def initUI(self):

        self.setWindowTitle('grid layout')
        self.grid = QGridLayout()
        self.setLayout(self.grid)

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
                return self.createNewRowOrColum(id)
            return QWidget.event(self, event)
        finally:
            self.update()
    def createNewRowOrColum(self,id):
        try:
            for t in self.my_touch_points[id].keys():
                k = self.my_touch_points[id][t]
                #check the first and last points to see if is a column or a row
                firstPoint = k[0]
                lastPoint = k[len(k) -1]
                width = lastPoint.x() - firstPoint.x()
                height = firstPoint.y() - lastPoint.y()
                w = self.width() - abs(width)
                print('width diff = %f' % w)
                h = self.height() - abs(height)
                print('height diff = %f' % h)
                avgY = (firstPoint.y() + lastPoint.y())/2.
                avgX = (firstPoint.x() + lastPoint.x())/2.
                if self.isRowOrColumn(w, avgY, width, k, ROW):
                    pass
                elif self.isRowOrColumn(h, avgX, height, k, COLUMN):
                    pass
#                if w <= TOUCH_ACCURACY:
#                    #now check the y value of each point in this gesture is with is
#                    #plus or minus 20 points
#                    row = True
#                    avgY = (firstPoint.y() + lastPoint.y())/2.
#                    for p in k:
#                        _h = avgY - p.y()
#                        if abs(_h) > ROW_OR_COLUMN_RANGE:
#                            print('Not a row, diff on y axis is too large: %f'\
#                                  % _h)
#                            row = False
#                    if row and width < 0:
#                        print('This is a row created from right to left')
#                        self.newRow()
#                    else:
#                        print('This is a row created from left to right')
#                elif h <= TOUCH_ACCURACY:
#                    #now check the x value of each point in this gesture is 
#                    #within plus or minus 20 points
#                    avgX = (firstPoint.x() + lastPoint.x())/2.
#                    col = True
#                    for p in k:
#                        _w = avgX - p.x()
#                        if abs(_w) > ROW_OR_COLUMN_RANGE:
#                            print(\
#                                'Not a column, diff on x axis is too large: %f'\
#                                % _w)
#                            col = False
#                    if col and height < 0:
#                        print('This is a column created from top to bottom')
#                    else:
#                        print('This is a column created from Bottom to top')
#                         
#                    
#                if firstPoint is not lastPoint:
#                    if firstPoint.x() <= TOUCH_ACCURACY and\
#                       lastPoint.x() >= self.width() - TOUCH_ACCURACY:
#                        #this is a row
#                        print('This is a row created from left to right')
#                    if firstPoint.x() >= self.width() - TOUCH_ACCURACY and\
#                       lastPoint.x() <= TOUCH_ACCURACY:
#                        print('This is a row created from right to left')
#                        
#                self.my_touch_points[id][t.id()].append(t.pos())
        finally:
            return True
    def isRowOrColumn(self, dif, avg, len, l_points, type):
        ret = False
        func = 'y' if type is ROW else 'x'
        if dif <= TOUCH_ACCURACY:
            #now check the dim value of each point in this gesture is 
            #within plus or minus 20 points
            ret = True
            for p in l_points:
                _h = avg - p.__getattribute__(func)()
                if abs(_h) > ROW_OR_COLUMN_RANGE:
                    print('Not a row or column diff on axis is too large: %f'\
                          % _h)
                    ret = False
            if ret:
                print('This is a %s' % type)
                self.newRow()
        return ret
        
    def gestureEvent(self, e):
        l_gestures = e.activeGestures()
        print('Got a gesture!!')
        if e.gesture(Qt.PanGesture):
            self.panTriggered(e.gesture(Qt.PanGesture))
#        for g in l_gestures:
#            gg = e.gesture(Qt.PanGesture)
#            if isinstance(g, gg):
#                self.panTriggered(g)
#        elif e.gesture(Qt.SwipeGesture):
#            self.swipeTriggered(e.gesture(Qt.SwipeGesture))
#        elif e.gesture(Qt.PinchGesture):
#            self.pinchTriggered(e.gesture(Qt.PinchGesture))
        return True
    def panTriggered(self,gesture):
        state = gesture.state()
        if state == Qt.GestureStarted:
            pass#self.panningDirection.append(gesture.)
        if ( state == Qt.GestureFinished):
            print('Pan gestured finished!!')
#            spacer = QSpacerItem()
#            self.grid.addItem(QLayoutItem, int, int, rowSpan=1, columnSpan=1, alignment=0)
            #self._delta = gesture.delta()
            
#            for v in self.my_touch_points.values():
#                for i in v:
#                    i *= self._delta 
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
