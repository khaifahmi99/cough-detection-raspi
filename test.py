from aws_controller import s3_upload, save_to_db
from server_controller import predict_img, predict_sound
import json
import cv2 as cv
import time
import numpy as np

import sounddevice as sd
from scipy.io import wavfile

def capture_photo():
    PIC_TARGET_DIR = 'data/'
    current_time = int(time.time()) # for unique file name
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

def record_sound():
    PIC_TARGET_DIR = 'data/'
    current_time = int(time.time()) # for unique file name

    fs = 44100  # this is the frequency sampling; also: 4999, 64000
    seconds = 3  # Duration of recording
    
    rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print("Start Audio Recording...")
    sd.wait()  # Wait until recording is finished
    print("Audio Recording Finished...")

    loc = PIC_TARGET_DIR + '{}.wav'.format(current_time)
    wavfile.write(loc, fs, rec)
    return current_time

def test_img_inference():
    # img, _ = capture_photo()
    # img = str(img) + '.png'
    # print(img)

    # comment this line to use captured image
    img = 'test_cough.jpg'

    response = s3_upload(img)
    if response['status'] == 'OK':
        img_url = response['url']
        
        # do the fetch to /inference
        response = predict_img(img_url)
        if response['status'] == 'OK':
            print('----------------------------------\n')
            print('Prediction: ' + response['label'])
            print('\n----------------------------------')
            # if coughing
            if response['label'] == 'Coughing':
                # save to db
                result = save_to_db("1", response, classification_type='image')

        else:
            print('An error occured')

def test_sound_inference():
    # record sound for 3 seconds
    # file_name = record_sound()
    # file_name = str(file_name) + '.wav'

    # replace next line to use actual recording
    file_name = 'test_not_cough2.wav'
    response = s3_upload(file_name)

    if response['status'] == 'OK':
        sound_url = response['url']
        
        # do the fetch to /inference
        response = predict_sound(sound_url)
        if response['status'] == 'OK':
            print('----------------------------------\n')
            print('Prediction: ' + response['label'] + '(' + str(response['confidence']) + ')')
            print('\n----------------------------------')
            # if coughing
            if response['label'] == 'Coughing':
                # save to db
                result = save_to_db("2", response, classification_type='sound')

        else:
            print('An error occured')

def monitor(state='test'):
    count = 1
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    cv.startWindowThread()

    if state == 'test':
        cap = cv.VideoCapture('./data/test.avi')
    else:
        cap = cv.VideoCapture(0)

    while(cap.isOpened()):
        # reading the frame
        ret, frame = cap.read()

        if (ret == True):
            # resizing for faster detection
            frame = cv.resize(frame, (640, 480))
            # using a greyscale picture, also for faster detection
            gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

            # detect people in the image
            # returns the bounding boxes for the detected objects
            boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

            boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            print(boxes)

            for (xA, yA, xB, yB) in boxes:
                # display the detected boxes in the colour picture
                cv.rectangle(frame, (xA, yA), (xB, yB),
                                (0, 255, 0), 2)

            # displaying the frame
            cv.imshow('frame',frame)

            for (xA, yA, xB, yB) in boxes:
                print('human exists')
                count += 1
                if count > 10:
                    return frame

        if cv.waitKey(1) & 0xFF == ord('q'):
            # breaking the loop if the user types q
            # note that the video window must be highlighted!
            break

    cap.release()
    cv.destroyAllWindows()
    # the following is necessary on the mac,
    # maybe not on other platforms:
    cv.waitKey(1)

# START main execution block

while(True):

    # monitor(state="live")
    monitor()
    current_time, frame = capture_photo()
    test_img_inference()
    time.sleep(5)

# END main execution block