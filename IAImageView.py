#
#  IAImageView.py
#  ImageAlpha
#
#  Created by porneL on 21.wrzenia.08.
#  Copyright (c) 2008 Lyncroft. All rights reserved.
#

from objc import *
from Foundation import *
from AppKit import *
from math import ceil, floor

class IAImageView(NSView):
    zoom = 2.0
    image = None
    alternateImage = None
    drawAlternateImage = NO
    backgroundRenderer = None
    smooth = YES
    backgroundOffset = (0,0)
    imageOffset = (0,0)
    imageFade = 1.0
    zoomingToFill = 0

    def setFrame_(self,rect):
        NSView.setFrame_(self,rect)
        if self.zoomingToFill: self.zoomToFill(self.zoomingToFill)

    def increaseZoom(self):
        self.setZoom_(self.zoom * 2.0);
        
    def decreaseZoom(self):
        self.setZoom_(self.zoom / 2.0);
    
    def zoomToFill(self, zoom=1.0):
        self.zoomingToFill = zoom
        if self.image is None: return
        size = self.image.size()
        framesize = self.frame().size
        zoom = min(framesize.width/size.width, framesize.height/size.height)*self.zoomingToFill
        if zoom > 1.0:
            zoom = min(4.0,floor(zoom))
        self._setZoom(zoom)
    
    def _limitImageOffset(self):
        if self.image is None: return
        size = self.frame().size
        imgsize = self.image.size()
        
        w = (size.width + imgsize.width * self.zoom) /2
        h = (size.height + imgsize.height * self.zoom) /2
        
        self.imageOffset = (max(-w+15, min(w-15, self.imageOffset[0])), \
                            max(-h+15, min(h-15, self.imageOffset[1])))

    def setSmooth_(self,smooth):
        self.smooth = smooth
        NSGraphicsContext.currentContext().setImageInterpolation_(NSImageInterpolationHigh if smooth else NSImageInterpolationNone)
        self.setNeedsDisplay_(YES)

    def setZoom_(self,zoom):
        self.zoomingToFill = 0
        self._setZoom(zoom);
    
    def _setZoom(self,zoom):
        self.zoom = min(16.0,max(1.0/128.0,zoom))
        self._limitImageOffset()
        self.setNeedsDisplay_(YES)      

    def setImage_(self,aImage):
        self.image=aImage
        if self.zoomingToFill: self.zoomToFill(self.zoomingToFill)
        self.setNeedsDisplay_(YES)  

    def setAlternateImage_(self,aImage):
        self.alternateImage = aImage
        self.setNeedsDisplay_(YES)

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
        
        image = self.image if not self.drawAlternateImage else self.alternateImage;
        if image is None: return
		
        unscaled = abs(self.zoom - 1.0) < 0.01;
        
        NSGraphicsContext.currentContext().setImageInterpolation_(NSImageInterpolationHigh if self.smooth and not unscaled else NSImageInterpolationNone)
        
        frame = self.frame();
        imgsize = image.size()
        offx = (frame.size.width  - imgsize.width * self.zoom )/2 + self.imageOffset[0] 
        offy = (frame.size.height - imgsize.height * self.zoom )/2 + self.imageOffset[1]
        
        x = (rect.origin.x - offx) / self.zoom
        y = (rect.origin.y - offy) / self.zoom
        
        if unscaled:
            x = ceil(x)
            y = ceil(y)
        
        imgrect = ((x,y), (rect.size.width / self.zoom, rect.size.height / self.zoom));
        image.drawInRect_fromRect_operation_fraction_(rect, imgrect, NSCompositeSourceOver, self.imageFade)

