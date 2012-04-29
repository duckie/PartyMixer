//
//  PMPlayerSpotifyOSX.cpp
//  //  PartyMixer//  PartyMixer
//
//  Created by Nicolas Hognon on 08/04/12.
//  Copyright (c) 2012 ePawn. All rights reserved.
//

#include "PMPlayerSpotifyOSX.h"
#include <sys/time.h>
#import "AppDelegate.h"
#include <stdio.h>
#include <string.h>

PMPlayerSpotifyOSX::PMPlayerSpotifyOSX(AppDelegate* appDelegate, bool random)
: PMPlayerSpotifyMixer(random), _appDelegate(appDelegate)
{
    _threadRunning = false;
}

PMPlayerSpotifyOSX::~PMPlayerSpotifyOSX()
{
}

void PMPlayerSpotifyOSX::connectionFailed()
{
    [_appDelegate connectionFailed];
}

void PMPlayerSpotifyOSX::connectionSucceeded()
{
    PMPlayerSpotifyMixer::connectionSucceeded();
    [_appDelegate connectionSucceeded];
    callEngine();
}

void PMPlayerSpotifyOSX::notifyMainThread()
{
	[_appDelegate performSelectorOnMainThread:@selector(processEvents) withObject:nil waitUntilDone:NO];
}


void PMPlayerSpotifyOSX::endOfTrack(bool forced)
{
    _link = 0;
    _track = 0;
    _indice++;
    _playing = false;
    callEngine();
    //_chooseTrack();
}

void PMPlayerSpotifyOSX::trackReady(const char* name, const char* artist, int duration)
{
    [_appDelegate newTrack: [NSString stringWithCString:name encoding:NSUTF8StringEncoding] withArtiste:[NSString stringWithCString:artist encoding:NSUTF8StringEncoding] withDuration:duration];
}

void PMPlayerSpotifyOSX::trackReady(const char* name, const char* artist, int duration, const void* img_data, size_t img_size)
{
    NSData* data = [NSData dataWithBytes:img_data length:img_size];
    NSImage* nsimg = [[NSImage alloc] initWithData:data];
    [_appDelegate newTrack:[NSString stringWithCString:name encoding:NSUTF8StringEncoding] withArtiste:[NSString stringWithCString:artist encoding:NSUTF8StringEncoding] withDuration:duration andImage:nsimg];
}

void PMPlayerSpotifyOSX::updated()
{
    _chooseTrack();
}

void PMPlayerSpotifyOSX::progress(int second)
{
    [_appDelegate progress:second];
}

static void* callEngine_threadfunc(void *aux)
{
    PMPlayerSpotifyOSX* This = (PMPlayerSpotifyOSX*)aux;
    system("python /Users/nicolas/DEV/GIT/PartyMixer/Moteur/decision.py > /tmp/partymixer.log");
    FILE* f = fopen("/tmp/partymixer.log","r");
    if (!f) {
        return 0;
    }
    char buffer[1024];
    std::vector<std::string> vectors;
    while (fgets(buffer,1024,f)) {
        printf("buffer: %s",buffer);
        if (strstr(buffer,"spotify-WW")!=buffer) {
            printf("not spotify line\n");
            continue;
        }
        const char* ptr = strchr(buffer,':');
        if (ptr) {
            ptr = strchr(ptr+1,':');
            if (ptr+1) {
                std::string s = "spotify:track:";
                s += ptr+1;
                s[s.size()-1] = '\0';
                printf("spotify track id: %s\n",s.c_str());
                vectors.push_back(s);
            }
        }
    }
    
    This->_elapsed_frames = 30*44100;
    This->_indice = 0;
    This->_ids = vectors;
    This->_threadRunning = false;
	[This->_appDelegate performSelectorOnMainThread:@selector(chooseTrack) withObject:nil waitUntilDone:NO];
    return 0;
}

void PMPlayerSpotifyOSX::callEngine()
{
    if (_threadRunning) {
        return;
    }
    pthread_t tid;
    pthread_create(&tid, NULL, callEngine_threadfunc, this);
    _threadRunning = true;
}

void PMPlayerSpotifyOSX::_chooseTrack()
{
    if (_threadRunning) {
        return;
    }
    
updated_restart:
    
    if (!_link) {
        if (_ids.empty()) {
            return;
        }
        std::string str = _ids[_indice];
        _link = sp_link_create_from_string (str.c_str());
        if (!_link) {
            goto updated_restart;
        }
        sp_linktype tlink = sp_link_type(_link);
        if (tlink!=SP_LINKTYPE_TRACK) {
            goto updated_restart;
        }
        _track = sp_link_as_track(_link);
        printf("link ok\n");
    }
    
    if (_track && sp_track_is_loaded(_track) && !_playing) {
        sp_track_availability tav = sp_track_get_availability(_session,_track);
        if (tav!=SP_TRACK_AVAILABILITY_AVAILABLE) {
            printf("track is not available\n");
            _link = 0;
            _track = 0;  
            _indice++;
            if (_indice==_ids.size()) {
                printf("RECALL ENGINE !!!\n");
                callEngine();
                return;
            }
            goto updated_restart;
        }
        
        std::string name = sp_track_name(_track);
        printf("track: %s\n",name.c_str());
        std::string artist = "";
        if (sp_track_num_artists(_track)) {
            artist = sp_artist_name(sp_track_artist(_track, 0));
            printf("artist: %s\n",artist.c_str());
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
#if defined(USE_AUDIO_OSX)
        _audio_fifo_flush_osx(&_audiofifo);
#else
        _audio_fifo_flush_openal(&_audiofifo);
#endif
        sp_session_player_play(_session,true);
        sp_session_player_seek(_session, 30000);
        printf("play ...\n");
        _playing = true;
    }
}



