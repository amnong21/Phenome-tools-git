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

            uploaded_file.save(os.path.join(application.config["UPLOAD_PATH"], filename))

            print("File has been saved")

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
