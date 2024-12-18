from flask import Flask, request
from src.secret_santa import SecretSanta
from src.email_service import EmailService
from src.firebase_crud import FirebaseCRUD
from models.party_model import Party, PartyRequest
from models.user_model import User
from utilities.request_utils import create_instance_from_request
from dataclasses import asdict
import os
from flask_cors import CORS


# Create Flask app
app = Flask(__name__)

# Create email service
email_service = EmailService()

# Enable CORS with specific origins
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/SecretSanta/", methods=["POST"])
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
    return {"Status": "Success"}


@app.route("/CreateParty/", methods=["POST"])
def create_party():
    """
    Creates a new party.

    Returns:
        str: The ID of the created party.
    """

    # Get data from request body and create Party object
    party_data = create_instance_from_request(request, PartyRequest)

    # Create party in Firebase
    firebase_crud = FirebaseCRUD()
    return firebase_crud.create("Party", asdict(party_data))


@app.route("/UpdateParty/<party_id>", methods=["PUT"])
def update_party(party_id):
    """
    Updates a party.

    Args:
        party_id (str): The ID of the party to update.

    Returns:
        str: The status of the party update.
    """
    # Get data from request body and create Party object
    party_data = create_instance_from_request(request, PartyRequest)

    # Update party in Firebase
    firebase_crud = FirebaseCRUD()
    return firebase_crud.update("Party", asdict(party_data))


@app.route("/CreateUser/<party_id>", methods=["POST"])
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
    if message["code"] == 200:
        party = firebase_crud.read("Party", party_id)
        if party["code"] == 200 and party["data"]["ownerId"] == "":
            firebase_crud.update("Party", party_id, {"ownerId": message["id"]})

    return message


@app.route("/UpdateUser/<user_id>", methods=["PUT"])
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

    # Convert to dict
    user_dict = {
        key: value for key, value in asdict(user_data).items() if key != "party_id"
    }

    # Update user in Firebase
    firebase_crud = FirebaseCRUD()
    return firebase_crud.update("User", user_id, user_dict)


@app.route("/DeleteUser/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a user.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        str: The status of the user deletion.
    """

    # Delete user in Firebase
    firebase_crud = FirebaseCRUD()
    return firebase_crud.delete("User", user_id)


# Get all parties where you user email is accociated with
# Get email as a query parameter
@app.route("/GetParties/", methods=["GET"])
def get_parties():
    """
    Gets all parties where the user with the specified email is associated with.

    Returns:
        dict: A dictionary containing the status of the operation and the parties.
    """

    # Get email from query parameter
    user_email = request.args.get("email")

    # Ensure user_email is provided
    if not user_email:
        return {"code": 400, "message": "User email is required"}

    # Get all the party_id from users with the specified email
    # and use them to get the parties names
    firebase_crud = FirebaseCRUD()
    users = firebase_crud.where("User", "email", "==", user_email)
    if users["code"] == 200:
        parties = []
        for user in users["data"]:
            party = firebase_crud.read("Party", user["party_id"])
            if party["code"] == 200:
                parties.append(party["data"])
        return {
            "code": 200,
            "message": "Parties retrieved successfully",
            "data": parties,
        }
    else:
        return users


@app.route("/GetParty/<party_id>/<owner_id>", methods=["GET"])
@app.route("/GetParty/<party_id>", methods=["GET"])
def get_party(party_id, owner_id=None):
    """
    Gets a party with the specified ID.

    Args:
        party_id (str): The ID of the party to get.
        owner_id (str): The ID of the owner of the party.

    Returns:
        dict: A dictionary containing the party information.
    """
    # Get party from Firebase
    print(party_id)
    firebase_crud = FirebaseCRUD()
    party = firebase_crud.read("Party", party_id)

    # Ensure party exists
    if party["code"] == 200:
        # Get all users from Firebase associated with the party
        users = firebase_crud.where("User", "party_id", "==", party_id)
        if users["code"] == 200:
            party["data"]["users"] = users["data"]
            # if owner id is not null and the owner id is in the users list, then return all party and user data including the owner id and the user ids
            if owner_id is not None and any(user["id"] == owner_id for user in users["data"]):
                return {
                    "code": 200,
                    "message": "Party retrieved successfully",
                    "data": party["data"],
                }
            # if owner id is not null and the owner id is not in the users list, then return error
            elif owner_id is not None and not any(user["id"] == owner_id for user in users["data"]):
                return {
                    "code": 400,
                    "message": "Owner id is not valid",
                }
            # if owner id is null, then return only the party data without the owner_id and the user ids
            else:
                return {
                    "code": 200,
                    "message": "Party retrieved successfully",
                    "data": {
                        key: [
                            {k: v for k, v in user.items() if k != "id"}
                            for user in value
                        ] if key == "users" else value
                        for key, value in party["data"].items()
                        if key not in ["ownerId"]
                    }
                }
    return party


# Run Flask
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
