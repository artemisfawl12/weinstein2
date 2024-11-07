import copy
import pickle
import datetime

with open("name_date_MA_state_df.pkl", "rb") as f2:
    name_date_MA_state_df = pickle.load(f2)
for i in range(50,55):
    print(name_date_MA_state_df["LG전자우"].iloc[i])