from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 用户表
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 存加密后的密码
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系：用户 -> 评论
    comments = db.relationship("Comment", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# 菜谱表
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(200))  # 封面图路径
    ingredients = db.Column(db.Text)   # 食材清单
    steps = db.Column(db.Text)         # 做法步骤
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系：菜谱 -> 评论
    comments = db.relationship("Comment", backref="recipe", lazy=True)

    def __repr__(self):
        return f"<Recipe {self.title}>"

# 评论表
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

    def __repr__(self):
        return f"<Comment by User {self.user_id} on Recipe {self.recipe_id}>"
