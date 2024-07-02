import os
import json
from .notion_client import NotionClient

class PurchaseManager:
    def __init__(self):
        self.notion_client = NotionClient()
        self.purchase_database_id = os.getenv('PURCHASE_DATABASE_ID')

    def create_purchase(self, description, amount):
        properties = {
            "Description": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": description}
                    }
                ]
            },
            "Amount": {
                "type": "number",
                "number": amount
            }
        }
        return self.notion_client.create_page(self.purchase_database_id, properties)
