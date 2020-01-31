from webapp.model import db, Categories

def get_categories():
    category_list = ['дети', 'женщины', 'мужчины', 'кошки', 'собаки', 'unknown']
    for name in category_list:
        save_categories(name)

def save_categories(name):
    cats_cats = Categories(name=name)
    db.session.add(cats_cats)
    db.session.commit()
