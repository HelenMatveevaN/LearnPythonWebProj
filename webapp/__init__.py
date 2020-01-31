import os

from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename

from webapp.model import db, Categories, Images, ImagesCategories
from webapp.images import save_images
from webapp.images_categories import save_images_categories

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

def create_app():
    app = Flask(__name__) #переменная будет flask-приложением
    app.config.from_pyfile('config.py') #можно брать конфигурацию из json и др. типов файлов
    db.init_app(app) #инициализация базы данных, после app.config (последовательность строго такая)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Session = sessionmaker(bind=engine)

    @app.route('/', methods=['GET', 'POST']) #запустится __init__.py
    def index():
        category_list = Categories.query.order_by(Categories.name).all()
        if request.method == 'POST':
            file = request.files['file']
            if file: #если файл загружен:
                filename = secure_filename(file.filename)
                #сохранила файл в папку
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                #проверяю, есть ли такой image в таблице Image (фильтр по filepath):
                session = Session()
                id_image = 0
                try:
                    image_list = session.query(Images.id).filter(Images.path==filepath).first()
                    id_image = image_list[0]
                except(ValueError, TypeError):
                    id_image = 0
                #если есть, редактирую load_data в Image
                if id_image > 0:
                    image_list = Images.query.filter_by(id = id_image).update({'load_data': datetime.now()})
                    db.session.commit()
                #иначе создаю новую запись в Image
                else:
                    save_images(path=filepath, load_data=datetime.now())   
                    session = Session()            
                    image_list = session.query(Images.id).filter(Images.path==filepath).first()
                    id_image = image_list[0]

                #проверяю, есть такой image id в таблице ImageCategory
                session = Session()
                id_image_category_exists = 0
                try:
                    image_category_list = session.query(ImagesCategories.id).filter(ImagesCategories.id_image==id_image).first()
                    id_image_category_exists = image_category_list[0]
                except(ValueError, TypeError):
                    id_image_category_exists = 0

                #по наименовании категории с формы получаем id категории из таблицы Categories
                category_name_form = request.form.get('category') 
                category_list_ = session.query(Categories.id).filter(Categories.name==category_name_form).first()
                id_category = category_list_[0]
                
                #сохранила инф. в базу данных
                if id_image_category_exists > 0:
                    update = ImagesCategories.query.filter_by(id = id_image_category_exists).first()
                    update.updated_at = datetime.now()
                    update.id_category = id_category
                    db.session.commit()
                else:
                    save_images_categories(id_image=id_image, id_category=id_category, labelled=True, confidence=0, updated_at=datetime.now())
                    
                flash('загружен файл: ' + filename + ' | категория: ' + category_name_form) #передача данных на веб-страницу
                return redirect(url_for('index', filename=filename))
        return render_template('index.html', category_list=category_list, page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'])
        
    @app.route('/image')
    def image():
        #загружает последнюю картинку из базы данных
        image_list = Images.query.order_by(desc(Images.load_data)).first()
        picture = image_list.path
        new_picture = picture[picture.rfind('/')+1:]
        return render_template('image.html', page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'], picture=new_picture)

    @app.route("/images")
    def images():
        #загрузить последние 10 картинок из базы данных
        cntrows = Images.query.count()
        if cntrows > 10:
            cntrows = 10
        image_list = Images.query.order_by(desc(Images.load_data)).limit(cntrows)
        image_list_new = image_list
        for x in range(0, cntrows):
            picture = image_list[x].path
            image_list_new[x].path = picture[picture.rfind('/')+1:]
        return render_template('images.html', page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'], image_list=image_list_new )
    return app
