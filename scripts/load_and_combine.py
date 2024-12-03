import pandas as pd
import os

data_folder = "./data/raw/"

# get all csv files path to a single list
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Load all CSV files into DataFrames and store them in a list
data_list = []
for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)
    data_list.append(df)

print(data_list[0])




# dataframes = []
# for file in csv_files:
#     file_path = os.path.join(data_folder, file)
#     df = pd.read_csv(file_path)
#     dataframes.append(df)  

# print(dataframes)

# print("details")
# print(dataframes["Name"])