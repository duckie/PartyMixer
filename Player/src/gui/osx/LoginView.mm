//
//  LoginView.m
//  PartyMixer
//
//  Created by Nicolas Hognon on 11/04/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "LoginView.h"

@interface LoginView (Private)
- (void)launchConnection;
@end

@implementation LoginView

- (id)initWithFrame:(NSRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code here.
    }
    
    [self reset];
    
    return self;
}

- (void)reset
{
    [_tfPassword setHidden:FALSE];
    [_tfLogin setHidden:FALSE];
    [_btnConnection setHidden:FALSE];
    
    [_lConnection setHidden:TRUE];
    [_piIndicator setHidden:TRUE];
    [_piIndicator stopAnimation:self];
}

- (IBAction)loginOnReturn:(id)target
{
    [_tfPassword becomeFirstResponder];
}

- (IBAction)passwordOnReturn:(id)target
{
}

- (void)controlTextDidEndEditing:(NSNotification *)aNotification
{
    NSControl *textfield = [aNotification object]; 
    NSDictionary *dict  = [aNotification userInfo];
    NSNumber  *reason = [dict objectForKey: @"NSTextMovement"];
    int code = [reason intValue];
    
    if (textfield==_tfLogin && code == NSReturnTextMovement) {
        if ([_tfLogin.stringValue length]>0) {
            [_tfPassword becomeFirstResponder];
        }
    } else if (textfield==_tfPassword && code == NSReturnTextMovement) {
        [self launchConnection];
    }    
}

- (IBAction)connection:(id)target
{
    [self launchConnection];
}

@end

@implementation LoginView (Private)

- (void)launchConnection
{
    [_tfPassword setHidden:TRUE];
    [_tfLogin setHidden:TRUE];
    [_btnConnection setHidden:TRUE];
    
    [_lConnection setHidden:FALSE];
    [_piIndicator setHidden:FALSE];
    [_piIndicator startAnimation:self];
    
    [_appDelegate connectionWithLogin:_tfLogin.stringValue andPassword:_tfPassword.stringValue];
}

@end

