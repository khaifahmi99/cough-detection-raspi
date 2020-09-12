import requests 

def predict(image_url):
    url = 'https://cough-classification.herokuapp.com/inference?url=' + image_url
    response = requests.get(url=url)
    return response.json()