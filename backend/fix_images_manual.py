from app import app, db, Recipe

with app.app_context():
    # 找到每道菜
    pizza = Recipe.query.filter_by(title="意大利披萨").first()
    sushi = Recipe.query.filter_by(title="日本寿司").first()
    hotpot = Recipe.query.filter_by(title="四川火锅").first()

    # 设置对应的图片文件名（必须放在 static/images 下）
    if pizza:
        pizza.image = "recipe_1.jpg"
    if sushi:
        sushi.image = "recipe_2.jpg"
    if hotpot:
        hotpot.image = "recipe_3.jpg"

    # 保存修改
    db.session.commit()

    print("✅ 图片字段已更新完成！")
