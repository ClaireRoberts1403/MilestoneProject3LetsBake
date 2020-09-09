import os
import time
from flask import Flask, render_template, request
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

if os.path.exists("venv/env.py"):
    import env

app = Flask(__name__)

#Mongodb database set up
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route('/')
def index():
    recipe_of_the_week = mongo.db.Recipes.find({"_id": 'ObjectId("5f491c75885c2e445ab07664")'})
    return render_template("index.html", Recipes=recipe_of_the_week)

if __name__ == '__main__':
    app.run(debug=True)