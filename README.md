# Scam Contradiction Detection

Within this zip file I have included all of the necessary code required for this project.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirements needed to run the code for Python 3.

```bash
pip install -r requirements.txt
```

## Usage

Now that Python has all the requirements, the first stage will be to download all the profile data. I have not included this data in the submission due to restrictions from the board of ethics. I made use of the harvester used in the previous work done by Suarez et al. This can be found at [this link](https://github.com/gsuareztangil/automatic-romancescam-digger).

Second stage in the processing of the data is to extract all the necessary data from the API's. Run all the programs in the API folder on each of the downloaded scam and real users. To be able to run this code you have to have been granted access to the needed API keys, or can purchase your own from their respective websites.

Combining the data from all API responses is the next step. The code for this can be found in calculate_contradictions folder. Once all the users are combined, into their respective classes, with necessary values for each feature then run the real_contradictions.py file and scam_contradictions.py. With this, you should now have folders with all the features for each individual user, now anonymous by being represented as a number.

The final stage before using the classifiers is to combine it into a single CSV file. Run the script found in json2csv, and you should have one final .csv file containing all the features.

You can now test out the classifiers found in the classifiers folder. They all make use of 10-fold cross validation, and all output the metrics of how well it performed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
