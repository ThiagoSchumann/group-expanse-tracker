import requests
import os

class EventManager:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('EVENT_DATABASE_ID')
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def create_event(self, name, date):
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": name}}]},
                "Date": {"date": {"start": date}},
                "Total Amount": {"number": 0}
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_event_with_purchases(self, event_id, purchases, total_amount):
        url = f"https://api.notion.com/v1/pages/{event_id}"
        purchase_ids = [{"id": purchase['id']} for purchase in purchases]
        payload = {
            "properties": {
                "Split Purchases": {"relation": purchase_ids},
                "Total Amount": {"number": total_amount}
            }
        }
        response = requests.patch(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_event_with_participants(self, event_id, participants):
        url = f"https://api.notion.com/v1/pages/{event_id}"
        participant_ids = [{"id": participant['id']} for participant in participants]
        payload = {
            "properties": {
                "Participants": {"relation": participant_ids}
            }
        }
        response = requests.patch(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
