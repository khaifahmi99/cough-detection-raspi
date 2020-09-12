from aws_controller import s3_upload, save_to_db
from server_controller import predict
import json

response = s3_upload('test2.jpg')
if response['status'] == 'OK':
    img_url = response['url']
    
    # do the fetch to /inference
    response = predict(img_url)
    if response['status'] == 'OK':
        if response['label'] == 'Coughing':
            # save to db
            result = save_to_db("1", response)
            print(result)
        else:
            print(response['label'])
    else:
        print('An error occured')