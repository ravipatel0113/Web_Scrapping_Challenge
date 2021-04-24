from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/web_scraping")
mars_data = mongo.db.mars_data


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    

    # Return template and data
    return render_template("index.html")


# Route that will trigger the scrape function
@app.route("/scrape")
def scrapes():
    mars_data.drop()
    # Run the scrape function
    scrape_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, scrape_data, upsert=True)

    # Redirect back to home page
    return redirect("/data")

@app.route("/data")
def data():
    mars_info = mongo.db.mars_data.find_one()
    return render_template("data.html", info=mars_info)

if __name__ == "__main__":
    app.run(debug=True)