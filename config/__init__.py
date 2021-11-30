import os
from database.db import MoneyDB


DB_PATH = './database/money.db'
DB = MoneyDB(DB_PATH)
if not os.path.exists(DB_PATH):
    DB.create_db()
