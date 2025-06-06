# this script combines all of the other CSVs into a single cleaned CSV
# which can be used in Flask app.py

import pandas as pd

# loading databases
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

database = pd.concat([sunscreen, cleanser, essence, moisturizer, toner], ignore_index=True, axis = 0)

# data cleaning
database['sv_url'] = database['sv_url'].fillna('')
database['ys_url'] = database['ys_url'].fillna('')
database['az_url'] = database['az_url'].fillna('')

database['price'] = database['price'].str.replace('$', '').astype(float)
database['ys_num_reviews'] = database['ys_num_reviews'].fillna(0).astype(int)
database['az_num_reviews'] = database['az_num_reviews'].fillna(0).astype(int)

database.to_csv('data/database.csv', index=False)