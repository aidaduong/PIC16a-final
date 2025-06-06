What the project does:

  The scraper.py file scrapes Stylevana, an Asian skincare shopping website. It scrapes the first 3 pages (by popularity) of 5 different skincare product types: cleansers, moisturizers, essence/serums, sunscreens, and toners. It retrieves the URL, name, brand, price, rating, etc. of the each category.
  The app.py file creates a webpage, where the user can search for a product by its name or brand. There are also pages for a list of all products and a complete list of each product type. Each product page has the basic information that was scraped using scraper.py, as well as links to and ratings from Stylevana, Yesstyle, and/or Amazon.

  
How to install dependencies:

  To install dependencies, simply pip install in the virtual environment terminal.


How to run and use the project:

  To run the webpage, simply run the app.py file. Note that all templates for the Flask app and all of the CSVs with product data should be included.

  
What outputs to expect:

  From the scraper.py file, you can expect a CSV with columns: url,image,name,price,brand,star,num_reviews
  I edited the CSVs to include the URLs, stars, and number of reviews from Yesstyle and Amazon: az_url,ys_url,ys_star,ys_num_reviews,az_star,az_num_reviews
  From the app.py fie, you can expect a simple webpage called skinFinds with a menu bar and search feature on the homepage. 


Any setup instructions or limitations:

  Using the scraper.py requires many other files like items.py, settings.py, middlewares.py, etc. which are included in the GitHub.
