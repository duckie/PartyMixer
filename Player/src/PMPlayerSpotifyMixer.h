//
//  PMPlayerSpotify.h
//  nipinipi
//
//  Created by Nicolas Hognon on 08/04/12.
//  Copyright (c) 2012 ePawn. All rights reserved.
//

#ifndef _PMPlayerSpotifyMixer_H_
#define _PMPlayerSpotifyMixer_H_

#include "PMPlayerSpotify.h"
#include <vector>
#include <string>

class PMPlayerSpotifyMixer : public PMPlayerSpotify
{
public:

    PMPlayerSpotifyMixer(bool random);
    virtual ~PMPlayerSpotifyMixer();
    
    virtual void connectionSucceeded();

    virtual void trackReady(const char* name, const char* artist, int duration) {}
    virtual void trackReady(const char* name, const char* artist, int duration, const void* img_data, size_t img_size) {}
    
    void setIDS(const std::vector<std::string>& ids);
    
    static void _image_loaded(sp_image *image, void *userdata);
    
    bool            _random;
    //sp_playlist*    _playlist;
    int             _count;
    int             _indice;
    sp_link*        _link;
    sp_track*       _track;
    bool            _playing;
    sp_image*       _image;

    std::vector<std::string> _ids;

};

#endif // _PMPlayerSPOTIFY_H_
