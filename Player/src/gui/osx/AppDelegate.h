//
//  AppDelegate.h
//  PartyMixer
//
//  Created by Nicolas Hognon on 11/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#include "PMPlayerSpotifyOSX.h"

@class LoginView;
@class PlayerView;

@interface AppDelegate : NSObject <NSApplicationDelegate>
{
    PMPlayerSpotifyOSX* _player;
    NSString* _recString;
}

@property (assign) IBOutlet NSWindow *window;
@property (assign) IBOutlet NSView *mainView;
@property (assign) IBOutlet LoginView *loginView;
@property (assign) IBOutlet PlayerView *playerView;

- (void)connectionWithLogin:(NSString*)login andPassword:(NSString*)password;
- (void)connectionFailed;
- (void)connectionSucceeded;
- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration;
- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration andImage:(NSImage*)image;
- (void)progress:(int)second;

//- (void)callEngine;
- (void)endOfTrack;


@end
