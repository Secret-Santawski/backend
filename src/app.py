from flask import Flask, request
from src.secret_santa import SecretSanta
from src.email_service import EmailService
from src.firebase_crud import FirebaseCRUD
from models.party_model import Party
from models.user_model import User
from utilities.request_utils import create_instance_from_request
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

@app.route('/UpdateParty/<party_id>', methods=['PUT'])
def update_party(party_id):
    """
    Updates a party.

    Args:
        party_id (str): The ID of the party to update.

    Returns:
        str: The status of the party update.
    """
    # Get data from request body and create Party object
    party_data = create_instance_from_request(request, Party)

    # Update party in Firebase
    party_dict = asdict(party_data)
    firebase_crud = FirebaseCRUD()
    return firebase_crud.update("Party", party_id, party_dict)

@app.route('/CreateUser/<party_id>', methods=['POST'])
def create_user(party_id):
    """
    Creates a new user.

    Args:
        party_id (str): The ID of the party to which the user belongs.
    
    Returns:
        str: The ID of the created user.
    """


    # Get data from request body and create User object
    user_data = create_instance_from_request(request, User)
    user_data.party_id = party_id
    
    # Create user in Firebase
    user_dict = asdict(user_data)
    firebase_crud = FirebaseCRUD()
    message = firebase_crud.create("User", user_dict)

    # If he's the first user to join the party, update the party's ownerId with his ID
    if message['code'] == 200:
        party = firebase_crud.read("Party", party_id)
        if party['code'] == 200 and party['data']['ownerId'] == '':
            firebase_crud.update("Party", party_id, {'ownerId': message['id']})
    
    return message

@app.route('/UpdateUser/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a user.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        str: The status of the user update.
    """

    # Create User object from request data
    user_data = create_instance_from_request(request, User)

    # Convert to dict and remove 'party_id'
    user_dict = {key: value for key, value in asdict(user_data).items() if key != 'party_id'}

    # Update user in Firebase
    firebase_crud = FirebaseCRUD()
    return firebase_crud.update("User", user_id, user_dict)

# Run Flask 
if __name__ == '__main__':
    app.run(port=5001)