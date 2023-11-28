# In tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
from src.app import app
from models.party_model import Party


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
    
    @patch('src.app.FirebaseCRUD')
    def test_create_party(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.create.return_value = {'code': 200, 'id': '123'}

        # Prepare the test data
        test_data = {
            'name': 'Test Party',
            'budget': 100,
            'categories': ['Food', 'Games'],
            'ownerId': 'owner123',
            'closed': False
        }

        # Call the create_party endpoint
        response = self.app.post('/CreateParty/', json=test_data)

        # Verify that FirebaseCRUD.create was called with the correct parameters
        mock_firebase_crud_instance.create.assert_called_once()
        called_args, _ = mock_firebase_crud_instance.create.call_args
        self.assertEqual(called_args[0], 'Party')
        self.assertDictEqual(called_args[1], test_data)

        # Verify that the response is correct
        self.assertEqual(response.get_json(), {'code': 200, 'message': 'Party created successfully', 'id': '123'})
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()
