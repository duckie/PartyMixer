# -*- coding: utf-8 -*-

##### Useful functions for echonest requests
from pyechonest import config
config.ECHO_NEST_API_KEY="A4A4YZA78BY6QLSW4"

from pyechonest import artist, song, playlist
import cPickle as pickle
import random

# request echonest
def ask_echonest(artist_name):
    # get artist
    artist = artist.search(name = artist_name)[0]
    
    # get song
    song = pyechonest.song.search(artist = artist, max_duration = 240, buckets = ["id:spotify-WW"])[0]
    
    # return song id
    return song.get_tracks('spotify-WW')[0]

# request a list of hot artists from echonest
def getHotArtists():
    return artist.top_hottt()

# get similar artists from an echonest artist object
# min_results : minimal number of results regardless of conditions
# results : wished number of results
def getSimilarArtists(Artist, min_results=15, results=15):
    similar = artist.similar(Artist.name, buckets = ["familiarity", "hotttnesss"], min_results=min_results, results=results)
    return similar

# Returns a list of the main styles for a given artist
def getArtistStyle(Artist, number=10):
    terms = Artist.get_terms(sort='frequency')[:number]
    styles = []    
    for element in terms:
        style = element.values()[1]
        styles.append(style)
    return styles

# Returns a list of artists based on an artist name or style
def getArtistsList(artist_name=None, artist_style=None, number=15):
    return artist.search(name=artist_name, style=artist_style, results=number, fuzzy_match='true')

# get a list of songs using different parameters
#
# style : song style (list)
# mood : song mood (list)
# results : number of results (default 15)
# max and min_tempo default 200 and 80 BPM
# danceability default 0.5->0.8
#
# returns a list of spotify ids
#
def getSongs(style,mood,results=15,max_tempo=200.0,min_tempo=80.0,max_danceability=0.8,min_danceability=0.5):
        
    start_year = random.randint(1970,2012)
    print start_year
    songs = song.search(style=style, mood=mood, results=results,min_tempo=min_tempo,max_tempo=max_tempo,min_danceability=min_danceability,max_danceability=max_danceability,buckets=["id:spotify-WW"],limit='true',max_duration=240, sort='artist_familiarity-asc', artist_start_year_before=start_year)
    
    spotify_songs=[]    
    for element in songs:
        spotify_values = element.get_tracks('spotify-WW')
        spotify_songs.append(spotify_values[0].values()[1])

    return songs

# get a playlist
#
# returns a list of spotify ids
#
def getPlaylist(style,mood,likes, previous,results=15,max_tempo=200.0,min_tempo=80.0,max_d=0.8,min_d=0.5):

    if(len(previous)>0):
        if (likes<-3.3):
            p = playlist.Playlist(type='song-radio', limit='true',variety=0.8, style=style, mood=mood, buckets=["id:spotify-WW"], max_danceability=max_d,min_danceability=min_d,max_tempo=max_tempo,min_tempo=min_tempo)
        elif (likes>3.3):
            p = playlist.Playlist(type='song-radio', limit='true',variety=0.8, style=style, mood=mood, buckets=["id:spotify-WW"], max_danceability=max_d,min_danceability=min_d,max_tempo=max_tempo,min_tempo=min_tempo)
        else:
            p = playlist.Playlist(type='song-radio', limit='true',variety=0.8, style=style, mood=mood, buckets=["id:spotify-WW"], max_danceability=max_d,min_danceability=min_d,max_tempo=max_tempo,min_tempo=min_tempo)
    else:
        p = playlist.Playlist(type='song-radio', limit='true',variety=0.8, style=style, mood=mood, buckets=["id:spotify-WW"], max_danceability=max_d,min_danceability=min_d,max_tempo=max_tempo,min_tempo=min_tempo)

    songs = []
    songs.append(p.get_current_song().get_tracks('spotify-WW')[0].values()[1])
    songs.append(p.get_next_song().get_tracks('spotify-WW')[0].values()[1])
    return songs
    

