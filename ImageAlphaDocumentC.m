
#import "ImageAlphaDocumentC.h"

@implementation ImageAlphaDocumentC

@synthesize zoomedImageView, documentImage;

-(void) setDrawAlternateImage:(BOOL)val {
    // indirection to avoid leaks caused by xib observing itself
    if (self.zoomedImageView && self.documentImage) {
        self.zoomedImageView.drawAlternateImage = [NSNumber numberWithBool:val];
    }
}

-(BOOL) drawAlternateImage {
    if (self.zoomedImageView && self.documentImage) {
        return [self.zoomedImageView.drawAlternateImage boolValue];
    }
    return NO;
}

@end
