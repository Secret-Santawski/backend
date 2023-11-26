import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

# EmailService class for handling email operations
class EmailService:
    def __init__(self):
        # Get sender email and password from environment variables
        self.sender_email = os.environ.get("SENDER_EMAIL")
        self.sender_password = os.environ.get("SENDER_PASSWORD")

    # Function to send an email
    def send_email(self, recipient_email, subject, html_content):
        # Create a multipart message
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Create an alternative part for the message
        msgAlternative = MIMEMultipart('alternative')
        message.attach(msgAlternative)

        # Attach the HTML content to the message
        msgText = MIMEText(html_content, 'html')
        msgAlternative.attach(msgText)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as session:
            session.starttls()
            session.login(self.sender_email, self.sender_password)
            session.sendmail(self.sender_email, recipient_email, message.as_string())