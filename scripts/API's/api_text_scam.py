import csv
import os
import json
import argparse
import requests
import random
import re

#reals = [json.load(open('testReal'+os.sep+jsonfile,'r')) for jsonfile in os.listdir('testReal')]
counter = 0
for jsonfile in os.listdir('scam'):
    try:
        current = json.load(open('scam'+os.sep+jsonfile,'r'))
        url = "http://api.ai-applied.nl/api/demographics_api/?request="
        json_data = {
   "data":{
      "api_key":"",
      "call":{
         "return_original":True,
         "data":[
            {
               "text":current['description'],
               "language_iso":"eng",
               "user":current['name'],
               "id":1
            }
         ]
      }
   }
}
        finalURL = url + json.dumps(json_data)

        response = requests.get(finalURL)
        print(response.json())
        with open('scam_text_response'+os.sep+jsonfile+".json", 'w') as outfile:
            json.dump(response.json(), outfile)
    except Exception as this:
        print(this)

    #print(jsonfile)
