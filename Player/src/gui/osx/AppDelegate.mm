//
//  AppDelegate.m
//  PartyMixer
//
//  Created by Nicolas Hognon on 11/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "AppDelegate.h"
#import "PlayerView.h"
#import "LoginView.h"
#include <unistd.h>

@interface AppDelegate (Private)
-(void)processEvents;
-(void)chooseTrack;
@end

@implementation AppDelegate

@synthesize window = _window;
@synthesize mainView;
@synthesize loginView;
@synthesize playerView;

- (void)dealloc
{
    if (_player) {
        delete _player;
    }
    [super dealloc];
}
	
- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    if (remove("/tmp/data.pickle")) {
        printf ("Error remove: %s\n",strerror(errno));
    }

    _player = new PMPlayerSpotifyOSX(self,true);
    _player->create(true);
    
              
    [mainView addSubview:loginView];    
}

- (void)connectionWithLogin:(NSString*)login andPassword:(NSString*)password;
{
    _player->loggin([login UTF8String],[password UTF8String]);
}

// SpotifyDelegate

- (void)connectionFailed
{
    [loginView reset];
}

- (void)connectionSucceeded
{
    self.window.backgroundColor = [NSColor darkGrayColor];
    [loginView removeFromSuperview];
    [mainView addSubview:playerView];
}

- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration
{
    [playerView newTrack:name withArtiste:artist withDuration:duration];
}

- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration andImage:(NSImage*)image
{
    [playerView newTrack:name withArtiste:artist withDuration:duration andImage:image];
}

- (void)progress:(int)second
{
    [playerView progress:second];
}

/*- (void)callEngine
{
    NSPipe* recPipe = [NSPipe pipe];
    NSFileHandle* recFile;

    NSTask *recTask = [[NSTask alloc] init];
    [recTask setLaunchPath: @"/usr/bin/python"];
    
    NSArray *recArgs;
    recArgs = [NSArray arrayWithObjects: @"/Users/nicolas/DEV/GIT/PartyMixer/Moteur/decision.py", nil];
    [recTask setArguments: recArgs];
    
    [recTask setStandardOutput: recPipe];
     
     recFile = [recPipe fileHandleForReading];
    
    [recTask launch];
    
    NSData *recData;    
    recData = [recFile readDataToEndOfFile];
    
    if (_recString) {
        [_recString release];
    }
    _recString = [[NSString alloc] initWithData: recData encoding: NSUTF8StringEncoding];
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(taskDidTerminate:)
                                                 name:NSTaskDidTerminateNotification
                                               object:nil];
}*/

/*- (void)taskDidTerminate:(NSNotification *)notification
{
    [[NSNotificationCenter defaultCenter] removeObserver:self name:NSTaskDidTerminateNotification object:nil];
    
    NSLog(@"recString: %@",_recString);
    
    std::vector<std::string> ids;
    NSString *cmd;
    NSScanner *scanner = [NSScanner scannerWithString:_recString];
    while ([scanner isAtEnd]==NO) {
        [scanner scanUpToCharactersFromSet:[NSCharacterSet
                                        whitespaceAndNewlineCharacterSet] 
                            intoString:&cmd];
        NSRange r = [cmd rangeOfString:@"spotify-WW:track:"];
        cmd = [cmd substringFromIndex:r.location+r.length];
        cmd = [@"spotify:track:" stringByAppendingString:cmd];
        ids.push_back([cmd UTF8String]);
    }
    
    _player->setIDS(ids);
}*/

-(void)endOfTrack
{
    _player->endOfTrack(true);
}

@end

@implementation AppDelegate (Private)

-(void)chooseTrack
{
    _player->_chooseTrack();
}

-(void)processEvents;
{
	[NSObject cancelPreviousPerformRequestsWithTarget:self selector:_cmd object:nil];
	int msTilNext = 0;
	while(msTilNext == 0) {
		sp_session_process_events(_player->getSession(), &msTilNext);
    }
        
    NSTimeInterval secsTilNext = msTilNext/1000.;
    [self performSelector:_cmd withObject:nil afterDelay:secsTilNext];
}

@end