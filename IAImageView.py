#
#  IAImageView.py

from objc import *
from Foundation import *
from AppKit import *
from math import ceil, floor

class IAImageView(NSView):
    _zoom = 2.0
    _image = None
    _alternateImage = None
    _drawAlternateImage = NO
    backgroundRenderer = None
    _smooth = YES
    backgroundOffset = (0,0)
    imageOffset = (0,0)
    imageFade = 1.0
    zoomingToFill = 0

    def setFrame_(self,rect):
        NSView.setFrame_(self,rect)
        if self.zoomingToFill: self.zoomToFill(self.zoomingToFill)

    @objc.IBAction
    def zoomIn_(self, sender):
        self.setZoom_(self.zoom() * 2.0);

    @objc.IBAction
    def zoomOut_(self,sender):
        self.setZoom_(self.zoom() / 2.0);

    def zoomToFill(self, zoom=1.0):
        self.zoomingToFill = zoom
        if self.image() is None: return
        size = self.image().size()
        framesize = self.frame().size
        zoom = min(framesize.width/size.width, framesize.height/size.height)*self.zoomingToFill
        if zoom > 1.0:
            zoom = min(4.0,floor(zoom))
        self._setZoom(zoom)

    def _limitImageOffset(self):
        if self.image() is None: return
        size = self.frame().size
        imgsize = self.image().size()

        w = (size.width + imgsize.width * self.zoom()) /2
        h = (size.height + imgsize.height * self.zoom()) /2

        self.imageOffset = (max(-w+15, min(w-15, self.imageOffset[0])), \
                            max(-h+15, min(h-15, self.imageOffset[1])))

    def smooth(self):
        return self._smooth;

    def setSmooth_(self,smooth):
        self._smooth = smooth
        NSGraphicsContext.currentContext().setImageInterpolation_(NSImageInterpolationHigh if smooth else NSImageInterpolationNone)
        self.setNeedsDisplay_(YES)

    def zoom(self):
        return self._zoom;

    def setZoom_(self,zoom):
        self.zoomingToFill = 0
        self._setZoom(zoom);

    def _setZoom(self,zoom):
        self._zoom = min(16.0,max(1.0/128.0,zoom))
        self._limitImageOffset()
        self.setNeedsDisplay_(YES)

    def image(self):
        return self._image;

    def setImage_(self,aImage):
        self._image=aImage
        if self.zoomingToFill: self.zoomToFill(self.zoomingToFill)
        self.setDrawAlternateImage_(NO)

    def alternateImage(self):
        return self._alternateImage;

    def setAlternateImage_(self,aImage):
        self._alternateImage = aImage
        self.setNeedsDisplay_(YES)

    def drawAlternateImage(self):
        return self._drawAlternateImage;

    def setDrawAlternateImage_(self,tf):
        self._drawAlternateImage = tf
        self.setNeedsDisplay_(YES)

    def drawAlternateImage(self):
        return self._drawAlternateImage == True

    def setBackgroundRenderer_(self,renderer):
        self.backgroundRenderer = renderer;
        self.setNeedsDisplay_(YES)

#    def initWithFrame_(self, frame):
#        self = super(IAImageView, self).initWithFrame_(frame)
#        if self:
#            # initialization code here
#            pass
#        return self

    def isOpaque(self):
        return self.backgroundRenderer is not None

    def drawRect_(self,rect):
        if self.backgroundRenderer is not None: self.backgroundRenderer.drawRect_(rect);

        image = self.image() if not self.drawAlternateImage() else self.alternateImage();
        if image is None: return

        unscaled = abs(self.zoom() - 1.0) < 0.01;

        NSGraphicsContext.currentContext().setImageInterpolation_(NSImageInterpolationHigh if self.smooth() and not unscaled else NSImageInterpolationNone)

        frame = self.frame();
        imgsize = image.size()
        offx = (frame.size.width  - imgsize.width * self.zoom() )/2 + self.imageOffset[0]
        offy = (frame.size.height - imgsize.height * self.zoom() )/2 + self.imageOffset[1]

        x = (rect.origin.x - offx) / self.zoom()
        y = (rect.origin.y - offy) / self.zoom()

        if unscaled:
            x = ceil(x)
            y = ceil(y)

        imgrect = ((x,y), (rect.size.width / self.zoom(), rect.size.height / self.zoom()));
        image.drawInRect_fromRect_operation_fraction_(rect, imgrect, NSCompositeSourceOver, self.imageFade)

