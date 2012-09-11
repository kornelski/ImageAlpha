//
//  IAColorBackgroundRenderer.h
//  ImageAlpha
//
//  Created by (ja) xx on 16.kwi.12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "IABackgroundRenderer.h"

@interface IAColorBackgroundRenderer : IABackgroundRenderer {
    CALayer *layer;
}

-(id)initWithColor:(NSColor*)c;


@end
