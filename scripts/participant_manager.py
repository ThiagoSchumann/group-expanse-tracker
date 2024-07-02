import os
import json
from .notion_client import NotionClient

class ParticipantManager:
    def __init__(self):
        self.notion_client = NotionClient()
        self.participant_database_id = os.getenv('PARTICIPANT_DATABASE_ID')

    def create_participant(self, name, amount_due):
        properties = {
            "Status": {
                "type": "status",
                "status": {"name": "Not Paid"}
            },
            "Amount Due": {
                "type": "number",
                "number": amount_due
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
        return self.notion_client.create_page(self.participant_database_id, properties)
