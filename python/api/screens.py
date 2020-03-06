#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch scores across all screens for a single gene
using customizable filtering options
"""

import requests
from python.core import config as cfg
import numpy as np
from sklearn import preprocessing


def get_screens():
    request_url = cfg.BASE_URL + "/screens"

    # These parameters can be modified to match any search criteria following
    # the rules outlined in the Wiki: https://wiki.thebiogrid.org/doku.php/orcs:webservice
    # In this particular instance, we've chosen to limit results to only those in which
    # our gene of interest is considered a hit
    params = {
        "accesskey": cfg.ACCESS_KEY,
        "format": "json"
    }

    r = requests.get(request_url, params=params)
    screens = r.json()
    return screens


def get_features(screens):
    meta = []
    data = []
    screens_with_features = []

    for screen in screens:
        if screen['SCREEN_TYPE'] == 'Negative Selection':
            screen_type = 1
        elif screen['SCREEN_TYPE'] == 'Positive Selection':
            screen_type = 2
        elif screen['SCREEN_TYPE'] == 'Phenotype Screen':
            screen_type = 3
        else:
            continue
        if screen['ENZYME'] == 'CAS9':
            enzyme = 1
        elif screen['ENZYME'] == 'd-Cas9-KRAB':
            enzyme = 2
        elif screen['ENZYME'] == 'SAM (NLS-dCas9-VP64/MS2-p65-HSF1)':
            enzyme = 3
        elif screen['ENZYME'] == 'sunCas9':
            enzyme = 4
        else:
            continue
        if screen['METHODOLOGY'] == 'Activation':
            methodology = 1
        elif screen['METHODOLOGY'] == 'Inhibition':
            methodology = 2
        elif screen['METHODOLOGY'] == 'Knockout':
            methodology = 3
        else:
            continue

        meta.append(
            screen['SCREEN_ID']
        )

        data.append([
            screen['SCORES_SIZE'],
            screen['FULL_SIZE'],
            screen['NUMBER_OF_HITS'],
            screen_type,
            str.split(screen['DURATION'], ' ')[0],
            methodology,
            enzyme
        ])

        screens_with_features.append(screen)

    data_np = np.array(data)
    data_scaled = preprocessing.scale(data_np)
    return type('obj', (object,), {
        'meta': meta,
        'data_scaled': data_scaled
    }), screens_with_features
