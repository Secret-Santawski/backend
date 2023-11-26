import unittest
from unittest.mock import patch, MagicMock
from src.secret_santa import SecretSanta

class TestSecretSanta(unittest.TestCase):
    @patch('json.load')
    @patch('builtins.open', new_callable=MagicMock)
    def test_init(self, mock_open, mock_json_load):
        # Setup the mock for json.load
        mock_json_load.return_value = ['category1', 'category2', 'category3']

        # Mock per il gestore di contesto usato con 'open'
        file_mock = MagicMock()
        mock_open.return_value.__enter__.return_value = file_mock

        # Create an instance of the SecretSanta class
        data = {'players': []}
        email_service = MagicMock()
        secret_santa = SecretSanta(data, email_service)

        # Verify that open was called with the correct parameters
        mock_open.assert_called_once_with('categories.json', 'r')

        # Verify that json.load was called with the file mock
        mock_json_load.assert_called_once_with(file_mock)

        # Verify that the attributes are set correctly
        self.assertEqual(secret_santa.data, data)
        self.assertEqual(secret_santa.email_service, email_service)
        self.assertEqual(secret_santa.categories, ['category1', 'category2', 'category3'])
        self.assertEqual(secret_santa.available_categories, ['category1', 'category2', 'category3'])

if __name__ == '__main__':
    unittest.main()
