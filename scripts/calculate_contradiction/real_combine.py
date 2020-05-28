import json
import os
import argparse
import random
import re


demographics_ids = {'ai_r5F00Gqn': 'white', 'ai_l9ngrR28': 'hispanic', 'ai_659b6V0v':'asian', 'ai_WWxnB3mw': 'american_indian', 'ai_wScNwk9Z':'black', 'ai_bZft5m0H':'middle_eastern_north_african', 'ai_1qp01psl':'native_hawaiin'}
genders_ids = {'ai_zgR2BBt0': 'male', 'ai_cVWr8NK5': 'female'}
counter = 0


output = {}


for jsonfile in os.listdir('data_json/real'):
    output = {}
    user_json = json.load(open("data_json"+os.sep+'real'+os.sep+jsonfile,'r'))

    try:
        user_json = json.load(open("data_json"+os.sep+'real'+os.sep+jsonfile,'r'))
        opened_user = True
    except Exception as e:
        opened_user = False

    try:
        demographic_json = json.load(open("data_json"+os.sep+"real_demographic_response"+os.sep+jsonfile,'r'))
        opened_demographic = True
    except Exception as e:
        opened_demographic = False

    try:
        text_json = json.load(open("data_json"+os.sep+"real_text_response_2"+os.sep+jsonfile,'r'))
        opened_text = True
    except Exception as e:
        opened_text = False

    try:
        image_json = json.load(open("data_json"+os.sep+"real_image_response"+os.sep+jsonfile,'r'))
        opened_image = True
    except Exception as e:
        opened_image = False

    if not opened_demographic and not opened_image and not opened_text:

        # counter += 1
        os.remove("data_json"+os.sep+'real'+os.sep+jsonfile)
        print(counter)
        continue

    #Extract data from user
    try:
        output['user_age'] = int(user_json['age'][:2])
        output['user_gender'] = user_json['gender']
        output['user_ethnicity'] = user_json['ethnicity']
    except Exception as e:
        print("user", e)

    #Extract data from text API response
    try:
        output['text_age'] = text_json['response']['data'][0]['age']
        output['text_age_confidence'] = text_json['response']['data'][0]['confidence_age']
        output['text_gender'] = text_json['response']['data'][0]['gender']
        output['text_gender_confidence'] = text_json['response']['data'][0]['confidence_gender']
    except Exception as e:

        print("text", e)

    #Extract data from image API response
    try:
        output['image_age'] = image_json[0]['data']['attributes']['face_id_0']['age']
        output['image_gender'] = image_json[0]['data']['attributes']['face_id_0']['gender']
        output['image_gender_confidence'] = image_json[0]['data']['attributes']['face_id_0']['gender_confidence']
    except Exception as e:
        print(jsonfile)
        print("IMAGE",e)

    #Extract data from demographic API response
    try:
        data = demographic_json[0]['outputs'][0]['data']['regions'][0]['data']['concepts']
        output['demographic_age'] = data[0]['name']
        output['demographic_age_confidence'] = data[0]['value']

        for i in range(0, len(data)):

            if data[i]['id'] in genders_ids:
                output['demographic_gender'] = genders_ids[data[i]['id']]
                output['demographic_gender_confidence'] = data[i]['value']
                break
        for i in range(0, len(data)):

            if data[i]['id'] in demographics_ids:
                output['demographic_ethnicity'] = demographics_ids[data[i]['id']]
                output['demographic_ethnicity_confidence'] = data[i]['value']
                break
    except Exception as e:
        print("DEMOGRAPHIC",e)

    with open("data_json"+os.sep+'real_combined_responses'+os.sep+str(counter)+'.json', 'w') as outfile:
        counter += 1
        print("Dumping data for:", jsonfile)
        json.dump(output, outfile)
