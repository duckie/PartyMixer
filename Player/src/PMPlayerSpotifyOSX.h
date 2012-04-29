//
//  PMPlayerSpotify.h
//  //  PartyMixer//  PartyMixer
//
//  Created by Nicolas Hognon on 08/04/12.
//  Copyright (c) 2012 ePawn. All rights reserved.
//

#ifndef _PMPlayerSpotifyOSX_H_
#define _PMPlayerSpotifyOSX_H_

#include "PMPlayerSpotifyMixer.h"

@class AppDelegate;

class PMPlayerSpotifyOSX : public PMPlayerSpotifyMixer
{
public:

    PMPlayerSpotifyOSX(AppDelegate* appDelegate, bool random);
    virtual ~PMPlayerSpotifyOSX();
    
    virtual void updated();
    virtual void endOfTrack(bool forced);
    virtual void connectionFailed();
    virtual void connectionSucceeded();
    virtual void notifyMainThread();
    virtual void trackReady(const char* name, const char* artist, int duration);
    virtual void trackReady(const char* name, const char* artist, int duration, const void* img_data, size_t img_size);
    virtual void progress(int second);
    
    void callEngine();
    void _chooseTrack();
    
    volatile bool _threadRunning;
    
    AppDelegate*    _appDelegate;
    
};

#endif // _PMPlayerSPOTIFY_H_
