//
//  PMPlayerSpotify.cpp
//  PartyMixer
//
//  Created by Nicolas Hognon on 08/04/12.
//  Copyright (c) 2012 ePawn. All rights reserved.
//

#include "PMPlayerSpotify.h"
#include <sys/stat.h>

const uint8_t g_appkey[] = {
	0x01, 0xA6, 0x11, 0x7F, 0x0A, 0x80, 0xA1, 0x05, 0x52, 0xA0, 0x73, 0xD8, 0x3A, 0x06, 0x5B, 0xE2,
	0x73, 0x15, 0xA3, 0x96, 0xFA, 0x56, 0x0F, 0xD5, 0x6E, 0x96, 0x4C, 0x99, 0x1F, 0x49, 0x2B, 0xDB,
	0xD0, 0xB7, 0x51, 0x11, 0x6A, 0x57, 0x76, 0x0E, 0x06, 0x9E, 0xCD, 0x93, 0xEE, 0xF7, 0xD9, 0xEB,
	0x75, 0x9A, 0xBC, 0x6A, 0xB4, 0x5F, 0xA7, 0x51, 0xF2, 0x62, 0x17, 0xC5, 0x08, 0x56, 0xD8, 0x26,
	0x55, 0x5C, 0xA6, 0xDF, 0x84, 0x18, 0xC9, 0xE6, 0x5F, 0xCA, 0x54, 0xAE, 0xBA, 0x95, 0x53, 0x5D,
	0x05, 0xAB, 0xE7, 0xA2, 0x28, 0x5E, 0x16, 0xE5, 0x56, 0x22, 0x66, 0xF1, 0x83, 0xA9, 0xB7, 0x45,
	0xD0, 0x88, 0x98, 0x7C, 0x37, 0x0E, 0xCD, 0xFB, 0x67, 0xC6, 0xCE, 0x22, 0x83, 0x97, 0xA6, 0x75,
	0x8C, 0x74, 0x23, 0xEE, 0x75, 0xD0, 0xDF, 0x53, 0x28, 0xDE, 0x3F, 0xED, 0x9B, 0x39, 0x6F, 0x21,
	0xD4, 0x8F, 0xE2, 0x4A, 0x41, 0xA5, 0x39, 0xC1, 0x19, 0x7B, 0x18, 0xFF, 0x5C, 0x34, 0xA1, 0x06,
	0x01, 0x26, 0xDB, 0xC5, 0x26, 0x23, 0xDB, 0x3B, 0xCD, 0xD6, 0xBC, 0xD6, 0xB3, 0xF0, 0x2B, 0x3C,
	0x4D, 0x26, 0xFB, 0xF7, 0xCF, 0x4E, 0xED, 0x8B, 0x24, 0x0B, 0xAF, 0xA6, 0xAF, 0x94, 0xB5, 0x1C,
	0xBA, 0xF1, 0x92, 0x1B, 0xC5, 0xA7, 0xB2, 0x6B, 0xE3, 0x87, 0x40, 0x14, 0xCC, 0x02, 0x32, 0x05,
	0x5B, 0xDD, 0x99, 0xD0, 0xC1, 0x5E, 0x52, 0x3E, 0x51, 0x5D, 0xDC, 0x0D, 0xC6, 0xFA, 0x90, 0xCD,
	0x10, 0x73, 0xE5, 0xA5, 0x03, 0x3A, 0x9E, 0x82, 0x76, 0x5D, 0xB0, 0x8F, 0xE3, 0x3C, 0x95, 0xA1,
	0xE1, 0xD2, 0xBD, 0x11, 0x87, 0x9C, 0xC4, 0xA5, 0x6A, 0xCB, 0x2A, 0xDA, 0x5A, 0xFD, 0xCB, 0x0E,
	0x35, 0x68, 0x21, 0xD8, 0x04, 0x4A, 0x77, 0xAF, 0x69, 0x8B, 0xB8, 0xA9, 0x5A, 0x22, 0xB9, 0x65,
	0x0D, 0x61, 0x34, 0xAB, 0x2A, 0x5F, 0x69, 0xD0, 0xD1, 0x16, 0xF1, 0x43, 0xE8, 0xB7, 0xCF, 0x37,
	0x1A, 0x05, 0x81, 0x45, 0xC4, 0x52, 0x20, 0x97, 0xDB, 0x56, 0xC5, 0xF1, 0x7C, 0x93, 0xD4, 0xE0,
	0x85, 0x09, 0x15, 0x3E, 0xDA, 0xB7, 0x7C, 0x2A, 0x0F, 0xC5, 0x99, 0xB0, 0x36, 0xF0, 0xD8, 0x6A,
	0x44, 0xB9, 0x46, 0x53, 0x1C, 0xE9, 0x13, 0x4A, 0x81, 0x1F, 0x3E, 0x29, 0x69, 0x0B, 0x9D, 0x11,
	0x05,
};
const size_t g_appkey_size = sizeof(g_appkey);

