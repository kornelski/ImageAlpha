
#import <Cocoa/Cocoa.h>

@interface IAImageView : NSView
-(NSNumber*)drawAlternateImage;
-(void)setDrawAlternateImage:(NSNumber*)b;
@end

@class IAImage;

@interface ImageAlphaDocumentC : NSDocument {
    IAImageView* zoomedImageView;
}

@property (assign) BOOL drawAlternateImage;
@property (retain) IBOutlet IAImageView* zoomedImageView;
@property (retain) IAImage* documentImage;
@end
