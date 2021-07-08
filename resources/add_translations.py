import csv
import json

if __name__=="__main__":

    try:
        # Load existing json file
        translation_json_file = open("translation.json", "r")
        translation_json = json.load(translation_json_file)
    except: #File doesn't exist
        translation_json = dict()


    with open("dataframe_t.csv", "r") as raw_df_file, open("dataframe_trans.csv", "r") as trans_df_file:

        # Load raw dataframe
        reader_raw = csv.reader(raw_df_file)

        # Load translated dataset
        reader_trans = csv.reader(trans_df_file)

        # Check if same length
        if len(list(reader_raw)) == len(list(reader_trans)):
            print("same size")
            # RESET files
            raw_df_file.seek(0)
            trans_df_file.seek(0)

            # If there is a field which doesn't match, add to json trans file
            for raw_row, trans_row in zip(reader_raw, reader_trans):
                for elem_r, elem_t in zip(raw_row, trans_row):
                    if elem_r != elem_t:
                        if '[' in elem_r or ']' in elem_r: # is a list
                            print("FOUND LIST")
                            for c in "[]": # Remove unwanted chars
                                elem_r = elem_r.replace(c, "")
                                elem_t = elem_t.replace(c, "")
                            raw_list = elem_r.split(",")
                            trans_list = elem_t.split(",")
                            for r, t in zip(raw_list, trans_list):
                                translation_json[r.replace("'", "").strip(" ")] = t.replace("'", "").strip(" ")
                                print(r.replace("'", '"'), ":", t.replace("'", '"'))
                        else:
                            translation_json[elem_r] = elem_t

    # Write into json
    with open("translation_t.json", "w", encoding="utf-8") as json_out:
        json.dump(translation_json, json_out, ensure_ascii=False)
