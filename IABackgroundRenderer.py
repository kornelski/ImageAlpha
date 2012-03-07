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
	composite = NSCompositeCopy

	def initWithImage_(self,image):
		self = super(IAImageBackgroundRenderer, self).init();
		if self:
			self.backgroundImage = image
			size = image.size()

			# background may be tiny and somehow 2000 loop iterations in drawRect are SLOOOOOW
			# so make sure that image is large enough to be drawn in few iterations
			xtimes = ceil(320.0 / size.width)
			ytimes = ceil(240.0 / size.height)

			#if xtimes > 2 or ytimes > 2:
			# paint it anyway, to render over predictable background color
			# coreanimation ignores NSCompositeCopy
			bigimage = NSImage.alloc().initWithSize_((size.width*xtimes,size.height*ytimes))
			bigsize = bigimage.size()
			whole = NSMakeRect(0,0,bigsize.width,bigsize.height);
			self.composite = NSCompositeSourceOver
			bigimage.lockFocus();
			NSColor.magentaColor().set()
			NSRectFill(whole)
			self.drawRect_(whole);
			bigimage.unlockFocus();
			self.backgroundImage = bigimage
			self.composite = NSCompositeCopy
		return self;

	def getLayer(self):
		return self.layerForTileImage_(self.backgroundImage);

	def canMove(self):
		return YES

	def moveBy_(self,delta):
		size = self.backgroundImage.size()
		self.backgroundOffset = ((self.backgroundOffset[0] - delta[0]) % size.width,
								 (self.backgroundOffset[1] - delta[1]) % size.height)

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
				self.backgroundImage.drawInRect_fromRect_operation_fraction_(((currentx,currenty),size), wholeimage, self.composite, 1.0)
				currentx += size.width
			currenty += size.height

