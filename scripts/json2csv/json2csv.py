import json
import os
import argparse
import random
import re
import csv

output = {}
user_races = {'hispanic': 4643, 'mixed': 844, 'white': 4043, 'pacific islander': 40, 'black': 659, 'asian': 400, 'native american': 107, 'middle eastern': 172, '-': 2}
demographic_races = {'asian': 1271, 'hispanic': 3693, 'white': 3447, 'middle_eastern_north_african': 197, 'black': 997, 'american_indian': 14, 'native_hawaiin': 11}


outfile = open("data_json"+os.sep+"data.csv", 'w')
out = csv.writer(outfile)

out.writerow(["text_age", "text_gender", "image_age", "image_gender", "demographic_age", "demographic_gender", "demographic_ethnicity","labels"])

for jsonfile in os.listdir('data_json/real_contradictions'):
    data = json.load(open("data_json"+os.sep+'real_contradictions'+os.sep+jsonfile,'r'))
    try:
        a = data['user_text']['age_inconsistency']
    except Exception as e:
        a = None

    try:
        b = data['user_text']['gender_inconsistency']
    except Exception as e:
        b = None

    try:
        c = data['user_image']['age_inconsistency']
    except Exception as e:
        print("HERE")
        c = None

    try:
        d = data['user_image']['gender_inconsistency']
    except Exception as e:
        d = None

    try:
        f = data['user_demographic']['age_inconsistency']
    except Exception as e:
        f = None

    try:
        g = data['user_demographic']['gender_inconsistency']
    except Exception as e:
        g = None

    try:
        h = data['user_demographic']['ethnicity_inconsistency']
    except Exception as e:
        h = None

    out.writerow([a,b,c,d,f,g,h,0])

for jsonfile in os.listdir('data_json/scam_contradictions'):
    data = json.load(open("data_json"+os.sep+'scam_contradictions'+os.sep+jsonfile,'r'))
    try:
        a = data['user_text']['age_inconsistency']
    except Exception as e:
        a = None

    try:
        b = data['user_text']['gender_inconsistency']
    except Exception as e:
        b = None

    try:
        c = data['user_image']['age_inconsistency']
    except Exception as e:
        print("HERE")
        c = None

    try:
        d = data['user_image']['gender_inconsistency']
    except Exception as e:
        d = None

    try:
        f = data['user_demographic']['age_inconsistency']
    except Exception as e:
        f = None

    try:
        g = data['user_demographic']['gender_inconsistency']
    except Exception as e:
        g = None

    try:
        h = data['user_demographic']['ethnicity_inconsistency']
    except Exception as e:
        h = None

    out.writerow([a,b,c,d,f,g,h,1])
