import json
import os
import argparse
import random
import re
import csv

output = {'user_text': {}, 'user_image': {}, 'user_demographic':{}, 'image_demographic':{},'api_vs_api':{}}
user_races = {'hispanic': 4643, 'mixed': 844, 'white': 4043, 'pacific islander': 40, 'black': 659, 'asian': 400, 'native american': 107, 'middle eastern': 172, '-': 2}
demographic_races = {'asian': 1271, 'hispanic': 3693, 'white': 3447, 'middle_eastern_north_african': 197, 'black': 997, 'american_indian': 14, 'native_hawaiin': 11}
jsonfile = '18.json'
counter = 0

for jsonfile in os.listdir('data_json/scam_combined_responses'):
    if jsonfile == '.DS_Store':
        continue
    data = json.load(open("data_json"+os.sep+'scam_combined_responses'+os.sep+jsonfile,'r'))


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
        output['user_text']['age_inconsistency'] = None
        pass


    #User gender -> Text gender
    try:
        if data['text_gender'] != 'unknown':
            if data['user_gender'] == data['text_gender']:
                output['user_text']['gender_inconsistency'] = 1 - data['text_gender_confidence']
            else:
                output['user_text']['gender_inconsistency'] = data['text_gender_confidence']
    except Exception as e:
        pass
        output['user_text']['gender_inconsistency'] = None
    #
    #
    # #IMAGE API
    # #User age -> Image age
    age_inconsistency_average = 0
    counter = 0
    for i in range(0,12):
        try:
            if data['image_age_'+str(i)][:2] == '0-':
                minAge = 0
            else:
                minAge = int(data['image_age_'+str(i)][:2])
            maxAge = abs(int(data['image_age_'+str(i)][2:]))
            if data['user_age'] >= minAge and data['user_age'] <= maxAge:
                age_inconsistency_average += 0.0
            else:
                temp1 = abs(data['user_age'] - minAge)
                temp2 = abs(data['user_age'] - maxAge)

                age_inconsistency_average += max(temp1,temp2)
            counter += 1
        except Exception as e:
            pass
    if counter != 0:
        output['user_image']['age_inconsistency'] = age_inconsistency_average/counter
    else:
        output['user_image']['age_inconsistency'] = None

    #
    # #User gender -> Image gender
    gender_inconsistency_average = 0
    counter = 0
    for i in range(0,12):
        try:
            if data['user_gender'] == data['image_gender_'+str(i)]:
                gender_inconsistency_average += 1 - float(data['image_gender_confidence_'+str(i)])
            else:
                gender_inconsistency_average += data['image_gender_confidence_'+str(i)]
            counter += 1
        except Exception as e:
            pass
    if counter != 0:
        output['user_image']['gender_inconsistency'] = gender_inconsistency_average/counter
    else:
        output['user_image']['gender_inconsistency'] = None
    #
    #
    # #DEMOGRAPHIC API
    # #User age -> Demographic age
    #
    age_inconsistency_average = 0
    counter = 0
    for i in range(0,12):
        try:
            demographic_age = float(data['demographic_age_'+str(i)])
            if abs(data['user_age'] - demographic_age) < 5:
                age_inconsistency_average += 1 - data['demographic_age_confidence_'+str(i)]
            elif abs(data['user_age'] - demographic_age) < 10:
                age_inconsistency_average += data['demographic_age_confidence_'+str(i)]/2
            else:
                age_inconsistency_average += data['demographic_age_confidence_'+str(i)]
            counter += 1
        except Exception as e:
            pass

    if counter != 0:
        output['user_demographic']['age_inconsistency'] = age_inconsistency_average/counter
    else:
        output['user_demographic']['age_inconsistency'] = None


    #
    # #User gender -> Demographic gender
    gender_inconsistency_average = 0
    counter = 0
    for i in range(0,12):
        try:
            if data['user_gender'] == data['demographic_gender_'+str(i)]:
                gender_inconsistency_average += 1 - data['demographic_gender_confidence_'+str(i)]
            else:
                gender_inconsistency_average += data['demographic_gender_confidence_'+str(i)]
            counter += 1
        except Exception as e:
            pass

    if counter != 0:
        output['user_demographic']['gender_inconsistency'] = gender_inconsistency_average/counter
    else:
        output['user_demographic']['gender_inconsistency'] = None
    #
    # #User ethnicity -> Demographic ethnicity
    ethnicity_inconsistency_average = 0
    counter = 0
    for i in range(0,12):
        try:
            if data['user_ethnicity'] == data['demographic_ethnicity_'+str(i)]:
                ethnicity_inconsistency_average += 1 - data['demographic_ethnicity_confidence_'+str(i)]
            elif data['user_ethnicity'] == 'native american' and data['demographic_ethnicity_'+str(i)] == 'american_indian':
                ethnicity_inconsistency_average += 1 - data['demographic_ethnicity_confidence_'+str(i)]
            elif data['user_ethnicity'] == 'middle eastern' and data['demographic_ethnicity_'+str(i)] == 'middle_eastern_north_african':
                ethnicity_inconsistency_average += 1 - data['demographic_ethnicity_confidence_'+str(i)]
            else:
                ethnicity_inconsistency_average += data['demographic_ethnicity_confidence_'+str(i)]
            counter += 1
        except Exception as e:
            pass

    if counter != 0:
        output['user_demographic']['ethnicity_inconsistency'] = ethnicity_inconsistency_average/counter
    else:
        output['user_demographic']['ethnicity_inconsistency'] = None


    gender_inconsistency_average_2 = 0
    counter = 0
    for i in range(0,12):
        try:
            if  data['demographic_gender_'+str(i)] == data['image_gender_'+str(i)]:
                gender_inconsistency_average_2 += ((1 - float(data['image_gender_confidence_'+str(i)]))+(1 - data['demographic_gender_confidence_'+str(i)]))/2
            else:
                gender_inconsistency_average_2 += (data['image_gender_confidence_'+str(i)]+data['demographic_gender_confidence_'+str(i)])/2
            counter += 1
        except Exception as e:
            pass

    if counter != 0:
        output['api_vs_api']['image_image_gender'] = gender_inconsistency_average_2/counter
    else:
        output['api_vs_api']['image_image_gender'] = None


    age_inconsistency_average = 0
    counter = 0
    for i in range(0,12):
        try:
            minAge = int(data['text_age'][:2])
            maxAge = abs(int(data['text_age'][2:]))

            demographic_age = float(data['demographic_age_'+str(i)])
            if demographic_age >= minAge and demographic_age <= maxAge:
                age_inconsistency_average += 0.0
            else:
                temp1 = abs(data['user_age'] - minAge)
                temp2 = abs(data['user_age'] - maxAge)

                age_inconsistency_average += max(temp1,temp2)
            counter += 1
        except Exception as e:
            pass

    if counter != 0:
        output['api_vs_api']['text_image_age'] = age_inconsistency_average/counter
    else:
        output['api_vs_api']['text_image_age'] = None

    with open("data_json"+os.sep+"scam_contradictions_2"+os.sep+jsonfile, 'w') as outfile:
        json.dump(output, outfile)
