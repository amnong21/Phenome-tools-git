from flask import Flask

application = app = Flask(__name__)

print(app.config['ENV'])

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import views
