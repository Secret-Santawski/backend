# In tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
from src.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('src.app.SecretSanta', autospec=True)
    @patch('src.app.email_service', new_callable=MagicMock)
    def test_send_emails(self, mock_email_service, mock_secret_santa):
        # Setup the mock for SecretSanta
        mock_secret_santa_instance = mock_secret_santa.return_value

        # Call the send_emails endpoint
        response = self.app.post('/SecretSanta/', json={'players': []})

        # Verify that SecretSanta was called with the correct parameters
        mock_secret_santa.assert_called_once_with({'players': []}, mock_email_service)

        # Verify that assign_and_send_emails was called
        assert mock_secret_santa_instance.assign_and_send_emails.called

        # Verify that the response is correct
        self.assertEqual(response.get_json(), {'Status': 'Success'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
