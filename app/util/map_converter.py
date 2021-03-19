import pandas as pd
import boto3, botocore
import os
from io import StringIO #python3 
from app.util.helpers import save_csv_to_s3
import s3fs



def map_convert(file_url, file_name):
    file_name = file_name
    file_name_without_extension  = file_name.rsplit(".", 1)[0]
    ext = file_name.rsplit(".", 1)[1]

    # Read xlsx
    dfs = pd.read_excel(file_url, sheet_name=0, header=None)
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
    converted_df = pd.DataFrame(plots, columns=['Entry code', 'Plot', 'row', 'column'])
    final_file_name= file_name_without_extension + '_plot_list.csv'
    
    # fs = s3fs.S3FileSystem(anon=False)
    # path = os.getenv("AWS_BUCKET_NAME") + '/' + final_file_name
    # with fs.open(path,'w') as f:
    #     converted_df.to_csv(f)

    csv_buffer = StringIO()
    converted_df.to_csv(csv_buffer)
    client = boto3.client('s3')
    response = client.put_object(
        ACL = 'public-read-write',
        Body = csv_buffer.getvalue(),
        Bucket = os.getenv("AWS_BUCKET_NAME"),
        Key = 'my_file.csv'
    )
    # output = save_csv_to_s3(final_file_name, csv_buffer)
    # print(type(output))
    return response