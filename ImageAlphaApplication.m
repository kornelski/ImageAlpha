

#import "ImageAlphaApplication.h"

@implementation ImageAlphaApplication
@synthesize imageOptimPath, imageOptimEnabled;

-(void)applicationDidFinishLaunching:(NSApplication*)sender {
    self.imageOptimPath = [[NSWorkspace sharedWorkspace] absolutePathForAppBundleWithIdentifier:@"net.pornel.imageoptim"];
}

@end
