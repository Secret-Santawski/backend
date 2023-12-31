# In tests/test_app.py
import unittest
from unittest.mock import patch, MagicMock
from src.app import app
from models.party_model import Party, PartyRequest
from models.user_model import User


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch("src.app.SecretSanta", autospec=True)
    @patch("src.app.email_service", new_callable=MagicMock)
    def test_send_emails(self, mock_email_service, mock_secret_santa):
        # Setup the mock for SecretSanta
        mock_secret_santa_instance = mock_secret_santa.return_value

        # Call the send_emails endpoint
        response = self.app.post("/SecretSanta/", json={"players": []})

        # Verify that SecretSanta was called with the correct parameters
        mock_secret_santa.assert_called_once_with({"players": []}, mock_email_service)

        # Verify that assign_and_send_emails was called
        assert mock_secret_santa_instance.assign_and_send_emails.called

        # Verify that the response is correct
        self.assertEqual(response.get_json(), {"Status": "Success"})
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_create_party(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.create.return_value = {
            "code": 200,
            "message": "Document created successfully",
            "id": "123",
        }

        # Prepare the test data
        test_data = {
            "name": "Test Party",
            "budget": 100,
            "categories": ["Food", "Games"]
        }

        # Call the create_party endpoint
        response = self.app.post("/CreateParty/", json=test_data)

        # Verify that FirebaseCRUD.create was called with the correct parameters
        mock_firebase_crud_instance.create.assert_called_once()
        called_args, _ = mock_firebase_crud_instance.create.call_args
        self.assertEqual(called_args[0], "Party")
        self.assertDictEqual(called_args[1], test_data)

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {"code": 200, "message": "Document created successfully", "id": "123"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_update_party(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.update.return_value = {
            "code": 200,
            "message": "Document updated successfully",
        }

        # Prepare the test data
        test_data = {
            "name": "Test Party",
            "budget": 100,
            "categories": ["Food", "Games"]
        }

        # Call the update_party endpoint
        response = self.app.put("/UpdateParty/123", json=test_data)

        # Verify that FirebaseCRUD.update was called with the correct parameters
        mock_firebase_crud_instance.update.assert_called_once()
        called_args, _ = mock_firebase_crud_instance.update.call_args
        self.assertEqual(called_args[0], "Party")
        self.assertEqual(called_args[1], test_data)

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {"code": 200, "message": "Document updated successfully"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_create_user(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.create.return_value = {
            "code": 200,
            "message": "Document created successfully",
            "id": "123",
        }

        # Prepare the test data
        test_data = {
            "username": "Test User",
            "email": "test@test.com",
            "suggested_categories": ["Food", "Games"],
            "party_id": "party123",
        }

        # Call the create_user endpoint
        response = self.app.post("/CreateUser/party123", json=test_data)

        # Verify that FirebaseCRUD.create was called with the correct parameters
        mock_firebase_crud_instance.create.assert_called_once()
        called_args, _ = mock_firebase_crud_instance.create.call_args
        self.assertEqual(called_args[0], "User")
        self.assertDictEqual(called_args[1], test_data)

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {"code": 200, "message": "Document created successfully", "id": "123"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_update_user(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.update.return_value = {
            "code": 200,
            "message": "Document updated successfully",
        }

        test_data = {
            "username": "Test User",
            "email": "test@test.com",
            "suggested_categories": ["Food", "Games"],
            "party_id": "party1234",  # Include party_id in test data
        }

        # Expected data without 'party_id'
        expected_data = {
            "username": "Test User",
            "email": "test@test.com",
            "suggested_categories": ["Food", "Games"]
            # 'party_id' is intentionally omitted
        }

        # Call the update_user endpoint
        response = self.app.put("/UpdateUser/123", json=test_data)

        # Verify that FirebaseCRUD.update was called with the correct parameters
        mock_firebase_crud_instance.update.assert_called_once()
        called_args, _ = mock_firebase_crud_instance.update.call_args
        self.assertEqual(called_args[0], "User")
        self.assertEqual(called_args[1], "123")
        self.assertDictEqual(called_args[2], expected_data)

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {"code": 200, "message": "Document updated successfully"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_delete_user(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.delete.return_value = {
            "code": 200,
            "message": "Document deleted successfully",
        }

        # Call the delete_user endpoint
        response = self.app.delete("/DeleteUser/123")

        # Verify that FirebaseCRUD.delete was called with the correct parameters
        mock_firebase_crud_instance.delete.assert_called_once()
        called_args, _ = mock_firebase_crud_instance.delete.call_args
        self.assertEqual(called_args[0], "User")
        self.assertEqual(called_args[1], "123")

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {"code": 200, "message": "Document deleted successfully"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_get_parties(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.where.return_value = {
            "code": 200,
            "data": [{"party_id": "party123"}, {"party_id": "party456"}],
        }
        mock_firebase_crud_instance.read.side_effect = [
            {"code": 200, "data": {"name": "Party 1"}},
            {"code": 200, "data": {"name": "Party 2"}},
        ]

        # Call the get_parties endpoint
        response = self.app.get("/GetParties/?email=test@test.com")

        # Verify that FirebaseCRUD.where was called with the correct parameters
        mock_firebase_crud_instance.where.assert_called_once_with(
            "User", "email", "==", "test@test.com"
        )

        # Verify that FirebaseCRUD.read was called with the correct parameters
        mock_firebase_crud_instance.read.assert_any_call("Party", "party123")
        mock_firebase_crud_instance.read.assert_any_call("Party", "party456")

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {
                "code": 200,
                "message": "Parties retrieved successfully",
                "data": [{"name": "Party 1"}, {"name": "Party 2"}],
            },
        )
        self.assertEqual(response.status_code, 200)

    @patch("src.app.FirebaseCRUD")
    def test_get_party(self, mock_firebase_crud):
        # Setup the mock for FirebaseCRUD
        mock_firebase_crud_instance = mock_firebase_crud.return_value
        mock_firebase_crud_instance.read.return_value = {
            "code": 200,
            "data": {
                "name": "Test Party",
                "budget": 100,
                "categories": ["Food", "Games"],
                "ownerId": "user123",
            },
        }
        mock_firebase_crud_instance.where.return_value = {
            "code": 200,
            "data": [
                {"id": "user123", "name": "User 1"},
                {"id": "user456", "name": "User 2"},
            ],
        }

        # Call the get_party endpoint without owner_id
        response = self.app.get("/GetParty/123")

        # Verify that FirebaseCRUD.read was called with the correct parameters
        mock_firebase_crud_instance.read.assert_called_once_with("Party", "123")

        # Verify that FirebaseCRUD.where was called with the correct parameters
        mock_firebase_crud_instance.where.assert_called_once_with(
            "User", "party_id", "==", "123"
        )

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {
                "code": 200,
                "message": "Party retrieved successfully",
                "data": {
                    "name": "Test Party",
                    "budget": 100,
                    "categories": ["Food", "Games"],
                    "users": [
                        {"name": "User 1"},
                        {"name": "User 2"},
                    ],
                },
            },
        )
        self.assertEqual(response.status_code, 200)

        # Call the get_party endpoint with valid owner_id
        response = self.app.get("/GetParty/123/user123")

        # Verify that FirebaseCRUD.read was called with the correct parameters
        mock_firebase_crud_instance.read.assert_called_with("Party", "123")

        # Verify that FirebaseCRUD.where was called with the correct parameters
        mock_firebase_crud_instance.where.assert_called_with(
            "User", "party_id", "==", "123"
        )

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {
                "code": 200,
                "message": "Party retrieved successfully",
                "data": {
                    "name": "Test Party",
                    "budget": 100,
                    "categories": ["Food", "Games"],
                    "ownerId": "user123",
                    "users": [
                        {"id": "user123" ,"name": "User 1"},
                        {"id": "user456", "name": "User 2"},
                    ],
                },
            },
        )
        self.assertEqual(response.status_code, 200)

        # Call the get_party endpoint with invalid owner_id
        response = self.app.get("/GetParty/123/invalid_owner")

        # Verify that FirebaseCRUD.read was called with the correct parameters
        mock_firebase_crud_instance.read.assert_called_with("Party", "123")

        # Verify that FirebaseCRUD.where was called with the correct parameters
        mock_firebase_crud_instance.where.assert_called_with(
            "User", "party_id", "==", "123"
        )

        # Verify that the response is correct
        self.assertEqual(
            response.get_json(),
            {
                "code": 400,
                "message": "Owner id is not valid",
            },
        )
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()