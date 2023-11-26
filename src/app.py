from flask import Flask, request
from .secret_santa import SecretSanta
from .email_service import EmailService

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

# Run Flask app in debug mode if the file is run as the main script
if __name__ == '__main__':
    app.run(debug=True)