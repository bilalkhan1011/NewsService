import requests


url = "http://newssites.pythonanywhere.com/api/directory/"

login_data = 



import requests

def register_agency():
    directory_url =  "http://newssites.pythonanywhere.com/api/directory/"

    registration_data = {
        'agency_name': "Bilal Khan News Agency",
        'url': "ed18b5k.pythonanywhere.com",
        'agency_code': "BK00"
    }

    response = requests.post(directory_url, json=registration_data)
    print(response.text)
    print(response)

def main():


    register_agency()

