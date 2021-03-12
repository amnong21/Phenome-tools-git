from application import application
from flask import render_template, request, redirect, url_for, abort, send_from_directory, jsonify, make_response
from werkzeug.utils import secure_filename
import os

@application.route('/')
def hello_world():
    return render_template("/index.html")

@application.route('/about/')
def about():
    return "All about Flask"