PMPlayerSpotify::PMPlayerSpotify()
:   _session(0),_logfile(0),_elapsed_frames(30*44100)
{
    _init();
}

PMPlayerSpotify::~PMPlayerSpotify()
{
    if (_logfile) {
        fclose(_logfile);
    }
}

bool PMPlayerSpotify::create(bool audio)
{
    LOG("audio=%s",audio?"true":"false");
    
    if (audio) { 
#if defined(USE_AUDIO_OSX)
        _audio_init_osx(&_audiofifo);
#else
        _audio_init_openal(&_audiofifo);
#endif
    }
    
    sp_error err = sp_session_create(&_config, &_session);
    
    if (SP_ERROR_OK != err) {
        fprintf(stderr, "Unable to create session: %s\n", sp_error_message(err));
        return false;
    }
    
    return true;
}

void PMPlayerSpotify::loggin(const char* login, const char* password)
{
    sp_session_login(_session, login, password, 0, NULL);
}

void PMPlayerSpotify::_init()
{
    srand((unsigned int)time(0));
    mkdir("/tmp/PartyMixer",0700);
    _logfile = fopen("/tmp/PartyMixer/partymixer.log", "w");
    
    _callbacks = (sp_session_callbacks){
        .logged_in = PMPlayerSpotify::_logged_in,
        .logged_out = PMPlayerSpotify::_logged_out,
        .metadata_updated = PMPlayerSpotify::_metadata_updated,
        .connection_error = PMPlayerSpotify::_connection_error,
        .message_to_user = PMPlayerSpotify::_message_to_user,
        .notify_main_thread = PMPlayerSpotify::_notify_main_thread,
        .music_delivery = PMPlayerSpotify::_music_delivery,
        .play_token_lost = PMPlayerSpotify::_play_token_lost,    
        .log_message = PMPlayerSpotify::_log_message,
        .end_of_track = PMPlayerSpotify::_end_of_track,
        .streaming_error = PMPlayerSpotify::_streaming_error,    
        .userinfo_updated = PMPlayerSpotify::_userinfo_updated,
        .start_playback = PMPlayerSpotify::_start_playback,
        .stop_playback = PMPlayerSpotify::_stop_playback,
        .get_audio_buffer_stats = PMPlayerSpotify::_get_audio_buffer_stats,    
        .offline_status_updated = PMPlayerSpotify::_offline_status_updated,
        .offline_error = PMPlayerSpotify::_offline_error,
        .credentials_blob_updated = PMPlayerSpotify::_credentials_blob_updated
    };
    
    
    _config = (sp_session_config){
        .api_version = SPOTIFY_API_VERSION,
        .cache_location = "/tmp/PartyMixer/cache",
        .settings_location = "/tmp/PartyMixer/settings",
        .application_key = g_appkey,
        .application_key_size = g_appkey_size,
        .user_agent = "PartyMixer",
        .callbacks = &_callbacks,
        .userdata = this
    };
    
    /* Create session */
    _config.application_key_size = g_appkey_size;
}

