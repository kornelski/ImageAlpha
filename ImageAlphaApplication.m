

#import "ImageAlphaApplication.h"

@implementation ImageAlphaApplication
@synthesize imageOptimPath;

-(void)applicationDidFinishLaunching:(NSApplication*)sender {
    self.imageOptimPath = [[NSWorkspace sharedWorkspace] absolutePathForAppBundleWithIdentifier:@"net.pornel.imageoptim"];
}

@end
