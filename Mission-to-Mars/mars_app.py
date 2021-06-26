from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__, template_folder="templates/index.html")

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database usnig update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # redirect back to the homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)