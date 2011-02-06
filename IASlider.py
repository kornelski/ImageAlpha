# coding=utf-8
#
#  IASlider.py
#  ImageAlpha
#
#  Created by porneL on 24.wrzenia.08.
#  Copyright (c) 2008 porneL. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *

from math import pow,log

class IASlider(NSSlider):
    zoomView = objc.IBOutlet()

    def scrollWheel_(self,event):
        if self.zoomView is not None:
            self.zoomView.scrollWheel_(event)

#    def initWithFrame_(self, frame):
#        self = super(IASlider, self).initWithFrame_(frame)
#        if self:
#            # initialization code here
#            pass
#        return self

#    def drawRect_(self, rect):
        # drawing code here



class IAZoomTransformer(NSValueTransformer):
    def transformedValueClass(self):
        return NSNumber.__class__

    def allowsReverseTransformation(self):
        return YES

    def reverseTransformedValue_(self,zoom):
        result = NSNumber.numberWithFloat_(1.0/(4.0-zoom) if zoom < 3.0 else zoom-2.0)
        return result

    def transformedValue_(self,zoom):
        zoom = zoom or 1.0
        result = NSNumber.numberWithFloat_(max(0,4.0-1.0/zoom) if zoom < 1.0 else zoom+2.0)
        return result

class IAZoomTimesTransformer(NSValueTransformer):
    def transformedValue_(self,zoom):
        return u"%d×" % zoom if zoom >= 1.0 else [u"½×",u"⅓×",u"¼×"][min(2,int(round(1.0/zoom))-2)];

# converts numbers 0-257 to 0-9 range
class IABitDepthTransformer(NSValueTransformer):
    def transformedValueClass(self):
        return NSNumber.__class__

    def allowsReverseTransformation(self):
        return YES

    # colors to depth
    def transformedValue_(self,value):
        if value is None: return None;
        value = int(value);
        if (value > 256): return 9;
        if (value <= 2): return 1;
        return log(value,2);

    # depth to colors
    def reverseTransformedValue_(self,value):
        if value is None: return None;
        value = int(value);
        NSLog("Reverse transforming from %d" % value);
        if (value > 8): return 257;
        if (value <= 1): return 2;
        return round(pow(2,value));

# displays 0-9 range as 0-256 and 2^24
class IABitDepthNameTransformer(NSValueTransformer):
    def transformedValue_(self,value):
        if value is None: return None;
        value = int(value);
        if (value > 256): return u"2²⁴"
        return "%d" % value;


# converts numbers 0-8 to 0-256 range
class IABitDepthReverseTransformer(NSValueTransformer):
    def transformedValueClass(self):
        return NSNumber.__class__

    # depth to colors
    def transformedValue_(self,value):
        if value is None: return None;
        value = int(value);
        if (value <= 1): return 2;
        return pow(2,value);


