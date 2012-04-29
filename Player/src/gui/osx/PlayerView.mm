//
//  PlayerView.m
//  PartyMixer
//
//  Created by Nicolas Hognon on 12/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "PlayerView.h"

@implementation PlayerView

- (id)initWithFrame:(NSRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code here.
    }
    
    _lTrack.stringValue = @"";
    _lProgress.stringValue = @"";
    _duration = 0;
    _second = 0;
    
    _mainThread = [NSThread currentThread];
    
    return self;
}

- (void)mouseDown:(NSEvent *)theEvent
{
    if ([theEvent clickCount]>1) {
        NSPoint event_location = [theEvent locationInWindow];
        NSPoint local_point = [self convertPoint:event_location toView:_iImage];
        if (CGRectContainsPoint(_iImage.bounds, local_point)) {
            printf("LOOKING FOR NEW TRACK !!!\n");
            [_appDelegate endOfTrack];
        }
    }
}

- (IBAction)record:(id)target
{
    [_lRecord setEnabled:NO];
     // NSString *hostsforping = @"google.es";
    NSTask *recTask = [[NSTask alloc] init];
    [recTask setLaunchPath: @"/opt/local/bin/rec"];
    
    //  ./rec sample.wav trim 0 00:05
    
    NSArray *recArgs;
    recArgs = [NSArray arrayWithObjects: @"-b 16", @"/Users/nicolas/DEV/GIT/PartyMixer/Moteur/test_wav/sample.wav", @"trim", @"0", @"00:05", nil];
    [recTask setArguments: recArgs];
    
    /*NSPipe *recPipe = [NSPipe pipe];
    [recArgs setStandardOutput: recPipe];
    
    NSFileHandle *recFile;
    pingfile = [pingpipe fileHandleForReading];*/
    
    [recTask launch];
    
    //NSData *pingdata1;    
    //pingdata1 = [pingfile readDataToEndOfFile];
    
    //NSString *pingstring;
    //pingstring = [[NSString alloc] initWithData: pingdata1 encoding: NSUTF8StringEncoding];
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(taskDidTerminate:)
                                                 name:NSTaskDidTerminateNotification
                                               object:nil];
}

- (void) taskDidTerminate:(NSNotification *)notification
{
    [self performSelectorOnMainThread:@selector(reEnableRecord) withObject:nil waitUntilDone:NO];
}

- (void) reEnableRecord
{
    [_lRecord setEnabled:YES];
}

- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration
{
    [_iImage setHidden:TRUE];
    _duration = duration;
    
    _lTrack.stringValue = name;
    _lArtist.stringValue = artist;

    int sec = duration/1000;
    div_t divresult;
    divresult = div (sec,60);
    _lProgress.stringValue = [NSString stringWithFormat:@"%.2d:%.2d", divresult.quot, divresult.rem];
}

- (void)newTrack:(NSString*)name withArtiste:(NSString*)artist withDuration:(int)duration andImage:(NSImage*)image
{
    [self newTrack:name withArtiste:artist withDuration:duration];
    [_iImage setHidden:FALSE];
    _iImage.image = image;
}

- (void)progress
{
    @synchronized(self) {
        int sec = _duration/1000;
        div_t divresult;
        divresult = div (sec,60);
        div_t divresult2;
        divresult2 = div (_second,60);
        _lProgress.stringValue = [NSString stringWithFormat:@"%.2d:%.2d | %.2d:%.2d",
                                  divresult2.quot, divresult2.rem,
                                  divresult.quot, divresult.rem];
        /*if (_second>5) {
            [_appDelegate endOfTrack];
        }*/
        
    }
}

- (void)progress:(int)second
{
    NSThread* t = [NSThread currentThread];
    if (t != _mainThread) {
        @synchronized(self) {
            _second = second;
            [self performSelectorOnMainThread:@selector(progress) withObject:nil waitUntilDone:NO];
        }
        return;
    }
    
    int sec = _duration/1000;
    div_t divresult;
    divresult = div (sec,60);
    div_t divresult2;
    divresult2 = div (second,60);
    _lProgress.stringValue = [NSString stringWithFormat:@"%.2d:%.2d | %.2d:%.2d",
                              divresult2.quot, divresult2.rem,
                              divresult.quot, divresult.rem];
}

@end
