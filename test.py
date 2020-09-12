from aws_controller import s3_upload
from server_controller import predict
import json

response = s3_upload('test.jpg')
if response['status'] == 'OK':
    img_url = response['url']
    
    # do the fetch to /inference
    response = predict(img_url)
    if response['status'] == 'OK':
        print(response['label'])
    else:
        print('An error occured')