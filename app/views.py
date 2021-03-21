from app import app
from flask import render_template, request, redirect, url_for, abort, send_from_directory, make_response, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.util.helpers import upload_file_to_s3, save_csv_to_s3, allowed_image, allowed_file
import boto3, botocore
from app.util.map_convert import convert_map

@app.route('/')
def index():
    return(redirect(url_for('home')))

@app.route('/home')
def home():
    return render_template("/index.html")

@app.route('/download/<resource>')
def download_file(resource):
    """ resource: name of the file to download"""
    s3 = boto3.client(
        's3', 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': os.getenv('AWS_BUCKET_NAME'), 'Key': resource}, ExpiresIn = 100)
    return redirect(url, code=302)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        if request.files:
            
            uploaded_file = request.files["file"]

            if uploaded_file.filename == "":
                flash("First select a file")
                return redirect(request.url)
            
            if not allowed_file(uploaded_file.filename):
                flash("File extension is not allowed, use only {}".format(', '.join(app.config['UPLOAD_EXTENSIONS'])))
                return redirect(request.url)

            filename = secure_filename(uploaded_file.filename) 
            file_name_without_ext, file_ext  = filename.rsplit(".", 1)
            final_file_name = file_name_without_ext + '_list_of_plots.csv'

            if file_ext == 'csv':
                plots = convert_map(pd.read_csv(request.files.get('file')))
            else: #excel
                plots = convert_map(pd.read_excel(request.files.get('file'), converters={'Date': str}))

            df = pd.DataFrame(plots, columns=["Genotype", "Entry", "Plot", "Row", "Column"])
            save_csv_to_s3(df, final_file_name)
             
            return redirect('/download/' + final_file_name)
    return render_template('upload.html')
