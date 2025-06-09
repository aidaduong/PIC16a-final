# this script combines all of the other CSVs into a single cleaned CSV
# which can be used in Flask app.py

import pandas as pd

# loading all the individual product CSVs
cleanser = pd.read_csv('data/cleanser.csv')
cleanser['product'] = 'cleanser'

moisturizer = pd.read_csv('data/moisturizer.csv')
moisturizer['product'] = 'moisturizer'

essence = pd.read_csv('data/essence.csv')
essence['product'] = 'essence'

sunscreen = pd.read_csv('data/sunscreen.csv')
sunscreen['product'] = 'sunscreen'

toner = pd.read_csv('data/toner.csv')
toner['product'] = 'toner'

def combine_data(df_list):
    # concatenate all the dataframes in df_list into a single dataframe
    df = pd.concat(df_list, ignore_index=True, axis=0)

    # fill NAs with empty strings for url columns
    df[['sv_url', 'ys_url', 'az_url']] = df[['sv_url', 'ys_url', 'az_url']].fillna('')
    # fill NAs with empty strings for num_review columns and convert to int
    df[['ys_num_reviews','az_num_reviews']] = df[['ys_num_reviews','az_num_reviews']].fillna(0).astype(int)

    # convert price column to float
    df['price'] = df['price'].str.replace('$', '').astype(float)

    return df

database = combine_data([cleanser, moisturizer, essence, sunscreen, toner])
database.to_csv('data/database.csv', index=False)