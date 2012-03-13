//
//  IAPatternBackgroundRenderer.m
//  ImageAlpha
//
//  Created by (ja) xx on 12.mar.12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "IAPatternBackgroundRenderer.h"
#import <Quartz/Quartz.h>

static void drawPatternImage(void *info, CGContextRef ctx)
{
    CGImageRef image = (CGImageRef)info;
    CGContextDrawImage(ctx, CGRectMake(0,0, CGImageGetWidth(image),CGImageGetHeight(image)), image);
}


@implementation IAPatternBackgroundRenderer

-(void)dealloc {
    if (image) CGImageRelease(image);
    [super dealloc];
}

-(void)setTileImage:(NSImage*)nsimage {
    if (image) CGImageRelease(image);

    [NSGraphicsContext saveGraphicsState];
    image = [nsimage CGImageForProposedRect:&(NSRect){.size=[nsimage size]} context:NULL hints:[NSDictionary dictionary]];
    CGImageRetain(image);
    [NSGraphicsContext restoreGraphicsState];
}

-(void)tileLayer:(CALayer *)layer atX:(NSNumber*)x Y:(NSNumber *)y {

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
    NSLog(@"Got color %@", color);
    layer.backgroundColor = color; //set your layer's background to the image
    CGColorRelease(color);
}

@end
