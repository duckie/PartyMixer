# -*- coding: utf-8 -*-

import subprocess
import os
import arff2libsvm
import extract_audio_features
import utils

model_filename = r'/Users/nicolas/DEV/GIT/PartyMixer/Moteur/model/all_jemo_384_features_2_classes'
audio_dir = utils.get_moteur_dir() + os.path.sep + r'test_wav'
arff_dir = utils.get_moteur_dir() + os.path.sep + r'arff'
predictions_dir = utils.get_moteur_dir() + os.path.sep + r'predictions'
### FIXME
#svm_bin_dir = r'C:\Users\cchastag\Desktop\to_explore\libsvm-3.1\windows'
svm_bin_dir = r'/opt/local/bin'
#open_ear_dir = r'C:\Users\cchastag\Desktop\openEAR-0.1.0'
open_ear_dir = r'/usr/local/bin'


def launchOneTesting_bin(filename) :
    # Scale testing set according to training set's ranges
    cmdline = '%s -r %s %s > %s' % \
        (svm_bin_dir + os.path.sep + 'svm-scale',
         model_filename + '.libsvm.range',
         filename + '.libsvm',
         filename + '.libsvm.scale')
    subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE).communicate()

    # Perform prediction on testing set
    cmdline = '%s %s %s %s' % \
        (svm_bin_dir + os.path.sep + 'svm-predict',
         filename + '.libsvm.scale',
         model_filename + '.libsvm.model',
         filename + '.libsvm.predict')
    subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE).communicate()
    
    return


def get_predictions(prediction_file):
    ftr = open(prediction_file, 'r')
    lines = ftr.readlines()
    results = [elem.strip() for elem in lines]
    ftr.close()
    
    return results


def compute_emotions():
    if len(os.listdir(audio_dir)) == 0:
        return []
    
    # Extract audio features and store them in an ARFF file
    extract_audio_features.extract_audio_features(audio_dir, arff_dir, open_ear_dir)
    
    # Convert the ARFF files into libSVM format
    arff2libsvm.convert(arff_dir + os.path.sep + '384_audio_features.arff',
                        arff_dir + os.path.sep + '384_audio_features.libsvm',
                        verbose = False)
    
    # Launch testing
    launchOneTesting_bin(arff_dir + os.path.sep + '384_audio_features')
    
    # Get predictions
    results = get_predictions(arff_dir + os.path.sep + '384_audio_features.libsvm.predict')
    
    # Remove temp files
    for elem in os.listdir(arff_dir):
        os.remove(os.path.join(arff_dir, elem))
    
    return results
