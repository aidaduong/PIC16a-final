from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# database = {'johnnypickles':'trucks123','juanpoblano':'CAKE'}
# menu_df = pd.read_pickle('menu.pkl')

@app.route('/')
def home(): 
	return render_template("index.html")

# list of all the products
@app.route('/product_list', methods=["POST"])
def product_list():
	pass

# results of the search
@app.route('/results', methods=["POST"])
def results():
	query = request.form.get("search")
	pass
	
if __name__ == '__main__':
	app.run(debug=True)