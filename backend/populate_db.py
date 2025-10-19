import os
from backend import db, Recipe  # 确保在 backend 下运行
from sqlalchemy.exc import IntegrityError

# ----------------------------
# 确保数据库路径正确
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(BASE_DIR, "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "food.db")

# ----------------------------
# 初始化数据库
# ----------------------------
db.create_all()

# ----------------------------
# 示例菜谱数据
# ----------------------------
sample_recipes = [
    {
        "title": "意大利面",
        "description": "经典意大利面，美味易做。",
        "category": "意大利",
        "image": "recipe_1.jpg",
        "ingredients": "意大利面,番茄,橄榄油,大蒜,罗勒",
        "steps": "1. 煮面\n2. 炒番茄大蒜\n3. 拌面"
    },
    {
        "title": "宫保鸡丁",
        "description": "香辣可口的川菜经典。",
        "category": "中国",
        "image": "recipe_2.jpg",
        "ingredients": "鸡胸肉,花生,干辣椒,葱姜蒜,酱油",
        "steps": "1. 切鸡丁\n2. 炒花生辣椒\n3. 加鸡丁炒匀"
    },
    {
        "title": "法式薄饼",
        "description": "甜美法式早餐。",
        "category": "法国",
        "image": "recipe_3.jpg",
        "ingredients": "面粉,牛奶,鸡蛋,黄油,糖",
        "steps": "1. 混合面糊\n2. 烙薄饼\n3. 加糖黄油"
    }
]

# ----------------------------
# 插入示例数据
# ----------------------------
for r in sample_recipes:
    # 检查是否已存在
    exists = Recipe.query.filter_by(title=r["title"]).first()
    if not exists:
        recipe = Recipe(
            title=r["title"],
            description=r["description"],
            category=r["category"],
            image=r["image"],
            ingredients=r["ingredients"],
            steps=r["steps"]
        )
        db.session.add(recipe)
        try:
            db.session.commit()
            print(f"已添加菜谱：{r['title']}")
        except IntegrityError:
            db.session.rollback()
            print(f"菜谱已存在：{r['title']}")
    else:
        print(f"菜谱已存在：{r['title']}")

print("示例菜谱插入完成！")
