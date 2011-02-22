'''
Created on Feb 21, 2011

@author: stevenson
'''

class ScribbleArea(QWidget):
    def __init__(self, **kwargs):
        super(ScribbleArea,self).__init__(**kwargs)
        self.setAttribute(Qt.WA_AcceptTouchEvents);
        self.setAttribute(Qt.WA_StaticContents);
        self.modified = false;
        self.image = None
    
        self.myPenColors = [QColor("green"), QColor("purple"), QColor("red"), 
                            QColor("blue"), QColor("yellow"), QColor("pink"),
                            QColor("orange"), QColor("brown"), QColor("grey"),
                            QColor("black")]

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return false
    
        QSize newSize = loadedImage.size().expandedTo(size())
        resizeImage(&loadedImage, newSize)
        self.image = loadedImage
        self.modified = false
        self.update()
        return true;

    def saveImage(self, fileName, fileFormat):
        QImage visibleImage = self.image
        resizeImage(visibleImage, self.size())
    
        if (visibleImage.save(fileName, fileFormat)) {
            self.modified = false;
            return true;
        } else {
            return false;
        }

    def clearImage(self):
        self.image.fill(qRgb(255, 255, 255));
        self.modified = true;
        update();

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = event.rect()
        painter.drawImage(rect.topLeft(), self.image, rect);

    def resizeEvent(self,event):
        if (width() > image.width() || height() > image.height()) {
            int newWidth = qMax(width() + 128, image.width());
            int newHeight = qMax(height() + 128, image.height());
            resizeImage(&image, QSize(newWidth, newHeight));
            update();
        return super(ScribbleArea,self).resizeEvent(event);

    def resizeImage(image, newSize):
        if (image->size() == newSize)
            return;
    
        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image);
        image = newImage;

    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
    
        printDialog = QPrintDialog(self, printer)
        if (printDialog.exec() == QDialog.Accepted):
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(),size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)

    def event(event):
    type = event.type()
    if type in [QEvent.TouchBegin, QEvent.TouchUpdate, QEvent.TouchEnd]
        touchPoints = event.touchPoints()
        for touchPoint in touchPoints:
            state = touchPoint.state()
            case Qt.TouchPointStationary:
                // don't do anything if this touch point hasn't moved
                continue;
            default:
                {
                    QRectF rect = touchPoint.rect();
                    if (rect.isEmpty()) {
                        qreal diameter = qreal(50) * touchPoint.pressure();
                        rect.setSize(QSizeF(diameter, diameter));
                    }

                    QPainter painter(&image);
                    painter.setPen(Qt.NoPen);
                    painter.setBrush(myPenColors.at(touchPoint.id() % myPenColors.count()));
                    painter.drawEllipse(rect);
                    painter.end();

                    modified = true;
                    int rad = 2;
                    update(rect.toRect().adjusted(-rad,-rad, +rad, +rad));
                }
                break;
            }
        }
        break;
    }
    return QWidget.event(event);

if __name__ == '__main__':
    pass