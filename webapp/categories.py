from webapp.model import db, Categories

def get_categories():
    category_list = ['дети', 'женщины', 'мужчины', 'кошки', 'собаки', 'неизвестно']
    for name in category_list:
        save_categories(name, "Y")

def save_categories(name, labelled):
    cats_cats = Categories(name=name, labelled=labelled)
    db.session.add(cats_cats)
    db.session.commit()