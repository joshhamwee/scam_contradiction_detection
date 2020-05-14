import json
import os
import argparse
import random
import re

unwanted_chars = ".,-_"
wordfreq = {}

for jsonfile in os.listdir('data_json/real_combined_responses'):


    try:
        data = json.load(open("data_json"+os.sep+'real_combined_responses'+os.sep+jsonfile,'r'))
        word = str(data['user_ethnicity'])
        if word not in wordfreq:
            wordfreq[word] = 0
        wordfreq[word] += 1
    except Exception as e:
        # print(jsonfile)
        continue

print(wordfreq)
