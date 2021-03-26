from app import app
from flask import session, render_template, request, redirect, url_for, abort, send_from_directory, make_response, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.util.helpers import check_file_name, generate_download_url, save_csv_to_s3, allowed_image, allowed_file
import boto3, botocore
from app.util.map_convert import convert_map
from app.util.variables_fix import check_variables

@app.route('/')
def index():
    return(redirect(url_for('home')))

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

# @app.route('/prepare_file', methods=['GET', 'POST'])
# def prepare_file():

#     if request.method == 'POST':
        
#         # Getting variables from form textbox:
#         variables_list = request.form['variables_list'].rsplit(",")
#         variables_list = [var.lower() for var in variables_list]
#         variables_list.insert(0, 'name')

#         if request.files:
            
#             uploaded_file = request.files["file"]
#             filename = uploaded_file.filename
            
#             message = check_file_name(uploaded_file.filename)
#             flash(message[0], message[1])

#             if message[1] == 'success':
#                 filename = secure_filename(uploaded_file.filename) 
#                 file_name_without_ext, file_ext  = filename.rsplit(".", 1)
#                 # final_file_name = file_name_without_ext + '_list_of_plots.csv'

#                 if file_ext == 'csv':
#                     data = pd.read_csv(request.files.get('file'))
#                 else: #excel
#                     data = pd.read_excel(request.files.get('file'))

#                 decisions = check_variables(variables_list, data)
#                 headers = decisions.columns.tolist()
#                 headers.insert(0, "Variable")   
                             
#                 data = decisions.to_records().tolist() # returns a list of tuples
                
#                 return render_template('show_table.html', headers = headers, data=data)

#             else:
#                 flash("Something went wrong", "warning")
#                 # redirect(request.url)
#     return render_template('fix_variables.html')

# @app.route('/show_table')
# def show_table():
#     return 

@app.route('/album')
def show_album():
    return render_template('album.html')