# -*- coding: utf-8 -*-

import os
import string
import time


def extract_audio_features(audio_dir, arff_dir, open_ear_dir):
    '''final_arff_name = arff_dir + os.path.sep + r'384_audio_features.arff'
    current_arff_name = arff_dir + os.path.sep + r'out.arff'''
    current_arff_name = arff_dir + os.path.sep + r'384_audio_features.arff'
    
    # check that the current_arff doesn't exist and if so, remove it
    if os.path.exists(current_arff_name) :
        os.remove(current_arff_name)
        '''file_open = open(current_arff_name, 'w')
        file_open.close()

    if not os.path.exists(final_arff_name) :
        file_open = open(final_arff_name, 'w')
        file_open.close()'''
        
    first_arff = True
    #final_arff = open(final_arff_name, 'w')
    path = audio_dir
    files = os.listdir(path)
    for filename in files :
        cmd_line = '"' + open_ear_dir + os.path.sep + r'SMILExtract" -C "' + r'/Users/nicolas/DEV/GIT/PartyMixer/Moteur/config/emo_IS09.conf' + '" -I "' + os.path.sep.join([audio_dir, filename]) + '" -O "' + current_arff_name + '"'
        print '\n\n', cmd_line, '\n\n'
        os.system(cmd_line)
        '''current_arff = open(current_arff_name, 'r')
        lines = current_arff.readlines()
        count = 0
        if first_arff == True :
            for i in range(len(lines) - 1, 0, -1) :
                if lines[i].startswith('@attribute emotion') :
                    lines[i] = string.join(lines[i].split(' ')[:-1], ' ')
                    lines[i] += ' {'
                    emotions = emot_dict.values()
                    emotions.sort()
                    for emotion in emotions :
                        lines[i] += emotion + ','
                    lines[i] = lines[i][:-1] + '}\n'
                    count = i
                    #print lines[:i]
                    break
                
            for values in lines[: count + 4] :
                #print values
                final_arff.write(values)
            first_arff = False
        for i in range(len(lines) - 1, 0, -1) :
            if not lines[i].isspace() :
                count = i
                break
        #print filename
        test_string = filename + ',' + string.join(lines[count].split(',')[1:-1], ',') + ',emotion\n'
        #print test_string
        final_arff.write(test_string)
        current_arff.close()
        time.sleep(0.01)
        #os.remove(current_arff_name)
    final_arff.close()'''
