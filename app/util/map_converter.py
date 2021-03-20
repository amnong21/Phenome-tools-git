import pandas as pd
import boto3, botocore
import os
from io import StringIO #python3 
from app import app


def map_convert(file_url, file_name):
    file_name = file_name
    file_name_without_extension  = file_name.rsplit(".", 1)[0]
    ext = file_name.rsplit(".", 1)[1]

    # Read xlsx
    dfs = pd.read_excel(file_url, sheet_name=0, header=None)
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
    converted_df = pd.DataFrame(plots, columns=['Entry code', 'Plot', 'row', 'column'])
    final_file_name= file_name_without_extension + '_plot_list.csv'
    
    csv_buffer = StringIO()
    converted_df.to_csv(csv_buffer)
    client = boto3.client('s3', 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = client.put_object(
        ACL = 'public-read-write',
        Body = csv_buffer.getvalue(),
        Bucket = os.getenv('AWS_BUCKET_NAME'),
        Key = final_file_name
    )
    return final_file_name