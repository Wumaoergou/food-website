import os
from app import app, db, Recipe

# 静态图片目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(BASE_DIR, "static", "images")

DEFAULT_IMAGE = "default.jpg"
default_path = os.path.join(images_dir, DEFAULT_IMAGE)

if not os.path.isfile(default_path):
    print(f"⚠️ 默认占位图 {DEFAULT_IMAGE} 不存在，请先放到 {images_dir}")
    exit(1)

with app.app_context():
    recipes = Recipe.query.all()
    missing_images = []

    for r in recipes:
        image_path = os.path.join(images_dir, r.image)
        if not os.path.isfile(image_path) or not r.image:
            missing_images.append((r.title, r.image))
            r.image = DEFAULT_IMAGE  # 自动修正为默认图片
            print(f"菜谱【{r.title}】缺失图片，已设置为默认图片 {DEFAULT_IMAGE}")

    db.session.commit()

    if missing_images:
        print(f"\n总共 {len(missing_images)} 个菜谱图片缺失，已修正为默认图片。")
    else:
        print("所有菜谱图片都存在，未发现缺失。")
