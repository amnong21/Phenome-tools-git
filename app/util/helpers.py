import boto3, botocore
import os
from werkzeug.utils import secure_filename
from app import app
import pandas as pd
from io import StringIO #python3 

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            '{}{}'.format(app.config['UPLOAD_PATH'],file.filename),
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened Amnon: ", e)
        return e
    

    # after upload file to s3 bucket, return url of the uploaded file
    uploaded_file_url = "{}{}{}".format(os.getenv('AWS_DOMAIN'), app.config['UPLOAD_PATH'],file.filename)
    return uploaded_file_url

def save_csv_to_s3(df, filename):
    csv_buffer = StringIO() # stores csv in buffer area
    df.to_csv(csv_buffer, index=False)
    response = s3.put_object(
        ACL = 'public-read-write',
        Body = csv_buffer.getvalue(),
        Bucket = os.getenv('AWS_BUCKET_NAME'),
        Key = filename
        )  
    return response

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