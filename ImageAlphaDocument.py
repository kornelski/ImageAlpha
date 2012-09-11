# coding=utf-8
#
#  IAController.py

from objc import *
from Foundation import *
import IAImageView
from IACollectionItem import *
from IABackgroundRenderer import *
from IAImage import IAImage

class ImageAlphaDocument(ImageAlphaDocumentC):

	statusBarView = objc.IBOutlet()
	backgroundsView = objc.IBOutlet()
	progressBarView = objc.IBOutlet()
	savePanelView = objc.IBOutlet()

	def windowNibName(self):
		return u"ImageAlphaDocument"

	def windowControllerDidLoadNib_(self, aController):
		super(ImageAlphaDocument, self).windowControllerDidLoadNib_(aController)

		self._startWork();

		bgs = [
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/photoshop","png")),
			IAColorBackgroundRenderer.alloc().initWithColor_(NSColor.redColor()),
			IAColorBackgroundRenderer.alloc().initWithColor_(NSColor.greenColor()),
			IAColorBackgroundRenderer.alloc().initWithColor_(NSColor.blueColor()),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/461223192","jpg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/A_MIXRED","jpeg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/nature71","jpg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/seawaterfull2","jpg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/STONE4","jpeg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/Rustpattern","jpeg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/461223185","jpg")),
			IAImageBackgroundRenderer.alloc().initWithImage_(self._getImage("textures/G_IRON3","jpg")),
		]
		self.backgroundsView.setContent_(bgs);

		self.zoomedImageView().window().setAcceptsMouseMovedEvents_(YES);
		self.zoomedImageView().setBackgroundRenderer_(bgs[0])

		if self.documentImage() is not None:
			self.setDisplayImage_(self.documentImage().image())
		   # self.setStatusMessage_("Opened " + NSFileManager.defaultManager().displayNameAtPath_(self.documentImage().path));
		else:
			self.setStatusMessage_("To get started, drop PNG image onto main area on the right");

		self.updateZoomedImageViewAlternateImage()


		self._endWork();

	def updateZoomedImageViewAlternateImage(self, zoomToFill=False):
		if self.zoomedImageView() is not None and self.documentImage() is not None:
			self.zoomedImageView().setAlternateImage_(self.documentImage().image())
			if zoomToFill:
				self.zoomedImageView().zoomToFill()

	def validateUserInterfaceItem_(self,item):
		# I can't find nice way to compare selectors in pyobjc, so here comes __repr__() hack (or non-hack I hope)
		if self.documentImage() is None and item.action().__repr__() in ["'saveDocument:'","'saveDocumentAs:'","'zoomIn:'","'zoomOut:'", "'toggleShowOriginal:'"]:
			return NO

		return super(ImageAlphaDocument, self).validateUserInterfaceItem_(item);


	def prepareSavePanel_(self, savePanel):
		delegate = NSApplication.sharedApplication().delegate()
		if delegate and delegate.imageOptimPath is not None:
			savePanel.setAccessoryView_(self.savePanelView);
		return YES

	def dataOfType_error_(self, typeName, outError):
		if url.isFileURL() or self.documentImage() is not None:
			return (self.documentImage().imageData(), None)
		return (None,None)

	def writeToURL_ofType_error_(self, url, typeName, outErorr):
		NSLog("write to %s type %s" % (url.path(), typeName));

		if url.isFileURL() or self.documentImage() is not None:
			data = self.documentImage().imageData();
			if data is not None:
				if NSFileManager.defaultManager().createFileAtPath_contents_attributes_(url.path(), data, None):
					self.optimizeFileIfNeeded_(url);
					return (True, None)

		return (NO,None)

	def readFromURL_ofType_error_(self, url, typeName, outError):
		NSLog("Reading file %s" % url.path());
		if not url.isFileURL():
			return (NO,None)
		return (self.setDocumentImageFromPath_(url.path()),None)

	def optimizeFileIfNeeded_(self,url):
		delegate = NSApplication.sharedApplication().delegate();
		if not delegate or delegate.imageOptimPath is None or not NSUserDefaults.standardUserDefaults().boolForKey_("Optimize"):
			return

		w = NSWorkspace.sharedWorkspace();
		result = w.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url], "net.pornel.imageoptim", NSWorkspaceLaunchAsync|NSWorkspaceLaunchWithoutAddingToRecents, None, None)
		if (not result):
			result = w.openFile_withApplication_(url.path(), delegate.imageOptimPath);
			if (not result):
				NSLog("Could not launch ImageOptim for %s" % url);

	def setStatusMessage_(self,msg):
		NSLog("(status) %s", msg);
		if self.statusBarView is not None: self.statusBarView.setStringValue_(msg);

	def canSetDocumentImageFromPasteboard_(self,pboard):
