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

# Display the dataframe structure
wine_df.info()


# Split the 'Region' column by '/' and create new columns
wine_df['Country'] = wine_df['Region'].str.split('/').str[0].str.strip()  # First part as 'Country'
wine_df['Country_Region'] = wine_df['Region'].str.split('/').str[1].str.strip()  # Second part as 'Country_Region'

# Display the first few rows to confirm the changes
print(wine_df[['Region', 'Country', 'Country_Region']].head())
print(wine_df)

# Check and display for duplicate rows
print("\nDuplicate records:")
print(wine_df.duplicated().sum())
# no duplicates has found

#check for null values
print("\null records:")
print(wine_df.isnull().sum())

# missing values percentage
print("\missing values percentage:")
missing_percentage = (wine_df.isnull().sum() / len(wine_df)) * 100
print(missing_percentage)
# If fewer than or around 10% of rows are affected, dropping them is often acceptable. 
# Above 30%-40% often impractical to remove rows, as it would lead to significant data loss.

# more than 40% are missing values. By concidering the Grapes column not critical for the analysis:
# Drop the 'Grapes' column from the dataframe
wine_df = wine_df.drop(columns=['Grapes'])
print(wine_df)

# Here, missing values percentage of Wine style is 10% so we can drop the rows with missing.
# Remove rows with missing values in 'Wine style'
wine_df = wine_df.dropna(subset=['Wine style'])

# Display the updated dataframe info
wine_df.info()


# Create a new column with row numbers starting from 1
wine_df.insert(0, "Index", range(1, len(wine_df) + 1))
wine_df.drop(columns=['Unnamed: 0'])

# Display the updated DataFrame
print(wine_df)

# downloading the updated dataframe 
#wine_df.to_csv('output3.csv', index=False)


# Function to find outliers outside the 1st and 99th percentiles
def find_percentile_outliers(df, columns, lower_percentile=1, upper_percentile=99):
    outlier_rows = {}

    for column in columns:
        # Calculate the lower and upper bounds for the percentiles
        lower_bound = df[column].quantile(lower_percentile / 100)
        upper_bound = df[column].quantile(upper_percentile / 100)
        
        # Find the rows where values are outside the percentiles
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index
        
        # Get the "row number" values for the outliers
        outlier_row_numbers = df.loc[outliers, 'Index'].tolist()
        
        # Store the row numbers for outliers in a dictionary
        outlier_rows[column] = outlier_row_numbers
    
    return outlier_rows

# Columns to check for outliers
columns_to_check = ['Rating', 'Price', 'Bold', 'Tannin', 'Sweet', 'Acidic']

# Get the rows with outliers outside the 1st and 99th percentiles
outlier_rows = find_percentile_outliers(wine_df, columns_to_check, lower_percentile=1, upper_percentile=99)

# Print the row numbers of outliers for each column
for column, rows in outlier_rows.items():
    print(f"Outliers for column '{column}':")
    print(rows)
    print("\n")

# the 'Rating' and 'Price' columns show values outside the 1st and 99th percentiles, it is important to recognize that these 
# values might still be valid and meaningful within the context of the dataset.
# There are no absolute "limits" for the values of Tannin, Sweet, Acidic, and Bold in wines, as these attributes can vary widely 
# depending on the grape variety, wine-making process, and style of wine.
print("Interpretation:")
print("Outliers in the 'Rating,' 'Price,' 'Tannin,' 'Sweet,' 'Acidic,' and 'Bold' columns in wines are considered valid and should not be" 
      "removed due to domain-specific reasons. These outliers may represent rare but legitimate cases, such as premium products or exceptional"
      " ratings, which are important for accurately capturing the full range of wine characteristics.")

# Get rows where alcohol content is greater than 16 or less than 9
non_regular_wines = wine_df[(wine_df['Alcohol content'] > 16) | (wine_df['Alcohol content'] < 9)]
print(non_regular_wines)
print("Wines below 9% alcohol are low-alcohol wines, like Moscato or low-alcohol Riesling. Wines above 16% are high-alcohol, typically fortified wines like Port or Sherry.")




# dataframes = []
# for file in csv_files:
#     file_path = os.path.join(data_folder, file)
#     df = pd.read_csv(file_path)
#     dataframes.append(df)  

# print(dataframes)

# print("details")
# print(dataframes["Name"])