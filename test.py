from aws_controller import s3_upload, save_to_db
from server_controller import predict
import json
import cv2 as cv
import time

def capture_photo():
    PIC_TARGET_DIR = 'img/'
    current_time = int(time.time())
    cam = cv.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Could not open video device")

    for i in range(30):
        temp = cam.read()
    retval, frame = cam.read()
    if retval is not True:
        raise ValueError("Can't read frame")

    loc = PIC_TARGET_DIR + '{}.png'.format(current_time)

    cv.imwrite(loc, frame)
    cam.release()
    cv.destroyAllWindows()
    return current_time, frame

img, _ = capture_photo()
img = str(img) + '.png'
print(img)

response = s3_upload(img)
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

