//
//  main.m
//  PartyMixer
//
//  Created by Nicolas Hognon on 11/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>

int main(int argc, char *argv[])
{
    NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
    int retVal = NSApplicationMain(argc, (const char **)argv);
    [pool release];
    return retVal;
}
