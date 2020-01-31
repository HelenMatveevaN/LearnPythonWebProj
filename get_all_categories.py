from webapp import create_app
from webapp.categories import get_categories

app = create_app()
'''скрипт заполнения категорий в базе данных скриптом'''
with app.app_context():
    get_categories()