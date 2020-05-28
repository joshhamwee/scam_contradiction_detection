from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import requests
import csv
import os
import json
import argparse
import requests
import random
import re

app = ClarifaiApp(api_key='')
model = app.models.get('demographics')
collected = 0

for jsonfile in os.listdir('scam'):
    print(collected, " Collected so far")
    try:
        if os.path.exists("scam_demographic_response"+os.sep+jsonfile):
            print("Already got data for ", jsonfile)
            collected += 1
            continue

        print("Working on scam user: ", jsonfile)
        current = json.load(open('scam'+os.sep+jsonfile,'r'))
        img_list = current['images']
        img_paths = []
        r = []

        #Reconfigure the image path to be correct
        #Not an issue with the scam accounts
        for i in range(0, len(img_list)):
            img_paths.append(img_list[i])

        print(img_paths)




        print("Collecting data for ", len(img_paths), " images.")

        for i in range(0,len(img_paths)):
            temp = model.predict_by_filename(img_paths[i])
            r.append(temp)


        with open('scam_demographic_response'+os.sep+jsonfile, 'w') as outfile:
            collected += 1
            print("Dumping data for:", jsonfile)
            json.dump(r, outfile)
    except Exception as e:
        # os.remove('scam'+os.sep+jsonfile)
        print(e)
