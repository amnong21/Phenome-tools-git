from app import app
from flask import jsonify, session, render_template, request, redirect, url_for, abort, send_from_directory, make_response, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.util.helpers import upload_file_to_s3, check_file_name, generate_download_url, save_csv_to_s3, allowed_image, allowed_file
import boto3, botocore
from app.util.map_convert import convert_map
from app.util.variables_fix import check_variables

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("/index.html")

@app.errorhandler(404)
def page_not_found(e):
    
    app.logger.info(f"Page not found: {request.url}")
    
    return render_template("error_handlers/404.html"), 404

@app.errorhandler(500)
def server_error(e):

    app.logger.error(f"Server error: {request.url}")

    return render_template("error_handlers/500.html"), 500

@app.route('/download/<filename>')
def download_file(filename):
    url = generate_download_url(filename)
    return redirect(url, code=302)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        if request.files:
            
            uploaded_file = request.files["file"]
            filename = uploaded_file.filename
            
            message = check_file_name(uploaded_file.filename)
            flash(message[0], message[1])

            if message[1] == 'success':
                filename = secure_filename(filename)
                file_name_without_ext, file_ext  = filename.rsplit(".", 1)
                final_file_name = file_name_without_ext + '_list_of_plots.csv'

                if file_ext == 'csv':
                    plots = convert_map(pd.read_csv(request.files.get('file'), header=None))
                else: #excel
                    plots = convert_map(pd.read_excel(request.files.get('file'), header=None, converters={'Date': str}))

                df = pd.DataFrame(plots, columns=["Genotype", "Entry", "Plot", "Row", "Column"])
                
                save_csv_to_s3(df, final_file_name)
                return redirect('/download/' + final_file_name)
            else:
                redirect(request.url)
    return render_template('upload.html')

@app.route('/prepare-file', methods=['GET', 'POST'])
def prepare_file():
    if request.method == 'POST':
        
        if request.files:            
            uploaded_file = request.files["file"]
            
            message = check_file_name(uploaded_file.filename)
            flash(message[0], message[1])

            if message[1] == 'success':
                uploaded_file.filename = secure_filename(uploaded_file.filename)
                upload_file_to_s3(uploaded_file)
                session["filename"] = uploaded_file.filename

                return redirect('/preview/')    
    return render_template('upload_observations.html')

@app.route('/preview/', methods=['GET', 'POST'])
def preview():

    # variables_list = session.get("variables_list")
    filename = session.get("filename")
    if not filename:
        return redirect('/prepare-file')
    
    # get file from S3:
    file_name_without_ext, ext  = filename.rsplit(".", 1)
    path_to_file = os.getenv('AWS_DOMAIN') + app.config['UPLOAD_PATH']+filename
    # load file into df:
    if ext.lower() == 'csv':
        df = pd.read_csv(path_to_file)
    else: #excel
        df = pd.read_excel(path_to_file)
    # declare vars and return to preview
    data = df.values
    preview_data = data[1:5,:]
    headers = df.columns

    return render_template('preview.html', data=preview_data, headers=headers)

@app.route('/preview/add_variables', methods=['GET', 'POST'])
def add_variables():
    print('Adding variables!!')

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    variables_list = req

    return res
    # variables_list = request.form['variables_to_add']
    
    # if variables_list:
            
    #     return jsonify({'name' : variables_list})
    
    # return jsonify({'error' : 'Invalid Data!'})


    # if request.method == 'POST':
    #     add_variables = request.form.get('variables_list')
    #     variables_list.append(add_variables)
    #     session["variables_list"] = variables_list
    #     print('the method is POST')
    # if request.method == 'DELETE':
    #     variables_list = []
    #     session["variables_list"] = variables_list
    #     print('the method is DELETE')

@app.route("/guestbook")
def guestbook():
    return render_template("guestbook.html")

@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res

@app.route('/pre_process')
def form_submit():
    return render_template('form.html')

@app.route('/process', methods = ['POST'])
def process():

    email = request.form['email']
    name = request.form['name']

    if email and name:
        newName = name[::-1]
    
        return jsonify({'name' : newName})
    
    return jsonify({'error' : 'Missing Data!'})