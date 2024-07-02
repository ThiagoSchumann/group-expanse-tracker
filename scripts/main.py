import inquirer
from event_manager import EventManager
from purchase_manager import PurchaseManager
from participant_manager import ParticipantManager

def main():
    event_manager = EventManager()
    purchase_manager = PurchaseManager()
    participant_manager = ParticipantManager()

    # Step 1: Create a new event
    event_questions = [
        inquirer.Text('name', message="What is the name of the event?"),
        inquirer.Text('date', message="What is the date of the event? (YYYY-MM-DD)")
    ]
    event_answers = inquirer.prompt(event_questions)
    event_name = event_answers['name']
    event_date = event_answers['date']

    event = event_manager.create_event(event_name, event_date)
    event_id = event['id']
    print(f"Event created with ID: {event_id}")

    # Step 2: Add purchases
    purchases = []
    total_amount = 0
    while True:
        purchase_questions = [
            inquirer.Text('description', message="Add purchase description"),
            inquirer.Text('amount', message="Add purchase amount"),
            inquirer.Confirm('continue', message="Add another purchase?", default=True)
        ]
        purchase_answers = inquirer.prompt(purchase_questions)
        description = purchase_answers['description']
        amount = float(purchase_answers['amount'])
        total_amount += amount
        purchase = purchase_manager.create_purchase(description, amount)
        purchases.append(purchase)
        print(f"Purchase created with ID: {purchase['id']}")
        if not purchase_answers['continue']:
            break

    # Step 3: Update the event page with purchases and total amount
    event_manager.update_event_with_purchases(event_id, purchases, total_amount)
    print(f"Event updated with total amount: {total_amount}")

    # Step 4: Add participants
    participants = []
    participant_names = []
    while True:
        participant_questions = [
            inquirer.Text('name', message="Add participant name"),
            inquirer.Confirm('continue', message="Add another participant?", default=True)
        ]
        participant_answers = inquirer.prompt(participant_questions)
        participant_names.append(participant_answers['name'])
        if not participant_answers['continue']:
            break

    amount_per_person = total_amount / len(participant_names)
    for name in participant_names:
        participant = participant_manager.create_participant(name, amount_per_person)
        participants.append(participant)
        print(f"Participant created with ID: {participant['id']}")

    # Step 5: Update the event page with participants
    event_manager.update_event_with_participants(event_id, participants)
    print("Event updated with participants")

if __name__ == "__main__":
    main()
