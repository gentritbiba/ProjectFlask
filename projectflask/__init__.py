import os
from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class 
from flask import jsonify , request, redirect, url_for , session, json
from flask_pymongo import PyMongo
basedir = os.path.abspath(os.path.dirname(__file__))
mongo = PyMongo()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads')
  app.config['MONGO_URI'] = os.getenv('MONGO_URI')
  return app

app=create_app()
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) 
mongo.init_app(app)

from projectflask import routes