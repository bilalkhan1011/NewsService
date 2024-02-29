import requests
from getpass import getpass
from datetime import datetime

r = requests.get ("http://127.0.0.1:8000/api/greet")
print (r.text)

login_url = 'http://127.0.0.1:8000/api/login'
logout_url = 'http://127.0.0.1:8000/api/logout'
poststories_url = 'http://127.0.0.1:8000/api/stories'
getstories_url = 'http://127.0.0.1:8000/api/stories'


session = requests.Session()

def login(username, password):

    login_data = {
        'username': username,
        'password': password
    }

    response = session.post(login_url, json=login_data)
    if response.status_code == 200:
        print('Login successful.', response.json())
    else:
        print('Login failed. Error:', response.json())



def logout():
    response = session.post(logout_url)
    if response.status_code == 200:
        print('Logout successful.', response.json())
    else:
        print('Logout failed. Error:', response.json())


def post_story(headline, category, region, details):

    story_data = {
        'headline': headline,
        'category': category,
        'region': region,
        'details': details
    }

    response = session.post(poststories_url, json=story_data)

    if response.status_code == 201:
        print('Story posted successfully.')

    else:
        print('Failed to post story. Error:', response.text)



def get_story(category, region, date):

    if date == '*':
        formatted_date = '*'
    else: 
         date_obj = datetime.strptime(date, '%d/%m/%Y')
         formatted_date = date_obj.strftime('%d/%m/%Y')

    story_data = {
    'story_cat': category,
    'story_region': region,
    'story_date': formatted_date
    }

    response = session.get(getstories_url, params=story_data)

    if response.status_code == 200:
        print('Story requested successfully.')
        print('Response:', response.json())  
    elif response.status_code == 404:
        print('No stories found.')
    else:
        print('Failed to get story oh NOOO. Error:', response.text)



def delete_story(key):

    delete_url = f"http://localhost:8000/api/stories/{key}"

    response = requests.delete(delete_url)

    if response.status_code == 200:
        print("Story deleted successfully.")
    elif response.status_code == 404:
        print("Story not found.")
    else:
        print("Failed to delete story. Error:", response.text)



# username = input("Username: ")
# password = getpass()
# login (username, password)
    
login("admin", "123")

# Perform actions after login

# headline = input ("\n Enter the headline of the story \n ")
# category = input ("\n Category (pol/art/tech/trivia): \n")
# region = input ("\n Region relevant to the story: \n")
# details = input ("\n Additional details about the story: \n")
#
#


#post_story("Smaller Tings", "art", "uk", "No idea")
get_story("*", "uk", "*")
#delete_story(73)


logout()




