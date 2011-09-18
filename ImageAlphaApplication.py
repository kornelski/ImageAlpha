#
#  ImageAlphaAppDelegate.py
#  ImageAlpha
#
#  Created by porneL on 18.wrze?nia.08.
#  Copyright porneL 2011. All rights reserved.
#
from objc import *
from Foundation import *
from AppKit import *

class IAApplication(NSObject):
    imageOptimPath = None
    imageOptimEnabled = False

    def applicationDidFinishLaunching_(self, sender):
        self.imageOptimPath = NSWorkspace.sharedWorkspace().absolutePathForAppBundleWithIdentifier_("net.pornel.imageoptim");
        pass
