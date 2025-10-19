import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# -------------------------------
# 1. 初始化 Flask 和数据库
# -------------------------------
app = Flask(__name__)

# 绝对路径，确保 database 文件夹存在
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # food-website 目录
db_dir = os.path.join(BASE_DIR, "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "food.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------------
# 2. 数据模型
# -------------------------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    comments = db.relationship("Comment", backref="author", lazy=True)

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    image = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    steps = db.Column(db.Text)
    comments = db.relationship("Comment", backref="recipe", lazy=True)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

# -------------------------------
# 3. 初始化数据库并添加测试数据
# -------------------------------
with app.app_context():
    print("正在初始化数据库...")

    # 删除旧表并创建新表
    db.drop_all()
    db.create_all()

    # 添加用户
    user1 = User(username="admin", email="admin@example.com", password="123456")
    user2 = User(username="alice", email="alice@example.com", password="alice123")

    # 添加菜谱
    recipe1 = Recipe(
        title="日本寿司",
        description="新鲜食材与匠心手艺，感受东瀛美味。",
        image="recipes/recipe_1.jpg",
        ingredients="米饭, 生鱼片, 紫菜, 芥末",
        steps="1. 准备米饭并加醋\n2. 放置紫菜\n3. 加入鱼片\n4. 卷起并切片"
    )
    recipe2 = Recipe(
        title="意大利披萨",
        description="芝士与番茄的绝妙融合，意大利经典美食。",
        image="recipes/recipe_2.jpg",
        ingredients="面粉, 番茄, 奶酪, 橄榄油",
        steps="1. 和面发酵\n2. 涂抹番茄酱\n3. 撒上芝士\n4. 烤箱200℃ 15分钟"
    )
    recipe3 = Recipe(
        title="四川火锅",
        description="麻辣鲜香，热气腾腾的中国川味代表。",
        image="recipes/recipe_3.jpg",
        ingredients="牛肉片, 辣椒, 花椒, 火锅底料, 蔬菜",
        steps="1. 准备火锅底料\n2. 加水煮沸\n3. 放入牛肉和蔬菜\n4. 涮食即可"
    )

    # 添加评论
    comment1 = Comment(content="寿司看起来好好吃！", author=user2, recipe=recipe1)
    comment2 = Comment(content="披萨我昨天刚做过，很棒！", author=user1, recipe=recipe2)
    comment3 = Comment(content="火锅太赞了，下次聚会一定试试！", author=user2, recipe=recipe3)

    # 保存到数据库
    db.session.add_all([user1, user2, recipe1, recipe2, recipe3, comment1, comment2, comment3])
    db.session.commit()

    print("数据库初始化完成！food.db 已生成并写入测试数据。")
    print(f"数据库路径: {db_path}")
