import csv
import os
import json
import argparse
import requests
import random
import re

#reals = [json.load(open('testReal'+os.sep+jsonfile,'r')) for jsonfile in os.listdir('testReal')]
counter = 0
for jsonfile in os.listdir('real'):
    try:
        current = json.load(open('real'+os.sep+jsonfile,'r'))
        if current['ethnicity'] == 'hispanic':
            lang = "spa"
        else:
            lang = "eng"
        if current['description'] != "-":
            url = "http://api.ai-applied.nl/api/demographics_api/?request="
            json_data = {
       "data":{
          "api_key":"",
          "call":{
             "return_original":True,
             "data":[
                {
                   "text":current['description'],
                   "language_iso":lang,
                   "user":current['username'],
                   "id":1
                }
             ]
          }
       }
    }
            finalURL = url + json.dumps(json_data)

            response = requests.get(finalURL)
            print(response.json())
            with open('real_text_response_2'+os.sep+jsonfile, 'w') as outfile:
                json.dump(response.json(), outfile)
    except Exception as this:
        print(this)

    #print(jsonfile)
