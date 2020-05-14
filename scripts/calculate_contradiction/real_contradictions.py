import json
import os
import argparse
import random
import re
import csv

output = {'user_text': {}, 'user_image': {}, 'user_demographic':{}, 'image_demographic':{}}
user_races = {'hispanic': 4643, 'mixed': 844, 'white': 4043, 'pacific islander': 40, 'black': 659, 'asian': 400, 'native american': 107, 'middle eastern': 172, '-': 2}
demographic_races = {'asian': 1271, 'hispanic': 3693, 'white': 3447, 'middle_eastern_north_african': 197, 'black': 997, 'american_indian': 14, 'native_hawaiin': 11}

counter = 0

for jsonfile in os.listdir('data_json/real_combined_responses'):
    if jsonfile == '.DS_Store':
        continue
    data = json.load(open("data_json"+os.sep+'real_combined_responses'+os.sep+jsonfile,'r'))

    ##Which contradictions do we need?
    #TEXT API
    #User age -> Text age
    try:    
        minAge = int(data['text_age'][:2])
        maxAge = abs(int(data['text_age'][2:]))
        if data['user_age'] >= minAge and data['user_age'] <= maxAge:
            output['user_text']['age_inconsistency'] = 1 - data['text_age_confidence']
        elif abs(data['user_age'] - minAge) < 5 or abs(data['user_age'] - maxAge) < 5:
            output['user_text']['age_inconsistency'] = data['text_age_confidence']/2
        else:
            output['user_text']['age_inconsistency'] = data['text_age_confidence']
    except Exception as e:
        print(e)
        output['user_text']['age_inconsistency'] = None


    #User gender -> Text gender
    try:
        if data['text_gender'] != 'unknown':
            if data['user_gender'] == data['text_gender']:
                output['user_text']['gender_inconsistency'] = 1 - data['text_gender_confidence']
            else:
                output['user_text']['gender_inconsistency'] = data['text_gender_confidence']
    except Exception as e:
        print(e)
        output['user_text']['gender_inconsistency'] = None


    #IMAGE API
    #User age -> Image age
    try:
        if data['image_age'][:2] == '0-':
            minAge = 0
        else:
            minAge = int(data['image_age'][:2])
        maxAge = abs(int(data['image_age'][2:]))
        if data['user_age'] >= minAge and data['user_age'] <= maxAge:
            output['user_image']['age_inconsistency'] = 0.0
        elif abs(data['user_age'] - minAge) < 5 or abs(data['user_age'] - maxAge) < 5:
            output['user_image']['age_inconsistency'] = 0.5
        else:
            output['user_image']['age_inconsistency'] = 1.0
    except Exception as e:
        output['user_image']['age_inconsistency'] = None
        print(e)

    #User gender -> Image gender
    try:
        if data['user_gender'] == data['image_gender']:
            output['user_image']['gender_inconsistency'] = 1 - float(data['image_gender_confidence'])
        else:
            output['user_image']['gender_inconsistency'] = data['image_gender_confidence']
    except Exception as e:
        output['user_image']['gender_inconsistency'] = None
        print(e)


    #DEMOGRAPHIC API
    #User age -> Demographic age

    try:
        demographic_age = float(data['demographic_age'])
        if abs(data['user_age'] - demographic_age) < 5:
            output['user_demographic']['age_inconsistency'] = 1 - data['demographic_age_confidence']
        elif abs(data['user_age'] - demographic_age) < 10:
            output['user_demographic']['age_inconsistency'] = data['demographic_age_confidence']/2
        else:
            output['user_demographic']['age_inconsistency'] = data['demographic_age_confidence']
    except Exception as e:
        output['user_demographic']['age_inconsistency'] = None
        print(e)

    #User gender -> Demographic gender
    try:
        if data['user_gender'] == data['demographic_gender']:
            output['user_demographic']['gender_inconsistency'] = 1 - data['demographic_gender_confidence']
        else:
            output['user_demographic']['gender_inconsistency'] = data['demographic_gender_confidence']
    except Exception as e:
        output['user_demographic']['gender_inconsistency'] = None
        print(e)


    #User ethnicity -> Demographic ethnicity
    try:
        if data['user_ethnicity'] == data['demographic_ethnicity']:
            output['user_demographic']['ethnicity_inconsistency'] = 1 - data['demographic_ethnicity_confidence']
        elif data['user_ethnicity'] == 'native american' and data['demographic_ethnicity'] == 'american_indian':
            output['user_demographic']['ethnicity_inconsistency'] = 1 - data['demographic_ethnicity_confidence']
        elif data['user_ethnicity'] == 'middle eastern' and data['demographic_ethnicity'] == 'middle_eastern_north_african':
            output['user_demographic']['ethnicity_inconsistency'] = 1 - data['demographic_ethnicity_confidence']
        else:
            output['user_demographic']['ethnicity_inconsistency'] = data['demographic_ethnicity_confidence']
    except Exception as e:
        output['user_demographic']['ethnicity_inconsistency'] = None
        print(e)

    with open("data_json"+os.sep+"real_contradictions"+os.sep+jsonfile, 'w') as outfile:
        json.dump(output, outfile)
