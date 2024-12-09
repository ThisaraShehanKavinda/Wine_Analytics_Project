import pandas as pd
import os

data_folder = "./data/raw/"


csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]


data_list = []
for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)
    data_list.append(df)


wine_df = pd.concat(data_list, ignore_index=True)


wine_df.info()



wine_df['Country'] = wine_df['Region'].str.split('/').str[0].str.strip()  
wine_df['Country_Region'] = wine_df['Region'].str.split('/').str[1].str.strip()  


print(wine_df[['Region', 'Country', 'Country_Region']].head())
print(wine_df)


print("\nDuplicate records:")
print(wine_df.duplicated().sum())



print("\null records:")
print(wine_df.isnull().sum())


print("\missing values percentage:")
missing_percentage = (wine_df.isnull().sum() / len(wine_df)) * 100
print(missing_percentage)



wine_df = wine_df.drop(columns=['Grapes'])
print(wine_df)


wine_df = wine_df.dropna(subset=['Wine style'])


wine_df.info()



wine_df.insert(0, "Index", range(1, len(wine_df) + 1))


print(wine_df)





def find_percentile_outliers(df, columns, lower_percentile=1, upper_percentile=99):
    outlier_rows = {}

    for column in columns:
       
        lower_bound = df[column].quantile(lower_percentile / 100)
        upper_bound = df[column].quantile(upper_percentile / 100)
        
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index
        
        
        outlier_row_numbers = df.loc[outliers, 'Index'].tolist()
        
       
        outlier_rows[column] = outlier_row_numbers
    
    return outlier_rows


columns_to_check = ['Rating', 'Price', 'Bold', 'Tannin', 'Sweet', 'Acidic']


outlier_rows = find_percentile_outliers(wine_df, columns_to_check, lower_percentile=1, upper_percentile=99)


for column, rows in outlier_rows.items():
    print(f"Outliers for column '{column}':")
    print(rows)
    print("\n")


print("Interpretation:")
print("Outliers in the 'Rating,' 'Price,' 'Tannin,' 'Sweet,' 'Acidic,' and 'Bold' columns in wines are considered valid and should not be" 
      "removed due to domain-specific reasons. These outliers may represent rare but legitimate cases, such as premium products or exceptional"
      " ratings, which are important for accurately capturing the full range of wine characteristics.")


non_regular_wines = wine_df[(wine_df['Alcohol content'] > 16) | (wine_df['Alcohol content'] < 9)]
print(non_regular_wines)
print("Wines below 9% alcohol are low-alcohol wines, like Moscato or low-alcohol Riesling. Wines above 16% are high-alcohol, typically fortified wines like Port or Sherry.")



wine_df['Food pairings'] = wine_df['Food pairings'].apply(eval) 


all_foods = set(food for sublist in wine_df['Food pairings'] for food in sublist)


for food in all_foods:
    wine_df[food] = wine_df['Food pairings'].apply(lambda x: food in x)


wine_df = wine_df.drop(columns=['Food pairings','Unnamed: 0'])


wine_df['Country_Region'] = wine_df['Country_Region'].fillna('Unknown')


def classify_alcohol(content):
    if content < 9.0:
        return "Low Alcohol Wine"
    elif 9.0 <= content < 11.0:
        return "Medium-Low Alcohol wine"
    elif 11.0 <= content < 14.0:
        return "Standard Alcohol wines"
    elif 14.0 <= content < 16.0:
        return "High Alcohol wines"
    elif content >= 16.0:
        return "High Alcohol wines"
    else:
        return "out of range"
    

wine_df['Alcohol Classification'] = wine_df['Alcohol content'].apply(classify_alcohol)


columns = list(wine_df.columns)
alcohol_idx = columns.index('Alcohol content')  
columns = columns[:alcohol_idx + 1] + ['Alcohol Classification'] + columns[alcohol_idx + 1:-1]
wine_df = wine_df[columns]


print(wine_df)



