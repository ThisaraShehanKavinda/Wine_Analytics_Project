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

# Concatenate the files into a single DataFrame
wine_df = pd.concat(data_list, ignore_index=True)
print(wine_df)

# Split the 'Region' column by '/' and create new columns
wine_df['Country'] = wine_df['Region'].str.split('/').str[0].str.strip()  # First part as 'Country'
wine_df['Country_Region'] = wine_df['Region'].str.split('/').str[1].str.strip()  # Second part as 'Country_Region'

# Display the first few rows to confirm the changes
print(wine_df[['Region', 'Country', 'Country_Region']].head())
print(wine_df)






# dataframes = []
# for file in csv_files:
#     file_path = os.path.join(data_folder, file)
#     df = pd.read_csv(file_path)
#     dataframes.append(df)  

# print(dataframes)

# print("details")
# print(dataframes["Name"])