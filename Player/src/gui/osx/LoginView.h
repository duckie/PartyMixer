//
//  LoginView.h
//  PartyMixer
//
//  Created by Nicolas Hognon on 11/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "AppDelegate.h"

@interface LoginView : NSView<NSTextFieldDelegate>
{
    IBOutlet NSTextField *_tfLogin;
    IBOutlet NSTextField *_tfPassword;
    IBOutlet NSButton *_btnConnection;
    IBOutlet NSTextField *_lConnection;
    IBOutlet NSProgressIndicator *_piIndicator;
    IBOutlet AppDelegate *_appDelegate;    
}

- (void)reset;

- (IBAction)loginOnReturn:(id)target;
- (IBAction)passwordOnReturn:(id)target;
- (IBAction)connection:(id)target;

@end
