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

