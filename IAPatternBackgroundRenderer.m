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

static void releasePatternImage(void *info)
{
    CGImageRelease((CGImageRef)info);
}

@implementation IAPatternBackgroundRenderer

-(CALayer *)layerForTileImage:(NSImage *)nsimage {

    [NSGraphicsContext saveGraphicsState];

    CGImageRef image = [nsimage CGImageForProposedRect:&(NSRect){.size=[nsimage size]} context:NULL hints:[NSDictionary dictionary]];
    CGImageRetain(image);
    CGFloat width = CGImageGetWidth(image), height = CGImageGetHeight(image);
    CGPatternRef pattern = CGPatternCreate( image,
                                           CGRectMake(0, 0, width, height),
                                           CGAffineTransformMake (1, 0, 0, 1, 0, 0),
                                           width, height,
                                           kCGPatternTilingConstantSpacing,
                                           true,
                                           &(CGPatternCallbacks){0, &drawPatternImage, &releasePatternImage});
    CGColorSpaceRef space = CGColorSpaceCreatePattern(NULL);
    CGColorRef color = CGColorCreateWithPattern(space, pattern, &(CGFloat){1.0});
    CGColorSpaceRelease(space);
    CGPatternRelease(pattern);
    CALayer *layer = [CALayer layer];
    NSLog(@"Got color %@", color);
    layer.backgroundColor = color; //set your layer's background to the image
    CGColorRelease(color);
    [NSGraphicsContext restoreGraphicsState];
    NSLog(@"Got pattern layer %@", layer);
    return layer;
}

@end
