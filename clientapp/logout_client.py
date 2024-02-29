import requests
from getpass import getpass
from datetime import datetime
import json

class NewsClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = None

    def login(self, url):
        self.base_url = url
        username = input("Username: ")
        password = getpass()
        login_data = {'username': username, 'password': password}
        response = self.session.post(f"{self.base_url}/api/login", json=login_data)
        if response.status_code == 200:
            print('Login successful.')
        else:
            try:
                error_message = response.json()
            except json.decoder.JSONDecodeError:
                error_message = response.text
            print('Login failed. Error:', error_message)


    def logout(self):
        if not self.base_url:
            print('Logout failed. Base URL is not set.')
            return

        response = self.session.post(f"{self.base_url}/api/logout")
        if response.status_code == 200:
            print('Logout successful.')
        else:
            try:
                error_message = response.json()
            except json.decoder.JSONDecodeError:
                error_message = response.text
            print('Logout failed. Error:', error_message)


    def post_story(self):
        headline = input("\nEnter the headline of the story: ")
        category = input("Category (pol/art/tech/trivia): ")
        region = input("Region relevant to the story: ")
        details = input("Additional details about the story: ")
        story_data = {'headline': headline, 'category': category, 'region': region, 'details': details}
        response = self.session.post(f"{self.base_url}/api/stories", json=story_data)
        if response.status_code == 201:
            print('Story posted successfully.')
        else:
            print('Failed to post story. Error:', response.text)

    def get_stories(self, news_id=None, category=None, region=None, date=None):
        print("get_stories region: ", region)
        params = {'story_cat': category, 'story_region': region, 'story_date': date}
        if news_id:
            response = self.session.get(f"{self.base_url}/api/stories/{news_id}", params=params)
        else:
            response = self.session.get(f"{self.base_url}/api/stories", params=params)
            print("Response: ", response.text)
        if response.status_code == 200:
            print('Story requested successfully.')
            print('Response:', response.json())
        elif response.status_code == 404:
            print('No stories found.')
        else:
            print('Failed to get story. Error:', response.text)

    def delete_story(self, story_key):
        response = self.session.delete(f"{self.base_url}/api/stories/{story_key}")
        if response.status_code == 200:
            print("Story deleted successfully.")
        elif response.status_code == 404:
            print("Story not found.")
        else:
            print("Failed to delete story. Error:", response.text)

    def list_services(self):
        dir_url = 'http://newssites.pythonanywhere.com/api/directory'
        response = self.session.get(dir_url)
        if response.status_code == 200:
            print('List of news services:')
            print(json.dumps((response.json()), indent=4))
        else:
            print('Failed to retrieve list of services. Error:', response.text)

    def execute_command(self, command):
        if command == 'login':
            url = input("Enter service URL: ")
            self.login(url)
        elif command == 'logout':
            self.logout()
        elif command == 'post':
            self.post_story()
        elif command.startswith('news'):
            args = command.split()[1:]
            news_id = category = region = date = None
            for arg in args:
                if arg.startswith('-id='):
                    news_id = arg.split('=')[1].strip('"')
                elif arg.startswith('-cat='):
                    category = arg.split('=')[1].strip('"')
                elif arg.startswith('-reg='):
                    region = arg.split('=')[1].strip('"')
                elif arg.startswith('-date='):
                    date = arg.split('=')[1].strip('"')

            if category is None:
                category = '*'
            if region is None:
                region = '*'
            if date is None:
                date = '*'
            self.get_stories(news_id=news_id, category=category, region=region, date=date)
        elif command == 'list':
            self.list_services()
        elif command.startswith('delete'):
            story_key = command.split()[1]
            self.delete_story(story_key)
        else:
            print("This command is not valid, please try again")


if __name__ == "__main__":
    client = NewsClient()
    while True:
        command = input("\nEnter command: ")
        if command == 'exit':
            break
        client.execute_command(command)
