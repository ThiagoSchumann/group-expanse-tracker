import os
from flask import Flask, request, jsonify, send_from_directory
from scripts.event_manager import EventManager
from scripts.purchase_manager import PurchaseManager
from scripts.participant_manager import ParticipantManager

app = Flask(__name__, static_folder='web')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    event_manager = EventManager()
    purchase_manager = PurchaseManager()
    participant_manager = ParticipantManager()

    # Step 1: Create a new event
    event_name = data['eventName']
    event_date = data['eventDate']
    event = event_manager.create_event(event_name, event_date)
    event_id = event['id']

    # Step 2: Add purchases
    purchases = []
    total_amount = 0
    for purchase in data['purchases']:
        description = purchase['description']
        amount = purchase['amount']
        if amount is None:
            amount = 0
        total_amount += float(amount)
        purchase_obj = purchase_manager.create_purchase(description, amount)
        purchases.append(purchase_obj)

    # Step 3: Update the event page with purchases and total amount
    event_manager.update_event_with_purchases(event_id, purchases, total_amount)

    # Step 4: Add participants
    participants = []
    participant_names = [participant['name'] for participant in data['participants']]
    if len(participant_names) > 0:
        amount_per_person = total_amount / len(participant_names)
    else:
        amount_per_person = 0

    for name in participant_names:
        participant = participant_manager.create_participant(name, amount_per_person)
        participants.append(participant)

    # Step 5: Update the event page with participants
    event_manager.update_event_with_participants(event_id, participants)

    return jsonify({'message': 'Event created successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
