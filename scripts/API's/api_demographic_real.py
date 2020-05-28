import requests
import csv
import os
import json
import argparse
import requests
import random
import re
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='')
model = app.models.get('demographics')
collected = 0

#------------------------------
count1 = 0
count2 = 0
for jsonfile in os.listdir('real'):
    print(count1, " files collected")
    print(count2, " files skipped")
    if os.path.exists("real_demographic_response"+os.sep+jsonfile):
        count1 += 1
        print("Already got data for ", jsonfile)
        continue

    print("Working on real user: ", jsonfile)
    try:
        current = json.load(open('real'+os.sep+jsonfile,'r'))
        img_list = current['images']
        img_paths = []
        r = []
        if len(img_list) == 0:
            print("No images to send.... skipping ",jsonfile)
            continue

        #Reconfigure the image path to be correct
        for i in range(0, len(img_list)):
            if not os.path.exists(img_list[i]):
                continue
            else:
                if img_list[i][0] == ".":
                    img_paths.append(img_list[i][3:])
                    print(img_paths)
                else:
                    img_paths.append(img_list[i])


        if len(img_paths) == 0 or img_paths[0] == 'imgreal/64cf2084dff36a3eda7ffbba3338fee3.png':
            count2 += 1
            print("no image file for that user... skipping")
            continue


        print("Collecting data for ", len(img_paths), " images.")

        for i in range(0,len(img_paths)):
            temp = model.predict_by_filename(img_paths[i])
            r.append(temp)


        with open('real_demographic_response'+os.sep+jsonfile, 'w') as outfile:
            print("Dumping data for:", jsonfile)
            json.dump(r, outfile)
            count1 += 1
    except Exception as e:
        # os.remove('real'+os.sep+jsonfile)
        print(e)

print("files collected = ", count1)
print("files skipped = ", count2)
