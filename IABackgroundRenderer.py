#
#  IABackgroundRenderer.py
from objc import *
from Foundation import *
from AppKit import *
from IAImageView import IAImageView
from  math import floor, ceil
from Quartz.CoreGraphics import *
from Quartz.QuartzCore import *

IAColorBackgroundRenderer = NSClassFromString("IAColorBackgroundRenderer");

class IAImageBackgroundRenderer(NSClassFromString("IAPatternBackgroundRenderer")):
	backgroundOffset = (0,0)

	def initWithImage_(self,image):
		self = super(IAImageBackgroundRenderer, self).init();
		if self:
			self.setTileImage_(image);
			self.moveBy_((0,0));
		return self;

	def canMove(self):
		return YES

	def moveBy_(self,delta):
		self.backgroundOffset = ((self.backgroundOffset[0] + delta[0]),
								 (self.backgroundOffset[1] + delta[1]))
		self.tileLayerAtX_Y_(self.backgroundOffset[0],self.backgroundOffset[1]);

