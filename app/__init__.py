from flask import Flask

application = Flask(__name__)

app = application

from app import views

