#
#  IAImage.py
from objc import *
from Foundation import *
from AppKit import *
from math import log

class Quantizer(object):
    def qualityLabel(self):
        return "Colors"

    def supportsIeMode(self):
        return False

    def preferredDithering(self):
        return True

    def numberOfColorsToQuality(self, colors):
        return colors;

    def versionId(self, colors, dithering, ieMode):
        return "c%d:m%s:d%d%d" % (self.numberOfColorsToQuality(colors), self.__class__.__name__, dithering, ieMode)

class Pngquant(Quantizer):
    def supportsIeMode(self):
        return True

    def launchArguments(self, dither, colors, ieMode):
        args = ["--floyd" if dither else "--nofs","%d" % colors];
        if ieMode:
            args.insert(0,"--iebug");
        return ("pngquant", args)

class Pngnq(Quantizer):
    def launchArguments(self, dither, colors, ieMode):
        return ("pngnq", ["-Q","f" if dither else "n","-n","%d" % colors])

class Posterizer(Quantizer):
    def qualityLabel(self):
        return "Quality"

    def preferredDithering(self):
        return False

    def numberOfColorsToQuality(self, c):
        return round(15 + (c * 240 / 255));

    def launchArguments(self, dither, colors, ieMode):
        args = ["%d" % self.numberOfColorsToQuality(colors)];
        if dither:
            args.insert(0,"-d")
        return ("posterizer",args);

class Blurizer(Quantizer):
    def qualityLabel(self):
        return "Quality"

    def preferredDithering(self):
        return True

    def versionId(self, colors, dithering, ieMode):
        return "blur%d" % self.numberOfColorsToQuality(colors)

    def numberOfColorsToQuality(self, c):
        return round(255 - 12 + 1.5*log(c, 2));

    def launchArguments(self, dither, colors, ieMode):
        args = ["-b", "%d" % self.numberOfColorsToQuality(colors)];
        return ("posterizer",args);


class IAImage(NSObject):
    _image = None
    _imageData = None

    path = None
    _sourceFileSize = None

    versions = None

    _numberOfColors = 256;

    _quantizationMethod = 0; # 0 = pngquant; 1 = pngnq; 2 = posterizer
    _quantizationMethods = [
        Pngquant(),
        Pngnq(),
        None, # separator
        Blurizer(),
        Posterizer(),
    ]
    _dithering = YES
    _ieMode = NO

    callbackWhenImageChanges = None

    def init(self):
        self = super(IAImage, self).init()
        self.versions = {};
        return self

    def setCallbackWhenImageChanges_(self, documentToCallback):
        self.callbackWhenImageChanges = documentToCallback;
        self.update()

    def setImage_(self,image):
        self._image = image

    def image(self):
        return self._image

    def imageData(self):
        return self._imageData;

    def sourceFileSize(self):
		return self._sourceFileSize;

    def setPath_(self,path):
		self.path = path
		(attrs,error) = NSFileManager.defaultManager().attributesOfItemAtPath_error_(self.path,None);
		self._sourceFileSize = attrs.objectForKey_(NSFileSize) if attrs is not None and error is None else None;

    def ieMode(self):
        return self._ieMode

    def setIeMode_(self,val):
        self._ieMode = int(val) > 0;
        if self._ieMode and not self.quantizer().supportsIeMode():
            self.setQuantizationMethod_(0);
        self.update()

    def dithering(self):
        return self._dithering

    def setDithering_(self,val):
        self._dithering = int(val) > 0
        self.update()

    def numberOfColors(self):
        return self._numberOfColors

    def qualityLabel(self):
        return self.quantizer().qualityLabel()

    def setNumberOfColors_(self,num):
        self._numberOfColors = int(num)
        self.update()

    def quantizationMethod(self):
        return self._quantizationMethod

    def quantizer(self):
        return self._quantizationMethods[self._quantizationMethod]

    def setQuantizationMethod_(self,num):
        self.willChangeValueForKey_("qualityLabel");
        self._quantizationMethod = num
        self.didChangeValueForKey_("qualityLabel");

        quantizer = self.quantizer()
        if not quantizer.supportsIeMode():
            self.setIeMode_(False)
        if quantizer.preferredDithering() is not None:
            self.setDithering_(quantizer.preferredDithering())
        self.update()

    def isBusy(self):
        if self.path is None: return False
        id = self.currentVersionId()
        if id not in self.versions: return False # not sure about this
        return not self.versions[id].isDone;

    def update(self):
        if self.path:
            id = self.currentVersionId()

            if self.numberOfColors() > 256:
                self._imageData = NSData.dataWithContentsOfFile_(self.path);
                self.setImage_(NSImage.alloc().initByReferencingFile_(self.path));

                if self.callbackWhenImageChanges is not None: self.callbackWhenImageChanges.imageChanged();

            elif id not in self.versions:
                self.versions[id] = IAImageVersion.alloc().init()
                self.versions[id].generateFromPath_method_dither_iemode_colors_callback_(self.path, self.quantizer(), self.dithering(), self.ieMode(), self.numberOfColors(), self)

                if self.callbackWhenImageChanges is not None: self.callbackWhenImageChanges.updateProgressbar();

            elif self.versions[id].isDone:
                self._imageData = self.versions[id].imageData
                self.setImage_(NSImage.alloc().initWithData_(self._imageData))

                if self.callbackWhenImageChanges is not None: self.callbackWhenImageChanges.imageChanged();

    def currentVersionId(self):
        return self.quantizer().versionId(self.numberOfColors(), self.dithering(), self.ieMode());

    def destroy(self):
        self.callbackWhenImageChanges = None
        for id in self.versions:
            self.versions[id].destroy()
        self.versions = {}


class IAImageVersion(NSObject):
    imageData = None
    isDone = False

    task = None
    outputPipe = None
    callbackWhenFinished = None

    def generateFromPath_method_dither_iemode_colors_callback_(self,path,quantizer,dither,ieMode,colors,callbackWhenFinished):

        self.isDone = False
        self.callbackWhenFinished = callbackWhenFinished

        (executable, args) = quantizer.launchArguments(dither, colors, ieMode)

        task = NSTask.alloc().init()

        exePath = NSBundle.mainBundle().pathForAuxiliaryExecutable_(executable)
        task.setLaunchPath_(exePath)
        task.setCurrentDirectoryPath_(exePath.stringByDeletingLastPathComponent())
        task.setArguments_(args);

        # pngout works best via standard input/output
        file = NSFileHandle.fileHandleForReadingAtPath_(path);
        task.setStandardInput_(file);

        # get output via pipe
        # use pipe's file handle to construct NSData object asynchronously
        outputPipe = NSPipe.pipe();
        task.setStandardOutput_(outputPipe);

        # pipe *must* be read, otheriwse task will block waiting for I/O
        handle = outputPipe.fileHandleForReading();
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, self.onHandleReadToEndOfFile_, NSFileHandleReadToEndOfFileCompletionNotification, handle);
        handle.readToEndOfFileInBackgroundAndNotify()

        task.launch();
        return task;

    def onHandleReadToEndOfFile_(self,notification):
        self.isDone = True

        self.imageData = notification.userInfo().objectForKey_(NSFileHandleNotificationDataItem);
        if self.callbackWhenFinished is not None:
            self.callbackWhenFinished.update()

    # FIXME: use dealloc and super()?
    def destroy(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self);
        self.callbackWhenFinished = None
        if self.task:
            self.task.terminate();
            self.task = None
        if self.outputPipe:
            self.outputPipe.fileHandleForReading().closeFile()
            self.outputPipe = None


