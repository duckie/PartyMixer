# -*- coding: utf-8 -*-

##### Module decision
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

temp_file = tempfile.gettempdir() + os.path.sep + 'data.pickle'

#from pyechonest import artist, song, playlist

get_vote_url = "http://partymixer3.appspot.com/get_votes"
flush_url = "http://partymixer3.appspot.com/flush"
votes_keys = ["mood", "likes"]

# Default Moods and Styles
moods = ['bouncy','cheerful','funky','groovy','party music']
all_styles = ['jazz','funk','rock','disco','fusion','lounge','ambient','classic rock','soul','ska', 'big bang', 'blues', 'bossa nova','gospel','gipsy','motown']
#styles = random.sample(all_styles,3)

# Moods for different situations
    # First, the people beat desire (upbeat, normal,slow)
moods_upbeat = ['sad','hypnotic','laid-back','futuristic','bouncy','groovy','lively','party music','funky','aggressive','angry']
moods_normal =['sad','relax','quiet','gloomy','ambient','relax','quiet','cool','party music', 'fun','gleeful','funky','aggressive','rebellious']
moods_slow = ['sad','calming','dreamy','gloomy','melancholia','cold','intimate', 'dramatic', 'quiet', 'relax', 'calming', 'dreamy','fun','party music' 'gleeful','joyous','manic', 'rebellious']

    # Then, the peoples emotions
moods_e_sadness = ['sad','hypnotic','relax','quiet','gloomy','calming','dreamy','gloomy','melancholia','cold']
moods_e_neutral = ['laid-back','futuristic','ambient','relax','quiet','cool','intimate', 'dramatic', 'calming', 'dreamy']
moods_e_happiness = ['bouncy','groovy','lively','party music','funky','fun']#,'gleeful','joyous']
moods_e_anger = ['aggressive','angry','rebellious','manic']

moods_active = moods_e_happiness #+ moods_e_anger
moods_passive = moods_e_sadness #+ moods_e_neutral


# Emotions
#emotions = ['anger', 'happiness', 'neutral', 'sadness']
emotions = ['active', 'passive']


# pull results from server and flushes database
def get_results_from_server():
    # make request and get results
    req = urllib2.Request(get_vote_url)
    response = urllib2.urlopen(req)
    page = response.read()

    #unpickle results
    results = pickle.loads(page)
    
    # flushes database
    #req = urllib2.Request(flush_url)
    #urllib2.urlopen(req)

    # return results
    return results


def process_emotion_results():
    results = compute_emotion.compute_emotions()

    if(len(results)==0):
        return 'active'
    
    found_emotions = [emotions[int(elem) - 1] for elem in results]
    
    # trouver l'emotion majoritaire
    count_emotions = dict(zip(emotions, [0 for i in range(len(emotions))]))
    for elem in found_emotions:
        count_emotions[elem] += 1
    majoritary_emotion = max(count_emotions, key = count_emotions.get)
    
    return majoritary_emotion

# Intersection of two lists
def intersect(a, b):
     return list(set(a).intersection(set(b)))

# process server results
# gets the votes from the web app
# return all the votes, and their mean value for each type of vote (likes, mood)
def process_server_results():
    results = get_results_from_server()
    #print results
    try:
        processed_results = dict([[key, sum(results[key])/len(results[key])] for key in votes_keys])
    except:
        processed_results = {"mood" : 0, "likes" : 0}

    wished_tempo = processed_results.values()[0]
    likes = processed_results.values()[1]

    if (wished_tempo<-3.3):
        peoples_mood = moods_slow
    elif (wished_tempo>3.3):
        peoples_mood = moods_upbeat
    else:
        peoples_mood = moods_normal

    emotion = process_emotion_results()
    print emotion

    if (emotion=='passive'):
        used_mood = intersect(peoples_mood,moods_passive)
    else:
        used_mood = intersect(peoples_mood,moods_active)
    
    previous_songs = []
    songs =[]
    min_d = 0.4
    weighted_styles = {}
    
    try:
        previous = pickle.load( open( temp_file, "rb" ) )    
        min_d = previous["danceability"]
        previous_songs = previous["spotify-ids"]
        previous_styles = previous["previous_styles"]
        weighted_styles = previous["weighted_styles"]
    except:
        min_d=0.4
        previous_styles = []
        previous_songs = []
        weighted_styles = {'jazz':50,'funk':50,'rock':50,'disco':50,'electro':50,'fusion':50,'lounge':50,'ambient':50,'classic rock':50,'dub':50,'metal':50,'ska':50,'soul':50,'techno':50,'trance':50}

    if (emotion == 'passive'):
        min_d -= 0.4
    else:
        min_d += 0.4

    min_d = min(min_d + wished_tempo/10.0,0.8)
    min_d = max(min_d,0)    

    max_d = min_d + 0.2

    update_style_weights(dico=weighted_styles,likes=likes,previous_styles=previous_styles)
    styles = random_triple_weighted(weighted_styles)
    
    songs = helper.getPlaylist(style=styles,mood=peoples_mood,max_d=max_d,min_d=min_d, likes=likes, previous=previous_songs)

    if (emotion == 'passive'):
        used_data = {"danceability": min_d + 0.4, "spotify-ids": songs, "previous_styles": styles, "weighted_styles":weighted_styles}
    else:
        used_data = {"danceability": min_d - 0.4, "spotify-ids": songs, "previous_styles": styles, "weighted_styles":weighted_styles}
    
    pickle.dump( used_data, open( temp_file, "wb" ) )
    

    return songs


# Random weighted choice 
#
# argument d : dictionary with syles as keys, and weights as values
#
# returns a list of 3 styles
def random_triple_weighted(d):
    
    tirage=[]

    dico = deepcopy(d)

    items, total = [], 0
    for key, value in dico.items():
        total += value
        items.append((total, key))

    tire = items[bisect.bisect_left(items, (random.randint(1, total),))][1]
    tirage.append(tire)
    dico.pop(tire)

    items, total = [], 0
    for key, value in dico.items():
        total += value
        items.append((total, key))

    tire = items[bisect.bisect_left(items, (random.randint(1, total),))][1]
    tirage.append(tire)
    dico.pop(tire)

    items, total = [], 0
    for key, value in dico.items():
        total += value
        items.append((total, key))

    tire = items[bisect.bisect_left(items, (random.randint(1, total),))][1]
    tirage.append(tire)
    dico.pop(tire)
    
    return tirage

# Update the weights in dico (dictionary with styles and weights)
#
# likes : user 'like' input about the previous song
# previous_styles : styles used to generate the previous song
#
# returns an updated dictionary with updated weights
def update_style_weights(dico,likes,previous_styles):
    if (len(previous_styles) >0):
        if (likes != 0):
            for style in previous_styles:
                dico[style] += 2*likes
                dico[style] = max(dico[style],1)
                dico[style] = min(dico[style],100)
            return dico
    else:
        return dico



'''if __name__ == "__main__":
    #process_emotion_results()
    print process_server_results()     
    #for s in songs:
	#print s'''
