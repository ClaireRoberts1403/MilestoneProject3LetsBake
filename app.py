import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

recipe_id = ObjectId

app = Flask(__name__)

#Mongodb database set up
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)

#home page
@app.route('/')
def index():
    all_recipes = mongo.db.Recipes.find()
    return render_template("index.html", Recipes=all_recipes)


# category page displaying all recipes with a set category
@app.route('/category/<category_type>')
def category_page(category_type):
    category_type = mongo.db.Recipes.find({"category_name": category_type})
    return render_template('category_page.html', Recipes=category_type)


# send user to add recipe form
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")


# submit recipe page
@app.route('/submit_recipe', methods=["POST"])
def submit_recipe():
    add_recipe = mongo.db.Recipes


    name = request.form['name']
    category_name = request.form['category_name']
    prep_time = request.form['prep_time']
    cooking_time = request.form['cooking_time']
    effort_level = request.form['effort_level']
    serves = request.form['serves']
    ingredients = request.form['ingredients']
    method = request.form['method']
    recipe_image = request.files['recipe_image']

    add_recipe_form = {
        "name": name,
        "category_name": category_name,
        "prep_time": prep_time,
        "cooking_time": cooking_time,
        "effort_level": effort_level,
        "serves": serves,
        "ingredients": ingredients,
        "method": method,
        "recipe_image": recipe_image,

    }
    add_recipe.insert_one(request.form.to_dict())
    mongo.save_file(recipe_image.filename, recipe_image)
    return render_template("Message.html")

# To display full recipe with link to edit and delete recipe
#@app.route('/recipe')
#def recipe():
#    Recipes = mongo.db.Recipes.find_one()
 #   return render_template("recipe.html", Recipes=Recipes)


#test to see recipe image returning from mongodb
@app.route('/image/<recipe_image>')
def image(recipe_image):
    return mongo.send_file(recipe_image)

# 404 error page personalised to site
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


#test to see recipe image returning from mongodb
@app.route('/edit_recipe')
def edit_recipe():
    return render_template("edit_recipe.html")

# edit function
#@app.route('/edit_recipe/<recipe_id>')
#def edit_recipe(recipe_id):
#    the_recipe = mongo.db.Recipes.find_one({"_id": ObjectId(recipe_id)})
#    all_recipes = mongo.db.Recipes.find()
#    return render_template(edit_recipe.html, recipe=the_recipe, all_recipes=all_recipes)



# delete function no recipe id added as it throws an error and crashes the app?
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.Recipes.delete_one({'_id': ObjectId(recipe_id)})
    return render_template("index.html", recipe_id=recipe_id)


if __name__ == '__main__':
    app.run(debug=True)