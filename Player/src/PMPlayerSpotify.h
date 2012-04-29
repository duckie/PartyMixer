//
//  PMPlayerSpotify.h
//  //  PartyMixer//  PartyMixer
//
//  Created by Nicolas Hognon on 08/04/12.
//  Copyright (c) 2012 ePawn. All rights reserved.
//

#ifndef _PMPlayerSPOTIFY_H_
#define _PMPlayerSPOTIFY_H_

#include <string>
#include <map>
#include <libspotify/api.h>
#include "audio.h"

#define LOG_S(log) _log(__PRETTY_FUNCTION__,__LINE__,log)
#define LOG(log,...) _log(__PRETTY_FUNCTION__,__LINE__,log,__VA_ARGS__)
#define LOG_CB_S(p,log) p->_log(__PRETTY_FUNCTION__,__LINE__,log)
#define LOG_CB(p,log,...) p->_log(__PRETTY_FUNCTION__,__LINE__,log,__VA_ARGS__)

#define USE_AUDIO_OSX 1

class PMPlayerSpotify
{
public:

    PMPlayerSpotify();
    virtual ~PMPlayerSpotify();
    
    bool create(bool audio);
    void loggin(const char* login, const char* password);

    sp_session* getSession()
    {
        return _session;
    }
    
    virtual void connectionFailed() {}
    virtual void connectionSucceeded() {}
    virtual void loggedOut() {}
    virtual void updated() {}
    virtual void connectionError(sp_error error) {}
    virtual void messageToUser(const char* message) {}
    virtual void notifyMainThread() {}
    virtual void userUpdated() {}
    virtual void endOfTrack(bool forced) {}
    virtual void progress(int second) {}

    sp_session* _session;

    static void _logged_in(sp_session *session, sp_error error);
    static void _logged_out(sp_session *session);
    static void _metadata_updated(sp_session *session);
    static void _connection_error(sp_session *session, sp_error error);
    static void _message_to_user(sp_session *session, const char *message);
    static void _notify_main_thread(sp_session *session);
    static void _log_message(sp_session *session, const char *message);
    static void _userinfo_updated(sp_session *session);
	static void _offline_status_updated(sp_session *session);
	static void _offline_error(sp_session *session, sp_error error);
	static void _credentials_blob_updated(sp_session *session, const char *blob);
    static int  _music_delivery(sp_session *session, const sp_audioformat *format, const void *frames, int num_frames);
    static void _play_token_lost(sp_session *session);
    static void _end_of_track(sp_session *session);
    static void _streaming_error(sp_session *session, sp_error error);
	static void _start_playback(sp_session *session);
	static void _stop_playback(sp_session *session);
	static void _get_audio_buffer_stats(sp_session *session, sp_audio_buffer_stats *stats);
    
    bool _audio_init_openal(audio_fifo_t *af);
    void _audio_fifo_flush_openal(audio_fifo_t *af);
    bool _audio_init_osx(audio_fifo_t *af);
    void _audio_fifo_flush_osx(audio_fifo_t *af);
    
    void _init();
    void _log(const char* func, int line, const char* format, ...);
    
    FILE* _logfile;
    int _elapsed_frames;
    
    audio_fifo_t _audiofifo;
    sp_session_callbacks _callbacks;
    sp_session_config _config;
};

#endif // _PMPlayerSPOTIFY_H_
