//
//  IAPatternBackgroundRenderer.h
//  ImageAlpha
//
//  Created by (ja) xx on 12.mar.12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "IABackgroundRenderer.h"

@interface IAPatternBackgroundRenderer : IABackgroundRenderer {
    CGImageRef image;
    CALayer *bgLayer;
}
@end
