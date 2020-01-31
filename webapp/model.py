import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

db = SQLAlchemy()

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    load_data = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class ImagesCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_image = db.Column(db.Integer, nullable=False)
    id_category = db.Column(db.Integer, nullable=False)
    labelled = db.Column(db.Boolean, nullable=False)
    confidence = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)