#
#  IAImageViewInteractive.py
#  ImageAlpha
#
#  Created by porneL on 27.wrzenia.08.
#  Copyright (c) 2008 Lyncroft. All rights reserved.
#
from objc import *
from Foundation import *
from AppKit import *
from IAImageView import IAImageView
from  math import floor

class IAImageViewInteractive(IAImageView):
    def initWithFrame_(self, frame):
        self = super(IAImageView, self).initWithFrame_(frame)       
        if self:
            # initialization code here
            types = [NSFilenamesPboardType]
            types.append(NSImage.imagePasteboardTypes())
            self.registerForDraggedTypes_(types);
            pass
        return self
    
    controller = objc.IBOutlet()        
                            
    mouseIsDown = False
    dragBackground = False
    dragStart = (0,0)

    def awakeFromNib(self):
        pass

    def draggingEntered_(self,sender):
        if self.controller.canSetDocumentImageFromPasteboard_(sender.draggingPasteboard()):
            self.imageFade = 0.85
            self.setNeedsDisplay_(YES)
            return NSDragOperationCopy | NSDragOperationGeneric | NSDragOperationMove
        
    def draggingExited_(self,sender):
        self.imageFade = 1.0
        self.setNeedsDisplay_(YES)

    def prepareForDragOperation_(self,sender):
        self.imageFade = 1.0
        self.setNeedsDisplay_(YES)
        return self.controller.canSetDocumentImageFromPasteboard_(sender.draggingPasteboard())
        
    def performDragOperation_(self,sender):
        return self.controller.setDocumentImageFromPasteboard_(sender.draggingPasteboard())
        
    def resetCursorRects(self):
        if self.image is not None or self.backgroundRenderer is not None:
            curs = NSCursor.closedHandCursor() if self.mouseIsDown else NSCursor.openHandCursor()
            self.addCursorRect_cursor_(self.visibleRect(), curs)
            curs.setOnMouseEntered_(YES)
    
    def scrollWheel_(self,event):
        if event.deltaY() > 0:
            self.increaseZoom()
        elif event.deltaY() < 0:
            self.decreaseZoom()

    def mouseExited_(self,event):
        self.imageFade=1.0
        self.setNeedsDisplay_(YES)

    def mouseEntered_(self,event):
        self.imageFade = 0.5
        self.setNeedsDisplay_(YES)

    def pointIsInImage_(self,point):
        if self.image is None: return NO
        size = self.image.size();
        
        fsize = self.frame().size;
        w = max(50,size.width * self.zoom +15) / 2  # add "border" around image to ease dragging of small ones
        h = max(50,size.height * self.zoom +15) / 2
        
        return point.x >= self.imageOffset[0]+fsize.width/2-w and point.y >= self.imageOffset[1]+fsize.height/2-h and \
               point.x <= self.imageOffset[0]+fsize.width/2+w and point.y <= self.imageOffset[1]+fsize.height/2+h

    def mouseDragged_(self,event):
        point = self.convertPoint_fromView_(event.locationInWindow(), None);
        delta = (point.x - self.dragStart[0], point.y - self.dragStart[1])
        self.dragStart = (point.x, point.y)                 
        if self.backgroundRenderer is not None and self.dragBackground:
            self.backgroundRenderer.moveBy_(delta)      
        elif self.image is not None:
            size = self.frame().size    
            self.imageOffset = (self.imageOffset[0] + delta[0],
                                self.imageOffset[1] + delta[1])
            self._limitImageOffset()        
            
        self.setNeedsDisplay_(YES)
        
    def mouseChange_(self, isDown):
        self.mouseIsDown = isDown
        self.window().invalidateCursorRectsForView_(self);

    def mouseDown_(self,event):
        point = self.convertPoint_fromView_(event.locationInWindow(), None)
        
        if self.backgroundRenderer is None or not self.backgroundRenderer.canMove(): 
            self.dragBackground = False
        else:
            self.dragBackground = not self.pointIsInImage_(point)
            if (event.modifierFlags() & (NSShiftKeyMask | NSAlternateKeyMask | NSCommandKeyMask)):
                self.dragBackground = not self.dragBackground
        
        
        self.dragStart = (point.x,point.y)
        if event.clickCount()&3==2:
            self.imageOffset = (0,0)
            if self.zoomingToFill:
                self.setZoom_(1)
            else:
                self.zoomToFill()
            self.setNeedsDisplay_(YES)
        else:   
            self.mouseChange_(YES);
            self.mouseDragged_(event)
                        
    def magnifyWithEvent_(self, event):
        NSLog("magnified by %f z = %f" % (event.magnification(), self.zoom));
        
        oldzoom = self.zoom;
        # zoom < 1 requires different zooming speed than > 1
        if (oldzoom + event.magnification() > 1):
            zoom = ((oldzoom / 20) + event.magnification()/4) * 20;
        else:
            zoom = 1 / (1/oldzoom - event.magnification());

        # avoid crossing of the 1.0 boundary at wrong speed
        if (zoom > 1.0 and oldzoom < 1.0) or (zoom < 1.0 and oldzoom > 1.0):
            zoom = 1.0;

        self.setZoom_(max(0.25,zoom));
    
    def keyDown_(self,event):
        NSLog("key! %s" % event);
    
    def mouseUp_(self,event):
        self.mouseChange_(NO);        

    def updateTouches_(self,event):
        touches = event.touchesMatchingPhase_inView_( NSTouchPhaseStationary, self);
        NSLog("touches %s" % touches.allObjects());
        self.drawAlternateImage = (touches.count() >= 3);
        self.setNeedsDisplay_(YES)
    
    def otherMouseDown_(self,event):
        self.drawAlternateImage = YES
        self.setNeedsDisplay_(YES)
                
    def otherMouseUp_(self,event):
        self.drawAlternateImage = NO
        self.setNeedsDisplay_(YES)
        
