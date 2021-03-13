from flask import Flask
from flask_s3 import FlaskS3

application = Flask(__name__)

application.config['FLASKS3_BUCKET_NAME'] = 'AmnonBucket'
s3 = FlaskS3(application)

print(application.config['ENV'])
if application.config["ENV"] == "production":
    application.config.from_object("config.ProductionConfig")
else:
    application.config.from_object("config.DevelopmentConfig")

from application import views
