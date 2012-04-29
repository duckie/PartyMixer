//
//  PMPlayerSpotify.cpp
//  nipinipi
//
//  Created by Nicolas Hognon on 08/04/12.
//  Copyright (c) 2012 ePawn. All rights reserved.
//

#include "PMPlayerSpotifyMixer.h"
#include <stdio.h>
PMPlayerSpotifyMixer::PMPlayerSpotifyMixer(bool random)
:   _random(random),/*_playlist(0),*/_count(0),_indice(0),_link(0),_track(0),_playing(false)
{
}

PMPlayerSpotifyMixer::~PMPlayerSpotifyMixer()
{
}

void PMPlayerSpotifyMixer::connectionSucceeded()
{
    //_playlist = sp_session_starred_create(_session);
}

/*void PMPlayerSpotifyMixer::setIDS(const std::vector<std::string>& ids)
{
    if (ids==_ids) {
        _indice++;
        if (_indice>=_ids.size()) {
            _indice = 0;
        }
    } else {
        _indice = 0;
        _ids = ids;
        if (_ids.empty()) {
            return;
        }
    }

    _chooseTrack();
}*/

void PMPlayerSpotifyMixer::_image_loaded(sp_image *image, void *userdata)
{
    PMPlayerSpotifyMixer* This = (PMPlayerSpotifyMixer*)userdata;
    
    if (image!=This->_image) {
        return;
    }

    std::string name = sp_track_name(This->_track);
    std::string artist = "";
    if (sp_track_num_artists(This->_track)) {
        artist = sp_artist_name(sp_track_artist(This->_track, 0));
    }
    
    size_t img_size = 0;
    const void* img_data = sp_image_data(This->_image, &img_size);
    This->trackReady(name.c_str(),artist.c_str(),sp_track_duration(This->_track),img_data,img_size);
}

/*void PMPlayerSpotifyMixer::_chooseTrack()
{
updated_restart:
    if (_playlist && sp_playlist_is_loaded(_playlist) && !_count) {
        _count = sp_playlist_num_tracks(_playlist);
    }
    
    if (_count && !_track) {
        if (_indice==-1) {
            _indice = _random?(rand()%_count):0;
        }
        _track = sp_playlist_track(_playlist,_indice);
    }
    
    if (_track && sp_track_is_loaded(_track) && !_playing) {
        sp_track_availability tav = sp_track_get_availability(_session,_track);
        if (tav!=SP_TRACK_AVAILABILITY_AVAILABLE) {
            _indice = _random?(rand()%_count):_indice++;
            _track = sp_playlist_track(_playlist,_indice);
            goto updated_restart;
        }
        
        std::string name = sp_track_name(_track);
        std::string artist = "";
        if (sp_track_num_artists(_track)) {
            artist = sp_artist_name(sp_track_artist(_track, 0));
        }
        
        sp_album* album = sp_track_album(_track);
        if (album) {
            const byte* img_id = sp_album_cover(album);
            if (img_id) {
                _image = sp_image_create(_session, img_id);
                if (_image && sp_image_is_loaded(_image)) {
                    size_t img_size = 0;
                    const void* img_data = sp_image_data(_image, &img_size);
                    trackReady(name.c_str(),artist.c_str(),sp_track_duration(_track),img_data,img_size);
                } else {
                    sp_image_add_load_callback(_image, _image_loaded, this);
                    trackReady(name.c_str(),artist.c_str(),sp_track_duration(_track));
                }
            }
        }
        
        sp_session_player_load(_session,_track);
        sp_session_player_play(_session,true);
        _playing = true;
    }    
}*/




