

#import "ImageAlphaApplication.h"

@implementation ImageAlphaApplication

@synthesize imageOptimPath, ditheredMenu;

-(void)applicationDidFinishLaunching:(NSApplication*)sender {
    self.imageOptimPath = [[NSWorkspace sharedWorkspace] absolutePathForAppBundleWithIdentifier:@"net.pornel.imageoptim"];

    id dithered = [[NSUserDefaults standardUserDefaults] objectForKey:@"dithered"];
    int tag = dithered != nil ? [dithered boolValue] : -1;
    for (NSMenuItem *item in self.ditheredMenu.itemArray) {
        [item setState:item.tag == tag ? NSOnState : NSOffState];
    }
}

@end
