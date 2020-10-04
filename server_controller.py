import requests 

def predict_img(image_url):   
    # url = 'https://cough-classification.herokuapp.com/inference?type=image&url=' + image_url
    url = 'http://localhost:5000/inference?type=image&url=' + image_url
    print('Reaching endpoint...')
    response = requests.get(url=url)
    print('Endpoint reached')

    return response.json()

def predict_sound(sound_url):       
    # url = 'https://cough-classification.herokuapp.com/inference?type=sound&url=' + sound_url
    url = 'http://localhost:5000/inference?type=sound&url=' + sound_url
    print('Reaching endpoint...')
    response = requests.get(url=url)
    print('Endpoint reached')
    print(response.content)
    return response.json()