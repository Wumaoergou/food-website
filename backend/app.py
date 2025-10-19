import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(BASE_DIR, "..", "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "food.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据模型
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(200))
    category = db.Column(db.String(50))
    ingredients = db.Column(db.Text)
    steps = db.Column(db.Text)

# 首页
@app.route("/")
def index():
    categories = [c[0] for c in db.session.query(Recipe.category).distinct() if c[0]]
    recipes = Recipe.query.all()
    return render_template("index.html", recipes=recipes, categories=categories, current_category=None)

# 分类页
@app.route("/category/<category_name>")
def category(category_name):
    categories = [c[0] for c in db.session.query(Recipe.category).distinct() if c[0]]
    recipes = Recipe.query.filter_by(category=category_name).all()
    return render_template("index.html", recipes=recipes, categories=categories, current_category=category_name)

# 菜谱详情页
@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)
