import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env


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


if __name__ == '__main__':
    app.run(debug=True)


#Due to an error being caused by the ObjectId the following functions where unable to be implemented.

# edit function no working correctly due to an error with ObjectId
#@app.route('/edit_recipe/<recipe_id>')
#def edit_recipe(recipe_id):
#    the_recipe = mongo.db.Recipes.find_one({"_id": ObjectId(recipe_id)})
#    all_recipes = mongo.db.Recipes.find()
#    return render_template(edit_recipe.html, recipe=the_recipe, all_recipes=all_recipes)

#search bar not working
# search results page to display search results containing keywords
#@app.route('/search_results', methods=["GET"])
#def recipe_display():
#    user_search_input = request.form.get("user_search")
#    search_results = list(mongo.db.Recipes.find('_id:{"$regex":user_search_input}}'))
 #   return render_template("recipe_search_display.html", search_results=search_results)

# delete function no working correctly due to an error with ObjectId
#@app.route('/delete_recipe/<recipe_id>')
#def delete_recipe(recipe_id):
#    mongo.db.Recipes.delete_one({'_id': ObjectId(recipe_id)})
 #   return render_template("index.html")

# Edit Recipe
#@app.route("/recipe/<Recipes_id>/edit", methods=["GET", "POST"])
#def edit_recipe(Recipes_id):
#    Recipes = mongo.db.Recipes
#    my_Recipe = mongo.db.Recipes.find_one({"_id": ObjectId(Recipes_id)})
#    if request.method == "POST":
 #       Recipes.update({"_id": ObjectId(Recipes_id)}, {
 #           "name": request.form.get("name"),
 #           "category_name": request.form.get("category_name"),
 #           "prep_time": request.form.get("prep_time"),
 #           "cooking_time": request.form.get("cooking_time"),
  #          "serves": request.form.get("serves"),
 #           "ingredients": request.form.get('ingredients'),
 #           "method": request.form.get('method'),
 #           "image": request.form.get("image"),
 #       })
  #      return redirect(url_for('my_recipe', Recipes_id=Recipes_id))
#   else:
 #       form = add_recipe_form()
  #      return render_template('add_recipe.html',
  #                             selected_recipe=selected_recipe, form=form)



