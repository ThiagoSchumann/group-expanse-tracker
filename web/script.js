let purchaseCount = 0;
let participantCount = 0;

function nextStep(step) {
    document.querySelectorAll('.form-step').forEach(step => {
        step.classList.remove('active');
    });
    document.getElementById(`step-${step}`).classList.add('active');
}

function addPurchase() {
    const description = document.getElementById('purchase-description').value;
    const amount = parseFloat(document.getElementById('purchase-amount').value.replace(',', '.')).toFixed(2);
    if (description && amount) {
        const table = document.getElementById('purchases-table').getElementsByTagName('tbody')[0];
        const newRow = table.insertRow();
        newRow.insertCell(0).textContent = description;
        newRow.insertCell(1).textContent = `R$ ${amount}`;
        document.getElementById('purchase-description').value = '';
        document.getElementById('purchase-amount').value = '';
    }
}

function addParticipant() {
    const name = document.getElementById('participant-name').value;
    if (name) {
        const table = document.getElementById('participants-table').getElementsByTagName('tbody')[0];
        const newRow = table.insertRow();
        newRow.insertCell(0).textContent = name;
        document.getElementById('participant-name').value = '';
    }
}

async function submitForm() {
    const eventName = document.getElementById('event-name').value;
    const eventDate = document.getElementById('event-date').value;

    const purchases = [];
    document.querySelectorAll('#purchases-table tbody tr').forEach(row => {
        const description = row.cells[0].textContent;
        const amount = parseFloat(row.cells[1].textContent.replace('R$ ', '').replace(',', '.'));
        purchases.push({ description, amount });
    });

    const participants = [];
    document.querySelectorAll('#participants-table tbody tr').forEach(row => {
        const name = row.cells[0].textContent;
        participants.push({ name });
    });

    const eventData = { eventName, eventDate, purchases, participants };
    console.log(eventData);

    // Sending data to the backend
    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(eventData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result);
        alert('Event created successfully!');
        resetForm();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to create event.');
    }
}

function resetForm() {
    document.getElementById('event-name').value = '';
    document.getElementById('event-date').value = '';
    document.querySelectorAll('.form-step').forEach(step => {
        step.classList.remove('active');
    });
    document.getElementById('step-1').classList.add('active');
    document.getElementById('purchases-table').getElementsByTagName('tbody')[0].innerHTML = '';
    document.getElementById('participants-table').getElementsByTagName('tbody')[0].innerHTML = '';
}
