import unittest
from unittest.mock import patch, ANY
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.email_service import EmailService

class TestEmailService(unittest.TestCase):
    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        # Setup the SMTP mock
        instance = mock_smtp.return_value.__enter__.return_value
        instance.sendmail.return_value = {}

        # Create an instance of the email service
        service = EmailService()

        # Set the email parameters
        recipient_email = 'test@example.com'
        subject = 'Test Subject'
        html_content = '<h1>Test Content</h1>'

        # Call the send_email method
        service.send_email(recipient_email, subject, html_content)

        # Verify that sendmail was called with the correct parameters
        instance.sendmail.assert_called_once_with(service.sender_email, recipient_email, ANY)

        # Verify that starttls was called
        self.assertTrue(instance.starttls.called)

        # Verify that login was called with the correct parameters
        instance.login.assert_called_once_with(service.sender_email, service.sender_password)

if __name__ == '__main__':
    unittest.main()
