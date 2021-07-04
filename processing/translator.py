# THE FOLLOWING PROGRAM TAKES dataframe.csv AND translation.json
# AND OUTPUTS dataframe_translation.csv

# Imports
import csv
import json
from os import chdir
# Getting the dataframe

chdir('processing')

fname_in = "../resources/dataframe.csv"
fname_out = "../resources/dataframe_t.csv"
fname_translation = "../resources/translation.json"

data = list(csv.reader(open(fname_in)))

# Getting the translations
translation_data = dict(json.load(open(fname_translation)))

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
with open(fname_out, "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
