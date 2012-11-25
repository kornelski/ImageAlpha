#
#  IAImageView.py

from objc import *
from Foundation import *
from AppKit import *
from Quartz.CoreGraphics import *
from Quartz.QuartzCore import *
from math import ceil, floor

class IAImageView(NSView):
    _zoom = 2.0
    _lastZoom = -1
    _image = None
    _alternateImage = None
    _drawAlternateImage = NO
    backgroundRenderer = None
    _smooth = YES
    backgroundOffset = (0,0)
    imageOffset = (0,0)
    imageFade = 1.0
    zoomingToFill = 0

    _imageLayer = None
    _backgroundLayer = None

    def initWithFrame_(self, frame):
        self = super(IAImageView, self).initWithFrame_(frame)
        if self:

            self.setWantsLayer_(YES);
            if self.layer() is None: self.setLayer_(CALayer.layer());
            assert self.layer() is not None;

            bg = CALayer.layer();
            bg.setBackgroundColor_(CGColorCreateGenericRGB(0.5,0.5,0.5,1));
            self._backgroundLayer = CALayer.layer();
            self.layer().addSublayer_(self._backgroundLayer);

            self._imageLayer = CALayer.layer()
            self.layer().addSublayer_(self._imageLayer);

            NSLog("initing self with frame");

            self.addShadow();
        return self

    def addShadow(self):

        shadowHeight = 10;
        shadowWidth = 12;

        bounds = self.layer().bounds();
        NSLog("bounds %d %d %d %d",bounds.size.width, bounds.size.height, bounds.origin.x, bounds.origin.y);

        shadow1 = CAGradientLayer.layer();
        stops = [CGColorCreateGenericRGB(0,0,0,x) for x in [0, 0.04, 0.11, 0.3]]
        shadow1.setColors_(stops);
        shadow1.setAutoresizingMask_(kCALayerWidthSizable | kCALayerMinYMargin);
        shadow1.setFrame_(((0,bounds.size.height-shadowHeight), (bounds.size.width, shadowHeight)));

        shadow2 = CAGradientLayer.layer();
        stops.reverse();
        shadow2.setColors_(stops);
        shadow2.setStartPoint_((0,0));
        shadow2.setEndPoint_((1,0));
        shadow2.setAutoresizingMask_(kCALayerHeightSizable | kCALayerMaxXMargin);
        shadow2.setFrame_(((0,0),(shadowWidth,bounds.size.height)));
        self.layer().addSublayer_(shadow2);
        self.layer().addSublayer_(shadow1);
        self.shadow1 = shadow1;


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
        if self._imageLayer:
            self._imageLayer.setMagnificationFilter_(kCAFilterLinear if smooth else kCAFilterNearest)
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
        if self._alternateImage and aImage:
            self._setScale_ofImage_(self._getScaleOfImage_(self._alternateImage), aImage);
        if self.zoomingToFill:
            self.zoomToFill(self.zoomingToFill)
        self.setDrawAlternateImage_(NO)


    def _getScaleOfImage_(self, image):
        w,h = image.size()
        rep = image.representations();
        if not rep or not rep.count(): return (0,0);
        return (rep[0].pixelsWide()/w, rep[0].pixelsHigh()/h);

    def _setScale_ofImage_(self, scale, image):
        rep = image.representations();
        if not rep or not rep.count(): return (0,0);
        image.setSize_((rep[0].pixelsWide()/scale[0], rep[0].pixelsHigh()/scale[1]));

    def alternateImage(self):
        return self._alternateImage;

    def setAlternateImage_(self,aImage):
        if self._image and aImage:
            self._setScale_ofImage_(self._getScaleOfImage_(aImage), self._image);
        self._alternateImage = aImage
        self.imageOffset = (0,0)
        if not self.zoomingToFill:
            self.setZoom_(1.0)
        self.setNeedsDisplay_(YES)

    def drawAlternateImage(self):
        return self._drawAlternateImage;

    def setDrawAlternateImage_(self,tf):
        self._drawAlternateImage = tf
        if self._imageLayer:
            image = self.image() if not tf else self.alternateImage()
            CATransaction.begin()
            CATransaction.setDisableActions_(True)
            self._imageLayer.setContents_(image);
            self._updateLayerZoom()
            CATransaction.commit()

        self.setNeedsDisplay_(YES)

    def drawAlternateImage(self):
        return self._drawAlternateImage == True

    def setBackgroundLayer_(self, layer):
        if self.layer() is None: self.initWithFrame_(self.frame());
        layer.setFrame_(self.layer().bounds());
        layer.setAutoresizingMask_(kCALayerWidthSizable|kCALayerHeightSizable)
        self.layer().replaceSublayer_with_(self._backgroundLayer, layer);
        self._backgroundLayer = layer;

    def setBackgroundRenderer_(self,renderer):
        assert renderer is not None;
        self.backgroundRenderer = renderer;
        if self.layer():
            self.setBackgroundLayer_(renderer.getLayer())
        self.setNeedsDisplay_(YES)

    def isOpaque(self):
        return self.backgroundRenderer is not None

    def _updateLayerZoom(self):
        if self._lastZoom != self._zoom:
            image = self.image() if not self.drawAlternateImage() else self.alternateImage();
            if image is not None:
                w,h = image.size()
                x,y = self.imageOffset
                size = self.bounds()[1]
                self._imageLayer.setFrame_(((x+size[0]/2-w/2,y+size[1]/2-h/2),(w*self._zoom, h*self._zoom)));
                self._lastZoom = self._zoom

    def setNeedsDisplay_(self, tf):
        if tf:
            image = self.image() if not self.drawAlternateImage() else self.alternateImage();
            if image is not None:
                self._updateLayerZoom()

                self._imageLayer.setOpacity_(self.imageFade);

                x,y = self.imageOffset
                size = self.bounds()[1]

                CATransaction.begin()
                CATransaction.setDisableActions_(True)
                self._imageLayer.setPosition_((x+size[0]/2,y+size[1]/2))
                CATransaction.commit()

        super(IAImageView, self).setNeedsDisplay_(tf);

