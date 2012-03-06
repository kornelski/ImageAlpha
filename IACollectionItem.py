#
#  IACollectionItem.py

from Foundation import *
from objc import *
from AppKit import *
from random import randint
from IAImageView import IAImageView
from IAImageViewInteractive import IAImageViewInteractive
from IABackgroundRenderer import *

class IACollectionViewItem(NSCollectionViewItem):
    def setSelected_(self, sel):
        NSCollectionViewItem.setSelected_(self,sel)
        col = self.collectionView()
        if sel and col is not None:
            col.updateSelection()

    def imageChangedNotification_(self,sender):
        view = self.view()
        if view is not None:
            subview = view.viewWithTag_(1234);
            if subview is not None:
                subview.setImage_(sender.object().image);

class IACollectionImageView(IAImageView):
    collectionItem = None;
    drawBorder = False

    def initWithFrame_(self, frame):
        self = super(IACollectionImageView, self).initWithFrame_(frame)
        if self:
            # initialization code here
            types = [NSFilenamesPboardType]
            types.append(NSImage.imagePasteboardTypes())
            self.registerForDraggedTypes_(types);
            pass
        return self

    def draggingEntered_(self,sender):
        if NSImage.canInitWithPasteboard_(sender.draggingPasteboard()):
            self.imageFade = 0.2
            image = NSImage.alloc().initWithPasteboard_(sender.draggingPasteboard())
            if image is not None:
                self.setBackgroundRenderer_(IAImageBackgroundRenderer(image))
                self.setNeedsDisplay_(YES)
                return NSDragOperationCopy | NSDragOperationGeneric | NSDragOperationMove

    def draggingExited_(self,sender):
        self.imageFade = 1.0
        self.setBackgroundRenderer_(self.collectionItem.representedObject())
        self.setNeedsDisplay_(YES)

    def prepareForDragOperation_(self,sender):
        self.imageFade = 1.0
        self.setNeedsDisplay_(YES)
        if NSImage.canInitWithPasteboard_(sender.draggingPasteboard()):
            return YES
        else:
            self.draggingExited_(sender)

    def performDragOperation_(self,sender):
        image = NSImage.alloc().initWithPasteboard_(sender.draggingPasteboard())
        if image is not None:
            self.collectionItem.setSelected_(YES)
            self.collectionItem.collectionView().setBackgroundImage_(image);
            self.setNeedsDisplay_(YES)
            return YES
        else:
            self.draggingExited_(sender)


    def tag(self):
        return 1234; # magic for interface builder

    def mouseEntered_(self,event):
        self.imageFade = 0.85
        self.drawBorder = True

    def mouseExited_(self,event):
        self.imageFade = 1
        pass

    def drawRect_(self,rect):
        if self.drawBorder:
            self.imageFade = 0.85
            super(IACollectionImageView, self).drawRect_(rect);
            self.imageFade = 1
            path = NSBezierPath.bezierPath()
            size = self.frame().size;
            NSColor.selectedControlColor().colorWithAlphaComponent_(0.8).set()
            path.setLineWidth_(4)
            path.appendBezierPathWithRoundedRect_xRadius_yRadius_(((3,3),(size.width-6,size.height-6)),8,8)
            path.stroke()
        else:
            super(IACollectionImageView, self).drawRect_(rect);


    def mouseUp_(self,event):
        self.drawBorder = False
        self.setNeedsDisplay_(YES)
        if self.collectionItem is not None:
            self.collectionItem.setSelected_(YES)

    def mouseDown_(self,event):
        self.drawBorder = True
        self.setNeedsDisplay_(YES)



class IACollectionView(NSCollectionView):
    imageView = objc.IBOutlet()
    image = None

    #def frameChanged_(self,bla):
    #   self.setMaxItemSize_((300,300))
        #for i in self.content():
        #   i.view().setNeedsDisplay_(YES)
    #   pass

    def awakeFromNib(self):
        self.setAllowsMultipleSelection_(NO);
        self.sendNotification_(u"SelectionChanged");
        #self.setPostsFrameChangedNotifications_(YES)
#       NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self,self.frameChanged_,NSViewFrameDidChangeNotification,self);

    def sendNotification_(self,name):
        n = NSNotification.notificationWithName_object_(name,self)
        NSNotificationQueue.defaultQueue().enqueueNotification_postingStyle_coalesceMask_forModes_(n,NSPostWhenIdle,NSNotificationCoalescingOnName,None)


    def selectionChangedNotification_(self,sender):
        self.updateSelection();

    def updateSelection(self):
        idx = self.selectionIndexes().firstIndex()
        if idx != NSNotFound:
            self.imageView.setBackgroundRenderer_(self.content()[idx]);

    def setBackgroundImage_(self,img):
        bgr = IAImageBackgroundRenderer(img);
        content = NSMutableArray.arrayWithArray_(self.content());
        idx = self.selectionIndexes().firstIndex()
        if idx != NSNotFound:
            content[idx] = bgr
            self.setContent_(content);
            self.sendNotification_(u"SelectionChanged");

    def setImage_(self,img):
        self.image = img
        if img is not None:
            size = img.size()
            self.setMaxItemSize_((max(100,size.width*2),max(100,size.height*2)))
            self.setMinItemSize_((40,40))

        self.sendNotification_(u"ImageChanged");
        pass

    def newItemForRepresentedObject_(self,obj):
        colitem = super(IACollectionView,self).newItemForRepresentedObject_(obj);

        view  = colitem.view().viewWithTag_(1234);
        #view = IACollectionImageView.alloc().initWithFrame_(((0,0),image.size()))
        view.setImage_(self.image)
        view.setBackgroundRenderer_(obj)
        view.zoomToFill(0.8);
        #colitem = IACollectionViewItem.alloc().init()
        #colitem.setRepresentedObject_(obj)
        #colitem.setView_(view)
        view.collectionItem = colitem

        # FIXME: remove from notification queue when deallocing!
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(colitem,colitem.imageChangedNotification_, u"ImageChanged", self)
        return colitem;


