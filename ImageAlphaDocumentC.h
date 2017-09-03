
#import <Cocoa/Cocoa.h>

@interface IAImageView : NSView
-(NSNumber*)drawAlternateImage;
-(void)setDrawAlternateImage:(NSNumber*)b;
@end

@interface IAImage : NSObject
-(void)updateDithering;
@end

@interface ImageAlphaDocumentC : NSDocument {
    IAImageView* zoomedImageView;
    NSView *leftPaneView;
}

@property (assign) BOOL drawAlternateImage;
@property (retain) IBOutlet IAImageView* zoomedImageView;
@property (retain) IAImage* documentImage;
@property (retain) IBOutlet NSView* leftPaneView;
@end
