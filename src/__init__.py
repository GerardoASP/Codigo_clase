from flask import Flask
from os import environ
from src.endpoints.users import users #dios mio
from src.endpoints.accounts import accounts
from src.endpoints.products import products

from src.database import db,ma

def create_app():
  ##Creation app
  app = Flask(__name__, 
  instance_relative_config=True)
 
  app.config['ENVIRONMENT'] = environ.get("ENVIRONMENT")
  config_class = 'config.DevelopmentConfig'
 
  match app.config['ENVIRONMENT']:
   case "development":
     config_class = 'config.DevelopmentConfig'
   case "production":
     config_class = 'config.ProductionConfig'
   case _:
     print(f"ERROR: environment unknown: {app.config.get('ENVIRONMENT')}")
     app.config['ENVIRONMENT'] = "development"
     
  app.config.from_object(config_class)
  ##Load the blueprints
  app.register_blueprint(users)
  app.register_blueprint(accounts)
  app.register_blueprint(products)
  
  db.init_app(app) #conexion bd con flask
  ma.init_app(app)
  #migrate.init_app(app,db)
  
  #Creacion de tablas
  with app.app_context():
    #db.drop_all()
    db.create_all()
  
  return app