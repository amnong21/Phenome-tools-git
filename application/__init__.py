from flask import Flask

application = Flask(__name__)

print(application.config['ENV'])

if application.config["ENV"] == "production":
    application.config.from_object("config.ProductionConfig")
    print('I am taking from ProductionConfig')
else:
    application.config.from_object("config.DevelopmentConfig")
    print('I am taking from DevelopmentConfig')

from application import views
