#%%
#imports
import pandas as pd
import os
import re
from params.paths import ROOT_DIR
from api_requests.meeting_convo_collector import MeetingConvoCollector
from file_handling.file_read_writer import read_json, write_json, create_dir, write_file
#%%
global labelled_data_df

#%%
#params
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RESOURCE_DIR = os.path.join(ROOT_DIR, 'resource')
#%%
#class instanciations
mcc = MeetingConvoCollector("https://kokkai.ndl.go.jp/api/speech?")

# %%
labelled_data_exist = False if len(os.listdir(DATA_DIR)) == 0 else True

if labelled_data_exist:
    oldest_labelled_filename = max([os.path.join(DATA_DIR, filename) for filename in os.listdir(DATA_DIR)], key=os.path.getctime)
    print(f"Getting oldest labelled data at {oldest_labelled_filename}")
    labelled_data_df = pd.read_csv(os.path.join(DATA_DIR, oldest_labelled_filename))
    startRecord = list(labelled_data_df["record_position"])[-1]

else:
    print("No labelled data found. Creating new file.")
    labelled_data_df = pd.DataFrame(columns=["speech", "label", "label_id", "record_position"])
    startRecord = 1
    
label2id = read_json(os.path.join(RESOURCE_DIR, "labels.json"))
id2label = {v:k for k, v in label2id.items()}

def check_labelid_input(input):
    if input not in list(id2label.keys()) + ["q"]:
        print("Invalid input. Please try again.")
        return False
    else:
        return True

def iterate_speech_segments(speech):
    for speech_segment in speech.split("。"):
        print(speech_segment)
        is_valid_input = False
        while not is_valid_input:
            label_id = input(f"Please enter the label id or quit by pressing q\n{id2label}: ")
            is_valid_input = check_labelid_input(label_id)
        if label_id == "q":
            print("Quitting...")
            labelled_data_df.to_csv(os.path.join(DATA_DIR, f"labelled_data_{startRecord}.csv"), index=False)
            exit()
        label = id2label[label_id]
        new_row = [speech_segment, label, label_id, record_position]

        if len(new_row) != len(labelled_data_df.columns):
            print("Error: new row has different number of columns than dataframe")
            print("new rows", new_row)
            print("dataframe columns", labelled_data_df.columns)
            exit()
            
        labelled_data_df.loc[len(labelled_data_df)] = new_row
        # labelled_data_df = labelled_data_df._append(pd.Series([speech_segment, label, label_id, record_position], index=labelled_data_df.columns), ignore_index=True)

while True:
    conditions_list = [
    "nameOfHouse=衆議院",
    "recordPacking=json",
    f"startRecord={startRecord}",
    "maximumRecords=100"]
    requests = mcc.make_requests(conditions_list)
    speeches = requests["speechRecord"]
    for idx, speech in enumerate(speeches):
        speech_text = speech['speech']
        speech_text = re.sub(r"^\s+", "", speech_text, flags = re.MULTILINE)
        record_position = startRecord + idx
        iterate_speech_segments(speech_text)


# %%
