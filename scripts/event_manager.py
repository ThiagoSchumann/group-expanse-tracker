import os
import json
from scripts.notion_client import NotionClient

class EventManager:
    def __init__(self):
        self.notion_client = NotionClient()
        self.event_database_id = os.getenv('EVENT_DATABASE_ID')

    def create_event(self, name, date):
        properties = {
            "Date": {
                "type": "date",
                "date": {"start": date}
            },
            "Total Amount": {
                "type": "number",
                "number": 0
            },
            "Name": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": name}
                    }
                ]
            }
        }
        return self.notion_client.create_page(self.event_database_id, properties)

    def update_event_with_purchases(self, event_id, purchases, total_amount):
        properties = {
            "Split Purchases": {
                "type": "relation",
                "relation": [{"id": purchase['id']} for purchase in purchases]
            },
            "Total Amount": {
                "type": "number",
                "number": total_amount
            }
        }
        return self.notion_client.update_page(event_id, properties)

    def update_event_with_participants(self, event_id, participants):
        properties = {
            "Participants": {
                "type": "relation",
                "relation": [{"id": participant['id']} for participant in participants]
            }
        }
        return self.notion_client.update_page(event_id, properties)
