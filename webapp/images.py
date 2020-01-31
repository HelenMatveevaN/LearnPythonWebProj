import os
from webapp.model import db, Images

def save_images(path, load_data):
    images_images = Images(path=path, load_data=load_data)
    db.session.add(images_images)
    db.session.commit()