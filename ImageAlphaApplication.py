#
#  ImageAlphaAppDelegate.py
from objc import *
from Foundation import *
from AppKit import *

class ImageAlphaApplication(NSObject):
    imageOptimPath = None
    _imageOptimEnabled = False

    def applicationDidFinishLaunching_(self, sender):
        self.imageOptimPath = NSWorkspace.sharedWorkspace().absolutePathForAppBundleWithIdentifier_("net.pornel.imageoptim");
        pass

    def imageOptimEnabled(self):
        return self._imageOptimEnabled

    def setImageOptimEnabled_(self,flag):
        self._imageOptimEnabled = flag
