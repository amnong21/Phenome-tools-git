from flask import Flask

application = Flask(__name__)

print(application.config['ENV'])
if application.config["ENV"] == "production":
    application.config.from_object("config.ProductionConfig")
else:
    application.config.from_object("config.DevelopmentConfig")

from application import views
