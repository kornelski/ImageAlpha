//
//  IAColorBackgroundRenderer.m
//  ImageAlpha
//
//  Created by (ja) xx on 16.kwi.12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "IAColorBackgroundRenderer.h"

@implementation IAColorBackgroundRenderer

static CGColorRef CGColorCreateFromNSColor(CGColorSpaceRef colorSpace, NSColor *color)
{
    NSColor *deviceColor = [color colorUsingColorSpaceName:NSDeviceRGBColorSpace];

    CGFloat components[4];
    [deviceColor getRed: &components[0] green: &components[1] blue:&components[2] alpha: &components[3]];

    return CGColorCreate(colorSpace, components);
}

-(id)initWithColor:(NSColor*)c
{
    self = [super init];
    if (self) {
        CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB ();
        CGColorRef color = CGColorCreateFromNSColor(colorSpace, c);
        layer = [CALayer new];
        layer.backgroundColor = color;
        CGColorSpaceRelease (colorSpace);
        CGColorRelease(color);
    }
    return self;
}

-(CALayer *)getLayer {
    CALayer *newLayer = [CALayer new];
    CGColorRef color = CGColorCreateCopy(layer.backgroundColor);
    newLayer.backgroundColor = color;
    CGColorRelease(color);
    return [newLayer autorelease];
}

- (void)dealloc
{

    [super dealloc];
}

@end
