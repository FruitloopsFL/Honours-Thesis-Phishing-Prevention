#!/usr/bin/python

import pickle
import os
from data_preprocessing.gibberish_detector.gib_detect_train import avg_transition_prob

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'gib_model.pki')
model_data = pickle.load(open(filename, 'rb'))


def check(str_to_chk):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return avg_transition_prob(str_to_chk, model_mat) > threshold
