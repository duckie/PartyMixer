//
//  PlayerView.h
//  PartyMixer
//
//  Created by Nicolas Hognon on 12/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "AppDelegate.h"

@interface PlayerView : NSView
{
    IBOutlet NSTextField* _lTrack;
    IBOutlet NSTextField* _lArtist;
    IBOutlet NSTextField* _lProgress;
    IBOutlet NSImageView* _iImage;
    IBOutlet NSButton* _lRecord;
    int _duration;
    int _second;
    NSThread* _mainThread;
    IBOutlet AppDelegate *_appDelegate;    
}

- (IBAction)record:(id)target;

- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration;
- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration andImage:(NSImage*)image;
- (void)progress;
- (void)progress:(int)second;

@end