void PMPlayerSpotify::_log(const char* func, int line, const char* format, ...)
{
    va_list vl;
    va_start(vl,format);

    fprintf(_logfile,"%s(%d): ",func,line);
    vfprintf(_logfile, format, vl);
    fprintf(_logfile,"\n");
    fflush(_logfile);

    va_end(vl);  
}

void PMPlayerSpotify::_logged_in(sp_session *session, sp_error error)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    if (error !=SP_ERROR_OK) {
        This->connectionFailed();
    } else {
        This->connectionSucceeded();
    }
    
}

void PMPlayerSpotify::_logged_out(sp_session *session)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    This->loggedOut();
}

void PMPlayerSpotify::_metadata_updated(sp_session *session)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    This->updated();
}

void PMPlayerSpotify::_connection_error(sp_session *session, sp_error error)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    This->connectionError(error);
}

void PMPlayerSpotify::_message_to_user(sp_session *session, const char *message)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    LOG_CB(This,"message to user: %s",message);
    This->messageToUser(message);
}

void PMPlayerSpotify::_notify_main_thread(sp_session *session)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    This->notifyMainThread();
}

void PMPlayerSpotify::_log_message(sp_session *session, const char *message)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    LOG_CB(This,"log message: %s",message);
}

void PMPlayerSpotify::_userinfo_updated(sp_session *session)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    This->userUpdated();
}

void PMPlayerSpotify::_offline_status_updated(sp_session *session)
{
}

void PMPlayerSpotify::_offline_error(sp_session *session, sp_error error)
{
}

void PMPlayerSpotify::_credentials_blob_updated(sp_session *session, const char *blob)
{
}

int PMPlayerSpotify::_music_delivery(sp_session *session, const sp_audioformat *format, const void *frames, int num_frames)
{
    PMPlayerSpotify* sp = (PMPlayerSpotify*)sp_session_userdata(session);
    
    audio_fifo_t *af = &sp->_audiofifo;
    audio_fifo_data_t *afd = NULL;
    size_t s;
    
    if (num_frames == 0) {
        return 0; // Audio discontinuity, do nothing
    }
    
    pthread_mutex_lock(&af->mutex);
    
    // Buffer one second of audio
    if (af->qlen > format->sample_rate) {
        pthread_mutex_unlock(&af->mutex);
        return 0;
    }
    
    s = num_frames * sizeof(int16_t) * format->channels;
    
    afd = (audio_fifo_data_t*)malloc(sizeof(audio_fifo_data_t) + s);
    memcpy(afd->samples, frames, s);
    
    afd->nsamples = num_frames;
    
    afd->rate = format->sample_rate;
    afd->channels = format->channels;
    
    TAILQ_INSERT_TAIL(&af->q, afd, link);
    af->qlen += num_frames;
    
    pthread_cond_signal(&af->cond);
    pthread_mutex_unlock(&af->mutex);
    
    sp->_elapsed_frames += num_frames;
    
    float progress = ((float)sp->_elapsed_frames)/((float)format->sample_rate);
    
    sp->progress((int)progress);
    
    return num_frames;        
}

void PMPlayerSpotify::_play_token_lost(sp_session *session)
{
}

void PMPlayerSpotify::_end_of_track(sp_session *session)
{
    PMPlayerSpotify* This = (PMPlayerSpotify*)sp_session_userdata(session);
    This->_elapsed_frames = 30*44100;
    This->endOfTrack(false);
}

void PMPlayerSpotify::_streaming_error(sp_session *session, sp_error error)
{
}

void PMPlayerSpotify::_start_playback(sp_session *session)
{
}

void PMPlayerSpotify::_stop_playback(sp_session *session)
{
}

void PMPlayerSpotify::_get_audio_buffer_stats(sp_session *session, sp_audio_buffer_stats *stats)
{
}
