from flask import Flask, request
from .secret_santa import SecretSanta
from .email_service import EmailService
from .firebase_crud import FirebaseCRUD
from models.party_model import Party

from flask import jsonify


# Create Flask app
app = Flask(__name__)

# Create email service
email_service = EmailService()

# Define '/SecretSanta/' route that only accepts POST requests
@app.route('/SecretSanta/', methods=['POST'])
def send_emails():
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
    # Estrai i dati dalla richiesta
    try:
        data = request.get_json()
        party_data = Party(**data)
    except (TypeError, ValueError) as e:
        return jsonify({"code": 400, "message": str(e)}), 400

    # Crea un nuovo documento nella collezione "Party"
    firebase_crud = FirebaseCRUD()
    result = firebase_crud.create("Party", party_data.__dict__)

    # Se il documento viene creato con successo, ritorna l'ID del documento
    if result['code'] == 200:
        return jsonify({"code": 200, "message": "Party created successfully", "id": result['id']}), 200
    else:
        return jsonify(result), result['code']

        
# Run Flask app in debug mode if the file is run as the main script
if __name__ == '__main__':
    app.run(debug=True)