from flask import Flask, request
from src.secret_santa import SecretSanta
from src.email_service import EmailService
from src.firebase_crud import FirebaseCRUD
from models.party_model import Party
from utilities.request_utils import create_instance_from_request


from flask import jsonify
from dataclasses import asdict


# Create Flask app
app = Flask(__name__)

# Create email service
email_service = EmailService()


@app.route('/SecretSanta/', methods=['POST'])
def send_emails():
    """
    Sends emails to assigned recipients based on the received data.

    Returns:
        dict: A dictionary indicating the status of the email sending process.
    """
    # Get data from request body
    data = request.get_json()
    
    # Create SecretSanta object with received data and email service
    secret_santa = SecretSanta(data, email_service)
    
    # Assign recipients and send emails
    secret_santa.assign_and_send_emails()
    
    # Return success status
    return {'Status': 'Success'}


@app.route('/CreateParty/', methods=['POST'])
def create_party(): 
    """
    Creates a new party.

    Returns:
        str: The ID of the created party.
    """
    # Get data from request body and create Party object
    party_data = create_instance_from_request(request, Party)

    # Create party in Firebase
    party_dict = asdict(party_data)
    firebase_crud = FirebaseCRUD()
    return firebase_crud.create("Party", party_dict)
        
# Run Flask 
if __name__ == '__main__':
    app.run()