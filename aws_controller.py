import boto3
import os
import matplotlib.pyplot as plt
from botocore.exceptions import ClientError

FOLDER_NAME = 'img/'
BUCKET_NAME = 'cough-images'

def s3_upload(file_name, bucket=BUCKET_NAME):
    file_loc = os.path.join(FOLDER_NAME, file_name)
    im = plt.imread(file_loc)
    bucket = boto3.resource('s3', region_name='ap-southeast-2').Bucket(BUCKET_NAME)
    try:
        bucket.upload_file(file_loc, file_name, ExtraArgs={'ACL':'public-read'})
        response = {'status': 'OK', 'url': f'https://cough-images.s3-ap-southeast-2.amazonaws.com/{file_name}' }
    except ClientError as e:
        response = {'status': 'Error', 'msg': 'Fail to upload file to s3'}

    return response