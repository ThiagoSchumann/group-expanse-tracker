import requests
import os
from dotenv import load_dotenv

class NotionClient:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv('NOTION_TOKEN')
        self.version = os.getenv('NOTION_VERSION')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': self.version
        }

    def create_page(self, parent_id, properties):
        url = 'https://api.notion.com/v1/pages/'
        data = {
            "parent": {"database_id": parent_id},
            "properties": properties
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_page(self, page_id, properties):
        url = f'https://api.notion.com/v1/pages/{page_id}'
        data = {"properties": properties}
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
