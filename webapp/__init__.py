from flask import Flask, render_template

from webapp.forms import SelectImgForm

def create_app():
    app = Flask(__name__) #переменная будет flask-приложением
    app.config.from_pyfile('config.py') #можно брать конфигурацию из json и др. типов файлов

    @app.route("/") #запустится __init__.py
    def index():
        select_form = SelectImgForm()
        try:
            return render_template('index.html', page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'], form=select_form )
        except KeyError:
            return render_template('index.html', page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'], form=select_form )

    @app.route("/image.html")
    def image():
        return render_template('image.html', page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'] )

    @app.route("/images.html")
    def images():
        return render_template('images.html', page_title_main=app.config['PAGE_TITLE_MAIN'], page_title_img=app.config['PAGE_TITLE_IMG'], page_title_imgs=app.config['PAGE_TITLE_IMGS'] )

    return app