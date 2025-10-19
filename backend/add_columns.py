import os
import sqlite3

# 数据库路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "food.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查看表结构
cursor.execute("PRAGMA table_info(recipes)")
columns = [col[1] for col in cursor.fetchall()]
print("当前字段：", columns)

# 添加 category 列
if "category" not in columns:
    cursor.execute("ALTER TABLE recipes ADD COLUMN category TEXT")
    print("已添加字段 category")

# 添加 image 列
if "image" not in columns:
    cursor.execute("ALTER TABLE recipes ADD COLUMN image TEXT")
    print("已添加字段 image")

conn.commit()
conn.close()
print("表结构更新完成！")
