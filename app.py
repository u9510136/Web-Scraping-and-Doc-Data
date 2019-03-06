import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_data_db
db.mars_data_coll.drop()

@app.route("/")
def home():
    mars_data = list(db.mars_data_coll.find())
    print(mars_data)
    return render_template("index.html", mars_data = mars_data)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    db.mars_data_coll.update({}, mars_data, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)