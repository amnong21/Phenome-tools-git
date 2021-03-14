from application import application
from flask import render_template, request, redirect, url_for, abort, send_from_directory, jsonify, make_response, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import pandas as pd
from application.util.helpers import upload_file_to_s3

@application.route('/')
def index():
    return render_template("/index.html")


def allowed_image(filename):
    if not "." in filename:
        return False
    ext  = filename.rsplit(".", 1)[1]
    if ext.upper() in application.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_file(filename):

    if not "." in filename:
        return False
    ext  = filename.rsplit(".", 1)[1]
    if ext.upper() in application.config["UPLOAD_EXTENSIONS"]:
        return True
    else:
        return False

@application.route("/upload-file", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":

        if request.files:

            uploaded_file = request.files["file"]
            if uploaded_file.filename == "":
                print("First select a file")
                return redirect(request.url)

            if not allowed_file(uploaded_file.filename):
                print("File extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(uploaded_file.filename)
                flash("Begining upload!")
                output = upload_file_to_s3(uploaded_file) 
                print('output: {}'.format(output))
            # if upload success,will return file name of uploaded file
            if output:
                # write your code here 
                # to save the file name in database

                flash("Success upload")
                return redirect(request.url)

            # upload failed, redirect to upload page
            else:
                flash("Unable to upload, try again")
                return redirect(request.url)
            # uploaded_file.save(os.path.join(application.config["UPLOAD_PATH"], filename))

            # print("File has been saved")

            # perform map_converter
            # result_file_name = map_convert(filename)

            #send to get file
            # send_to_get_file = "/get-file/"+result_file_name
            # print("send_to_get_file: {}".format(send_to_get_file))
            #  try:
            #     return redirect(send_to_get_file)     
            # except FileNotFoundError:
            #     abort(404)
    

    return render_template("upload_file.html")


def map_convert(file_name):
    #file_name = file_name
    path = os.path.join(app.config["UPLOAD_PATH"], file_name)
    file_name_without_extension  = file_name.rsplit(".", 1)[0]
    ext = file_name.rsplit(".", 1)[1]

    # Read xlsx
    dfs = pd.read_excel(path, sheet_name=0, header=None)
    # dfs = pd.read_excel(path, sheet_name=0, dtype={'col1':str, 'col2':str})
    [rows, cols] = dfs.shape

    # Empty table of plots
    plots = []

    # Loop
    for row in range(1, rows+1):
        for col in range(1, cols+1):
            if pd.isna(dfs.iat[row-1, col-1]) == True:
                continue
            else:
                plot = [dfs.iat[row-1, col-1], dfs.iat[row-1, col-1], row, col]
                plots.append(plot)

    # Convert list to DF
    df = pd.DataFrame(plots, columns=['Entry code', 'Plot', 'row', 'column'])

    # Save csv in DOWNLOADS to csv
    final_file_name= file_name_without_extension + '_plot_list.csv'
    df.to_csv(os.path.join(app.config["DOWNLOAD_PATH"], final_file_name), index_label='index')
    return final_file_name

