#
#  IABackgroundRenderer.py
from objc import *
from Foundation import *
from AppKit import *
from IAImageView import IAImageView
from  math import floor, ceil
from Quartz.CoreGraphics import *
from Quartz.QuartzCore import *


class IABackgroundRenderer(object):
	def moveBy_(self,by):
		pass

	def canMove(self):
		return NO

class IAColorBackgroundRenderer(IABackgroundRenderer):
	color = None;
	backgroundImage = None;

	def __init__(self,nscolor):
		self.color = nscolor

	def getLayer(self):
		layer = CALayer.layer()
		# fixme: bad colorspace
		layer.setBackgroundColor_(CGColorCreateGenericRGB(self.color.redComponent(),self.color.greenComponent(),self.color.blueComponent(),1));
		layer.setContents_(None);
		return layer;

	def drawRect_(self,rect):
		if self.color is None: return

		self.color.set()
		NSRectFill(rect)

class IAImageBackgroundRenderer(NSClassFromString("IAPatternBackgroundRenderer")):
	backgroundImage = None
	backgroundOffset = (0,0)

	def initWithImage_(self,image):
		self = super(IAImageBackgroundRenderer, self).init();
		if self:
			self.backgroundImage = image
			self._bgLayer = CALayer.layer();
			self.setTileImage_(image);
			self.moveBy_((0,0));
		return self;

	def getLayer(self):
		return self._bgLayer;

	def canMove(self):
		return YES

	def moveBy_(self,delta):
		self.backgroundOffset = ((self.backgroundOffset[0] + delta[0]),
								 (self.backgroundOffset[1] + delta[1]))
		self.tileLayer_atX_Y_(self._bgLayer,self.backgroundOffset[0],self.backgroundOffset[1]);


	def drawRect_(self,rect):
		size = self.backgroundImage.size()

		widthend = rect.origin.x + rect.size.width
		heightend = rect.origin.y + rect.size.height

		currentx = rect.origin.x // size.width * size.width  - self.backgroundOffset[0]
		currenty = rect.origin.y // size.height * size.height  - self.backgroundOffset[1]
		wholeimage = ((0,0),size)

		# totally depends on view doing the clipping anyway
		while currenty < heightend:
			drawnwidth = 0
			currentx = rect.origin.x // size.width * size.width - self.backgroundOffset[0]
			while currentx < widthend:
				self.backgroundImage.drawInRect_fromRect_operation_fraction_(((currentx,currenty),size), wholeimage, NSCompositeCopy, 1.0)
				currentx += size.width
			currenty += size.height

