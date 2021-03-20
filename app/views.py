from app import app
from flask import render_template, request, redirect, url_for, abort, send_from_directory, jsonify, make_response, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.util.helpers import upload_file_to_s3
from app.util.map_converter import map_convert
import boto3, botocore

@app.route('/')
def index():
    return render_template("/index.html")


def allowed_image(filename):
    if not "." in filename:
        return False
    ext  = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_file(filename):

    if not "." in filename:
        return False
    ext  = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["UPLOAD_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/upload-file", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        if request.files:

            uploaded_file = request.files["file"]
            if uploaded_file.filename == "":
                flash("First select a file")
                return redirect(request.url)

            if not allowed_file(uploaded_file.filename):
                flash("File extension is not allowed, use only {}".format(', '.join(app.config['UPLOAD_EXTENSIONS'])))
                return redirect(request.url)

            else:
                filename = secure_filename(uploaded_file.filename)
                flash("Begining upload..")
                file_url = upload_file_to_s3(uploaded_file) 
            # if upload success,will return file name of uploaded file
            if file_url:
                # write your code here 
                # to save the file name in database

                flash("Successfully uploaded to {}".format(file_url))
                # map convert and save to downloads folder
                converted_file = map_convert(file_url, filename)
                # save_converted_to_downloads_folder(converted_file)
                flash("Message: {}".format(converted_file))
                # return redirect('/download/'+converted_file)
                return redirect('/download/' + converted_file)    
            # upload failed, redirect to upload page
            else:
                flash("Unable to upload, try again")
                return redirect(request.url)

    return render_template("upload_file.html")


@app.route('/download/<resource>')
def download_image(resource):
    """ resource: name of the file to download"""
    s3 = boto3.client(
        's3', 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    url = s3.generate_presigned_url('get_object', Params = {'Bucket': os.getenv('AWS_BUCKET_NAME'), 'Key': resource}, ExpiresIn = 100)
    return redirect(url, code=302)
