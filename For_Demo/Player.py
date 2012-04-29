#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
import decision
import urllib2
import compute_emotion
import extract_audio_features
import echonest_helper as helper
import cPickle as pickle
import tempfile
import os
import pyechonest
import random
import bisect
import sys
from copy import deepcopy
import utils
import thread

song_name = "None"

class GTK_Main:
    
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("PartyMixer")
        window.set_default_size(300, -1)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)

        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()

        vbox.add(self.textview)
        self.textview.show()
        self.textview.set_editable(False)
        self.textview.set_justification(gtk.JUSTIFY_CENTER)
        self.textbuffer.set_text("Song title : " + song_name)


        self.PlayButton = gtk.Button("Play/Switch")
        self.StopButton = gtk.Button("Stop")
        self.RecordButton = gtk.Button("Record")
        self.PlayButton.connect("clicked", self.play)
        self.StopButton.connect("clicked", self.stop)
        self.RecordButton.connect("clicked", self.record)
        vbox.add(self.PlayButton)
        vbox.add(self.StopButton)
        vbox.add(self.RecordButton)

        window.show_all()
        
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def returnOneSong(self):
        song_url = ''
        artist = ''
        song_name = ''
        songs = []
        while (True):
            songs = decision.process_server_results()
            if ( (songs[0]!=[]) or (songs[1]!=[])):
                break
 

        for s in songs:
            if (s!=[]):
                song_url = s.get_tracks('7digital-US')[0]['preview_url'] 
                artist = s.artist_name
                song_name = s.title
            else:
                song_url = s.get_tracks('7digital-US')[0]['preview_url'] 
                artist = s.artist_name
                song_name = s.title

        # flushes votes database only when we have a new song
        flush_url = "http://partymixer3.appspot.com/flush"
        req = urllib2.Request(flush_url)
        urllib2.urlopen(req)

        return [song_url,artist,song_name]


    def play(self, w):
        # Ici on met l'appel a decision.py
        
        # Decision.py renvoie une url de preview 7-digital

        '''song_files = ['None','None']

        while ((song_files[0] == 'None') and (song_files[1] =='None')):
            song_files = []
            songs = decision.process_server_results()
            for s in songs:
                try:
                    song_files.append( s.get_tracks('7digital')[0]['preview_url'] )
                except:
                    song_files.append('None')
                print song_files

        if (song_files[0] != 'None'):
            mp3file = song_files[0]
        else:
            mp3file = song_files[1]'''

        song_info = self.returnOneSong()
        self.textbuffer.set_text(song_info[2] + " by " + song_info[1])

                

        # Fonction pour lire l'audio 
        #self.player.set_property("uri", mp3file)
        self.player.set_state(gst.STATE_NULL)       
        self.player.set_property("uri",  song_info[0])
        self.player.set_state(gst.STATE_PLAYING)
        return 0

    def record(self,w):
        # enregistrer un son, ligne commande
        # rec -b 16 test_wav/sample.wav trim 0 00:05
        if (os.path.isfile("test_wav/sample.wav")):
            os.remove("test_wav/sample.wav")
        
        os.system("rec -c 1 -r 16000 -b 16 test_wav/sample.wav trim 0 00:05")

    def stop(self, w):
        self.player.set_state(gst.STATE_NULL)
                        
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            #self.PlayButton.set_label("Start")
            self.play("clicked")#print "bouh"
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.PlayButton.set_label("Start")

GTK_Main()
gtk.gdk.threads_init()
gtk.main()
