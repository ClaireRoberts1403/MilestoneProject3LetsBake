import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

#Mongodb database set up
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route('/')
def index():
    recipe_of_the_week = mongo.db.Recipes.find()
    return render_template("index.html", Recipes=recipe_of_the_week)

# send user to add recipe page form
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")



if __name__ == '__main__':
    app.run(debug=True)