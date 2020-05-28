import requests
import csv
import os
import json
import argparse
import requests
import random
import re

# you can get the user_id  in user dashboard
USER_ID = ""
#------------------------------
count1 = 0
count2 = 0
for jsonfile in os.listdir('real'):
    print("files collected = ", count1)
    print("files skipped = ", count2)
    if os.path.exists("real_image_response"+os.sep+jsonfile):
        count1 += 1
        print("Already got data for ", jsonfile)
        continue

    print("Working on real user: ", jsonfile)
    try:
        current = json.load(open('real'+os.sep+jsonfile,'r'))
        img_list = current['images']
        img_paths = []
        r = []

        print(img_list)
        #Reconfigure the image path to be correct
        for i in range(0, len(img_list)):
            if not os.path.exists(img_list[i]):
                count2 += 1
                print("no image file for that user... skipping")
                continue

            else:
                if img_list[i][0] == ".":
                    img_paths.append(img_list[i][3:])
                    print(img_paths)
                else:
                    img_paths.append(img_list[i])
        if len(img_paths) == 0 or img_paths[0] == 'imgreal/64cf2084dff36a3eda7ffbba3338fee3.png':
            print("invisfile")
            count2 += 1
            continue


        API_URL = "http://facexapi.com/get_image_attr" # face attribute url

        print("Collecting data for ", len(img_paths), " images.")
        for img in img_paths:
            files = {'image_attr': open(img, 'rb')}
            headers = {"user_id": USER_ID}
            temp = (requests.post(API_URL,headers = headers,files = files)) # comment this line to use url image:
            if temp.status_code == 200:
                print("RESPONE OK")

            r.append(json.loads(temp.text))


        with open('real_image_response'+os.sep+jsonfile, 'w') as outfile:
            print("Dumping data for:", jsonfile)
            json.dump(r, outfile)
            count1 += 1
    except Exception as e:
        # os.remove('real'+os.sep+jsonfile)
        print(e)
