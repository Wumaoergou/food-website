import os
from app import app, db, Recipe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(BASE_DIR, "static", "images")
DEFAULT_IMAGE = "default.jpg"

def find_best_match(filename):
    """在 images_dir 中找到最匹配的文件（忽略大小写）"""
    if not filename:
        return None
    for f in os.listdir(images_dir):
        if f.lower() == filename.lower():
            return f
    return None

with app.app_context():
    recipes = Recipe.query.all()
    fixed_count = 0
    defaulted_count = 0

    for r in recipes:
        original = r.image or ""
        fixed_name = original.strip().replace("\\", "/")

        # 去掉路径前缀，例如 static/images/
        if "images/" in fixed_name:
            fixed_name = fixed_name.split("images/")[-1]
        if "/" in fixed_name:
            fixed_name = os.path.basename(fixed_name)

        # 查找匹配文件
        matched = find_best_match(fixed_name)
        if matched and os.path.isfile(os.path.join(images_dir, matched)):
            if matched != r.image:
                print(f"✅ 修复：{r.title} -> '{r.image}' 改为 '{matched}'")
                r.image = matched
                fixed_count += 1
        else:
            # 文件不存在，设为默认图
            print(f"⚠️ 图片缺失：{r.title} -> '{r.image}'，改为默认图片 {DEFAULT_IMAGE}")
            r.image = DEFAULT_IMAGE
            defaulted_count += 1

    db.session.commit()

    print("\n--- 修复完成 ---")
    print(f"✅ 修复文件名：{fixed_count} 条")
    print(f"⚠️ 设置默认图片：{defaulted_count} 条")
