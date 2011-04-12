'''
Created on 2011-02-18

@author: hotsoft
'''
import sys
#from PyQt4 import QtCore
from PyQt4.QtCore import QEvent, QPointF, Qt, QLineF
from PyQt4.QtGui import (QWidget, QGridLayout, QApplication, QTouchEvent,\
    QGestureEvent, QPainter, QSwipeGesture, QPanGesture, QMatrix,\
    QPinchGesture, QSpacerItem, QTableWidget, QTableWidgetItem, QBoxLayout, 
    QLabel,QFrame)
import uuid
from layouts.borderlayout import BorderLayout
TOUCH_ACCURACY = 50
ROW_OR_COLUMN_RANGE = 20
ROW = 'row'
COLUMN = 'column'
class Scribble1(QWidget):
  
    def __init__(self):
        super(Scribble1, self).__init__()
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.grabGesture(Qt.PanGesture)
        self.initUI()
        self.my_touch_points = {} #keep track of each scribble
        self.current_touch_Id = None
        self.panningDirection = []
        
    def initUI(self):

        self.setWindowTitle('Scribble1 layout')
#        self.grid = QGridLayout()
#        self.setLayout(self.grid)

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
                    self.newRow(avgX,avgY)
                elif self.isRowOrColumn(h, avgX, height, k, COLUMN):
                    self.newCol(avgX,avgY)
        finally:
            return True
    def newRow(self, x,y):
        pass#self.grid.cellRect(x, y)
    def isRowOrColumn(self, dif, avg, len, l_points, type):
        ret = False
        func = 'y' if type is ROW else 'x'
        if dif <= TOUCH_ACCURACY:
            #now check the dif value against each point in this gesture to make 
            #sure they are within plus or minus 20 points
            ret = True
            for p in l_points:
                #check that the average - (p.y() for rows or p.x() for columns)
                #is within the allowable variance if not we return false
                _h = avg - p.__getattribute__(func)()
                if abs(_h) > ROW_OR_COLUMN_RANGE:
                    ret = False
                    break
        return ret
        
    def gestureEvent(self, e):
        #l_gestures = e.activeGestures()
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
class Scribble2(QWidget,QTableWidgetItem):
  
    def __init__(self, *parent, **kwargs):
        super(Scribble2, self).__init__(*parent, **kwargs)
        self.drawBorder = kwargs.get('drawBorder')
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.grabGesture(Qt.PanGesture)
        self.initUI()
        self.my_touch_points = {} #keep track of each scribble
        self.current_touch_Id = None
        self.panningDirection = []
        
    def initUI(self):

        self.setWindowTitle('Scribble1 layout')
#        self.grid = QGridLayout()
#        self.setLayout(self.grid)

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
                    self.newRow(avgX,avgY)
                elif self.isRowOrColumn(h, avgX, height, k, COLUMN):
                    self.newCol(avgX,avgY)
        finally:
            return True
    def newRow(self, x,y):
        pass#self.grid.cellRect(x, y)
    def isRowOrColumn(self, dif, avg, len, l_points, type):
        ret = False
        func = 'y' if type is ROW else 'x'
        if dif <= TOUCH_ACCURACY:
            #now check the dif value against each point in this gesture to make 
            #sure they are within plus or minus 20 points
            ret = True
            for p in l_points:
                #check that the average - (p.y() for rows or p.x() for columns)
                #is within the allowable variance if not we return false
                _h = avg - p.__getattribute__(func)()
                if abs(_h) > ROW_OR_COLUMN_RANGE:
                    ret = False
                    break
        return ret
        
    def gestureEvent(self, e):
        #l_gestures = e.activeGestures()
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
        if self.drawBorder:
            self.drawTheBorder(qp)
        qp.end()
        
    def drawTheBorder(self, qp):
        qp.setPen(Qt.blue)
        qp.drawRect(0,0, self.width(), self.height())
    def drawPoints(self, qp):
        qp.setPen(Qt.red)
#        size = self.size()
        for k in self.my_touch_points.keys():
            for k1 in self.my_touch_points[k].keys():
                qp.drawPolyline(*self.my_touch_points[k][k1])
class MyGrid(QWidget, QGridLayout):
    def __init__(self,**kwargs):
        super(MyGrid,self).__init__(**kwargs)
        super(QGridLayout,self).__init__()
class Grid2(QWidget):
    def __init__(self):
        super(Grid2, self).__init__()
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.grabGesture(Qt.PanGesture)
        self.initUI()
        self.my_touch_points = {} #keep track of each scribble
        self.current_touch_Id = None
        self.panningDirection = []
        self.rows = []
        self.columns = []
        
    def initUI(self):

        self.setWindowTitle('Grid2 layout')
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
                    self.newRow(avgX,avgY)
                elif self.isRowOrColumn(h, avgX, height, k, COLUMN):
                    self.newCol(avgX,avgY)
                del self.my_touch_points[id]
        finally:
            return True
    def newRow(self, x,y):
        self.rows.append(QLineF(0, y, self.width(), y))
    def newCol(self, x,y):
        self.columns.append(QLineF(x, 0, x,self.height()))
    def isRowOrColumn(self, dif, avg, len, l_points, type):
        ret = False
        func = 'y' if type is ROW else 'x'
        if dif <= TOUCH_ACCURACY:
            #now check the dif value against each point in this gesture to make 
            #sure they are within plus or minus 20 points
            ret = True
            for p in l_points:
                #check that the average - (p.y() for rows or p.x() for columns)
                #is within the allowable variance if not we return false
                _h = avg - p.__getattribute__(func)()
                if abs(_h) > ROW_OR_COLUMN_RANGE:
                    ret = False
                    break
        return ret
        
    def gestureEvent(self, e):
        #l_gestures = e.activeGestures()
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
        if self.rows or self.columns:
            self.drawGrid(qp)
        qp.end()
    def drawGrid(self, qp):
        for row in self.rows:
            qp.drawLine(row)
        for col in self.columns:
            qp.drawLine(col)
    def drawPoints(self, qp):
        qp.setPen(Qt.red)
#        size = self.size()
        for k in self.my_touch_points.keys():
            for k1 in self.my_touch_points[k].keys():
                qp.drawPolyline(*self.my_touch_points[k][k1])
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = Grid2()#Scribble1()
    ex.resize(1000,1000)
    ex.show()
    sys.exit(app.exec_())
