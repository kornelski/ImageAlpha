//
//  IAPatternBackgroundRenderer.m
//  ImageAlpha
//
//  Created by (ja) xx on 12.mar.12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "IAPatternBackgroundRenderer.h"
#import <QuartzCore/QuartzCore.h>

static void drawPatternImage(void *info, CGContextRef ctx)
{
    CGImageRef image = (CGImageRef)info;
    CGContextDrawImage(ctx, CGRectMake(0,0, CGImageGetWidth(image),CGImageGetHeight(image)), image);
}

@implementation IAPatternBackgroundRenderer

- (id)init
{
    self = [super init];
    if (self) {
        bgLayer = [CALayer new];
        NSMutableDictionary *newActions = [[NSMutableDictionary alloc] initWithObjectsAndKeys:
                                           [NSNull null], @"backgroundColor",
                                           [NSNull null], @"contents",
                                           [NSNull null], @"bounds",
                                           nil];
        bgLayer.actions = newActions; // non-animated scroll
        [newActions release];
    }
    return self;
}

-(BOOL)canMove {
    return YES;
}

-(CALayer *)getLayer {
    CALayer *newLayer = [CALayer new];
    newLayer.actions = [[bgLayer.actions copy] autorelease];
    
    CGColorRef color = CGColorCreateCopy(bgLayer.backgroundColor);
    newLayer.backgroundColor = color;
    CGColorRelease(color);
    
    return [newLayer autorelease];
}

-(void)dealloc {
    if (image) CGImageRelease(image);
    [bgLayer release];
    [super dealloc];
}

-(void)setTileImage:(NSImage*)nsimage {
    if (image) CGImageRelease(image);

    [NSGraphicsContext saveGraphicsState];
    image = [nsimage CGImageForProposedRect:&(NSRect){.size=[nsimage size]} context:NULL hints:[NSDictionary dictionary]];
    CGImageRetain(image);
    [NSGraphicsContext restoreGraphicsState];
}

-(void)tileLayerAtX:(NSNumber*)x Y:(NSNumber *)y {

    CGFloat width = CGImageGetWidth(image), height = CGImageGetHeight(image);
    CGPatternRef pattern = CGPatternCreate( image,
                                           CGRectMake(0, 0, width, height),
                                           CGAffineTransformMake (1, 0, 0, 1, [x doubleValue], [y doubleValue]),
                                           width, height,
                                           kCGPatternTilingConstantSpacing,
                                           true,
                                           &(CGPatternCallbacks){0, &drawPatternImage, 0});
    CGColorSpaceRef space = CGColorSpaceCreatePattern(NULL);
    CGColorRef color = CGColorCreateWithPattern(space, pattern, &(CGFloat){1.0});
    CGColorSpaceRelease(space);
    CGPatternRelease(pattern);
    bgLayer.backgroundColor = color; //set your layer's background to the image
    CGColorRelease(color);
}

@end
