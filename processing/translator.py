# THE FOLLOWING PROGRAM TAKES dataframe.csv AND translation.json
# AND OUTPUTS dataframe_translation.csv

# Imports
import csv
import json
from os import chdir
# Getting the dataframe

chdir('scraper')

data = list(csv.reader(open("dataframe.csv")))

# Getting the translations
translation_data = dict(json.load(open("translation.json")))

# Translation mapping function
def translate_from_dict(element, translation_dict):
    try:
        return translation_dict[element]
    except:
        return element

# Translating for every element in "data"
for i, row in enumerate(data):
    for j, elem in enumerate(row):
        data[i][j] = translate_from_dict(elem, translation_data)

# Outputting the resulting file
with open("dataframe_t.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
