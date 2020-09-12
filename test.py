from aws_controller import s3_upload

response = s3_upload('test.jpg')
print(response)