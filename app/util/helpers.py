import boto3, botocore
import os
from werkzeug.utils import secure_filename
from app import app

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