# disabled until in-memory image support is done
#		 if NSImage.canInitWithPasteboard_(pboard):
#			 NSLog("image will handle that");
#			 return YES

		type = pboard.availableTypeFromArray_([NSFilenamesPboardType]);
		if type is not None:
		# FIXME: check for PNGs here
#			filenames = self.filenamesFromPasteboard_(pboard)
#			NSLog("Filenames %s" % filenames);
#			for f in filenames:
#				NSLog("drop file %s" % f);
			return YES

	def filenamesFromPasteboard_(self,pboard):
		data = pboard.dataForType_(NSFilenamesPboardType)
		if data is None: return []

		filenames, format, errorDescription = NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
					data , kCFPropertyListImmutable, None, None)
		return filenames;

	def setDocumentImageFromPasteboard_(self,pboard):
		type = pboard.availableTypeFromArray_([NSFilenamesPboardType]);
		if type is not None:
			filenames = self.filenamesFromPasteboard_(pboard)
			for file in filenames:
				if self.setDocumentImageFromPath_(file):
					return YES

# disabled until in-memory image support is done
#		 if NSImage.canInitWithPasteboard_(pboard):
#			 image = NSImage.alloc().initWithPasteboard_(pboard);
#			 self.setDocumentImageFromImage_(image)
#			 return YES

		return NO

	def setDocumentImageFromPath_(self,path):
		image = NSImage.alloc().initWithContentsOfFile_(path)
		if image is None:
			#NSLog("img is none");
			return NO

		docimg = IAImage.alloc().init();
		self.setFileURL_(NSURL.fileURLWithPath_(path))
		self.setFileType_("public.png.imagealpha");

		docimg.setPath_(path);
		docimg.setImage_(image);
		self.setNewDocumentImage_(docimg)
		return YES

	def setDocumentImageFromImage_(self,image):
		return NO # not supported until iaimage can save temp image

#		 if self.documentImage() is not None:
#			 NSLog("That's not supported yet");
#			 return NO

#		 docimg = IAImage.alloc().init();
#		 docimg.setImage_(image)
#		 return self.setNewDocumentImage_(docimg);

	def setNewDocumentImage_(self,docimg):
		#NSLog("new dimage set");
		if self.documentImage() is not None:
			self.documentImage().destroy();

		self.setDocumentImage_(docimg);
		docimg.setCallbackWhenImageChanges_(self);
		self.setDisplayImage_(docimg.image());

		self.updateZoomedImageViewAlternateImage(zoomToFill=True)

	def setDisplayImage_(self,image):
		if self.zoomedImageView() is None or self.backgroundsView is None: return;
		self.zoomedImageView().setImage_(image)
		self.backgroundsView.setImage_(image)
		self.backgroundsView.setSelectable_(YES if image is not None else NO);
		#NSLog("Set new display image %s" % image);

	def imageChanged(self):
		assert self.documentImage() is not None
		self.setDisplayImage_(self.documentImage().image());
		data = self.documentImage().imageData()
		self.updateProgressbar()
		if data is not None:
			source_filesize = self.documentImage().sourceFileSize();
			if source_filesize is None or source_filesize < data.length():
				msg = "Image size: %d bytes" % data.length()
			else:
				percent = 100-data.length()*100/source_filesize
				msg = "Image size: %d bytes (saved %d%% of %d bytes)" % (data.length(), percent, source_filesize)
			self.setStatusMessage_(msg)

	def _getImage(self,name,ext="png"):
		path = NSBundle.mainBundle().resourcePath().stringByAppendingPathComponent_(name).stringByAppendingPathExtension_(ext);
		image = NSImage.alloc().initWithContentsOfFile_(path);
		if image is None:
			NSLog("Failed to load %s " % name);
		return image

	_busyLevel = 0

	def _startWork(self):
		self._busyLevel += 1
		self.updateProgressbar()

	def _endWork(self):
		self._busyLevel -= 1
		self.updateProgressbar()

	def updateProgressbar(self):
		if self.progressBarView is None: return

		isBusy = self._busyLevel > 0 or (self.documentImage() is not None and self.documentImage().isBusy());

		if isBusy:
			self.progressBarView.startAnimation_(self);
		else:
			self.progressBarView.stopAnimation_(self);

	@objc.IBAction
	def toggleShowOriginal_(self,action):
		if self.zoomedImageView() is not None:
			self.zoomedImageView().setDrawAlternateImage_(not self.zoomedImageView().drawAlternateImage());

	@objc.IBAction
	def revert_(self,action):
		pass

	@objc.IBAction
	def zoomIn_(self, sender):
		if self.zoomedImageView() is not None:
			self.zoomedImageView().zoomIn_(sender);

	@objc.IBAction
	def zoomOut_(self, sender):
		if self.zoomedImageView() is not None:
			self.zoomedImageView().zoomOut_(sender);
