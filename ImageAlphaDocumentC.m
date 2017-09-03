
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

-(BOOL) validateMenuItem:(NSMenuItem *)sender {
    return self.documentImage != nil;
}

-(void) setDitheredPreference:(NSMenuItem *)sender {
    for (NSMenuItem *item in sender.menu.itemArray) {
        [item setState:item == sender ? NSOnState : NSOffState];
    }

    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    if (sender.tag < 0) {
        [defaults removeObjectForKey:@"dithered"];
    } else {
        [defaults setBool:sender.tag forKey:@"dithered"];
    }
    [defaults synchronize];
    [self.documentImage updateDithering];
}

@end
