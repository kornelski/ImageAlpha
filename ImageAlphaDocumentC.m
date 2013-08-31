
#import "ImageAlphaDocumentC.h"

@implementation ImageAlphaDocumentC

@synthesize zoomedImageView, documentImage, leftPaneView;

static CGFloat constrain(NSInteger dividerIndex, CGFloat proposedSize)
{
    if (dividerIndex == 0) {
        if (proposedSize > 300) return 300;
        if (proposedSize < 210) return 210;
    }
    return proposedSize;
}

- (CGFloat)splitView:(NSSplitView *)splitView constrainMinCoordinate:(CGFloat)proposedSize ofSubviewAt:(NSInteger)dividerIndex {
    return constrain(dividerIndex, proposedSize);
}

- (CGFloat)splitView:(NSSplitView *)splitView constrainMaxCoordinate:(CGFloat)proposedSize ofSubviewAt:(NSInteger)dividerIndex {
    return constrain(dividerIndex, proposedSize);
}

- (CGFloat)splitView:(NSSplitView *)splitView constrainSplitPosition:(CGFloat)proposedSize ofSubviewAt:(NSInteger)dividerIndex {
    return constrain(dividerIndex, proposedSize);
}

- (BOOL)splitView:(NSSplitView *)splitView shouldAdjustSizeOfSubview:(NSView *)subview {
    return subview != self.leftPaneView;
}


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
