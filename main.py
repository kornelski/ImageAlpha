#
#  main.py

# can't avoid default encoding. Python dies in a system-initiated callback due to pretending it's still 1963.
import sys
reload(sys);
sys.setdefaultencoding("utf8");

#import modules required by application
import objc
import Foundation
import AppKit

objc.setVerbose(1)

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib

import ImageAlphaDocument
import IASlider
import IACollectionItem
import IAImageViewInteractive
import IABackgroundRenderer
import IAImageView
import IAImage
import ImageAlphaApplication

# pass control to AppKit
AppHelper.runEventLoop()
