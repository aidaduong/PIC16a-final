from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

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
database['price'] = database['price'].str.replace('$', '').astype(float)
database['ys_num_reviews'] = database['ys_num_reviews'].fillna(0).astype(int)
database['az_num_reviews'] = database['az_num_reviews'].fillna(0).astype(int)

# homepage
@app.route('/')
def home(): 
	return render_template("index.html")

# list of all the products
@app.route('/product_list', methods=["GET","POST"])
def product_list():
	return render_template('product_list.html', products=database.to_dict('records'))

# list of all cleansers
@app.route('/cleanser')
def cleanser():
	cleansers = database[database['product'] == 'cleanser']
	return render_template('cleanser.html', cleansers=cleansers.to_dict('records'))

# list of all moisturizers
@app.route('/moisturizer')
def moisturizer():
	moisturizers = database[database['product'] == 'moisturizer']
	return render_template('moisturizer.html', moisturizers=moisturizers.to_dict('records'))

# list of all essences
@app.route('/essence')
def essence():
	essences = database[database['product'] == 'essence']
	return render_template('essence.html', essences=essences.to_dict('records'))

# list of all sunscreens
@app.route('/sunscreen')
def sunscreen():
	sunscreens = database[database['product'] == 'sunscreen']
	return render_template('sunscreen.html', sunscreens=sunscreens.to_dict('records'))

# list of all toners
@app.route('/toner')
def toner():
	toners = database[database['product'] == 'toner']
	return render_template('toner.html', toners=toners.to_dict('records'))

# logic to decide which template file to call based on procuct type
@app.route('/product/<product_type>/<name>')
def product(product_type, name):
	product = database[database['name'] == name]
	return render_template('product_page.html', product = product.to_dict('records')[0])

# results of the search
@app.route('/results', methods=["GET","POST"])
def results():
	query = request.form.get("search")
	pass
	
if __name__ == '__main__':
	app.run(debug=True)