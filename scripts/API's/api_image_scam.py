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

for jsonfile in os.listdir('scam'):
    try:
        if os.path.exists("scam_image_response"+os.sep+jsonfile):
            print("Already got data for ", jsonfile)
            continue
        print("Working on scam user: ", jsonfile)
        current = json.load(open('scam'+os.sep+jsonfile,'r'))
        img_list = current['images']
        img_paths = []
        r = []
        #Reconfigure the image path to be correct
        for i in range(0, len(img_list)):
            img_paths.append(img_list[i])

        print(img_paths)
        API_URL = "http://facexapi.com/get_image_attr" # face attribute url

        print("Collecting data for ", len(img_paths), " images.")
        for img in img_paths:
            files = {'image_attr': open(img, 'rb')}
            headers = {"user_id": USER_ID}
            temp = (requests.post(API_URL,headers = headers,files = files)) # comment this line to use url image:
            if temp.status_code == 200:
                print("RESPONE OK")
            else:
                print("ERROR")
            r.append(json.loads(temp.text))

        with open('scam_image_response'+os.sep+jsonfile, 'w') as outfile:
            print("Dumping data for:", jsonfile)
            json.dump(r, outfile)
    except Exception as e:
        os.remove('scam'+os.sep+jsonfile)
        print(e)
