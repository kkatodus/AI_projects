#%%
#imports
import pandas as pd
from api_requests.meeting_convo_collector import MeetingConvoCollector

#%%
#params
DATA_DIR = "./data"



#%%
#class instanciations
mcc = MeetingConvoCollector("https://kokkai.ndl.go.jp/api/speech?")

# %%
