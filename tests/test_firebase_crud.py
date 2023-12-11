import unittest
from unittest.mock import patch, MagicMock
from google.api_core.exceptions import NotFound
from src.firebase_crud import FirebaseCRUD
import os


class TestFirebaseCRUD(unittest.TestCase):
    @patch("firebase_admin.firestore.client")
    @patch("firebase_admin.credentials.Certificate")
    @patch("firebase_admin.initialize_app")
    def setUp(
        self, mock_initialize_app, mock_credentials_certificate, mock_firestore_client
    ):
        # Mock the initialization of the app
        mock_app = MagicMock()
        mock_initialize_app.return_value = mock_app

        # Mock the firestore client
        self.mock_db = MagicMock()
        mock_firestore_client.return_value = self.mock_db

        # Now FirebaseCRUD() can be instantiated without raising the 'default Firebase app does not exist' error
        self.firebase_crud = FirebaseCRUD()

    def test_create_document_success(self):
        # Mock Firestore set method

        self.mock_db.collection.return_value.document.return_value.set.return_value = (
            None
        )
        self.mock_db.collection.return_value.document.return_value.id = "test_id"
        response = self.firebase_crud.create("test_collection", {"data": "test"})
        self.assertEqual(
            response,
            {"code": 200, "message": "Document created successfully", "id": "test_id"},
        )

    def test_read_document_exists(self):
        # Mock Firestore get method for existing document
        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"data": "test"}
        self.mock_db.collection.return_value.document.return_value.get.return_value = (
            mock_doc
        )

        response = self.firebase_crud.read("test_collection", "test_document")
        self.assertEqual(
            response,
            {
                "code": 200,
                "message": "Document read successfully",
                "data": {"data": "test"},
            },
        )

    def test_read_document_not_exists(self):
        # Mock Firestore get method for non-existing document
        mock_doc = MagicMock()
        mock_doc.exists = False
        self.mock_db.collection.return_value.document.return_value.get.return_value = (
            mock_doc
        )

        response = self.firebase_crud.read("test_collection", "test_document")
        self.assertEqual(response, {"code": 404, "message": "Document not found"})

    def test_update_document_success(self):
        # Mock Firestore update method
        self.mock_db.collection.return_value.document.return_value.update.return_value = (
            None
        )

        response = self.firebase_crud.update(
            "test_collection", "test_document", {"updated_data": "new_test"}
        )
        self.assertEqual(
            response, {"code": 200, "message": "Document updated successfully"}
        )

    def test_update_document_not_found(self):
        # Mock Firestore update method to raise NotFound exception
        self.mock_db.collection.return_value.document.return_value.update.side_effect = NotFound(
            "test"
        )

        response = self.firebase_crud.update(
            "test_collection", "test_document", {"updated_data": "new_test"}
        )
        self.assertEqual(
            response, {"code": 404, "message": "Document to update not found"}
        )

    def test_delete_document_success(self):
        # Mock Firestore delete method
        self.mock_db.collection.return_value.document.return_value.delete.return_value = (
            None
        )

        response = self.firebase_crud.delete("test_collection", "test_document")
        self.assertEqual(
            response, {"code": 200, "message": "Document deleted successfully"}
        )

    def test_delete_document_not_found(self):
        # Mock Firestore delete method to raise NotFound exception
        self.mock_db.collection.return_value.document.return_value.delete.side_effect = NotFound(
            "test"
        )

        response = self.firebase_crud.delete("test_collection", "test_document")
        self.assertEqual(
            response, {"code": 404, "message": "Document to delete not found"}
        )

    def test_where_query_success(self):
        # Mock Firestore where method
        mock_collection = MagicMock()
        mock_document = MagicMock()
        mock_document.to_dict.return_value = {"data": "test"}
        mock_collection.where.return_value.get.return_value = [mock_document]
        self.mock_db.collection.return_value = mock_collection

        response = self.firebase_crud.where(
            "test_collection", "test_field", "==", "test_value"
        )
        self.assertEqual(
            response,
            {
                "code": 200,
                "message": "Documents retrieved successfully",
                "data": [{"data": "test"}],
            },
        )

    def test_where_query_failure(self):
        # Mock Firestore where method to raise exception
        mock_collection = MagicMock()
        mock_collection.where.side_effect = Exception("test")
        self.mock_db.collection.return_value = mock_collection

        response = self.firebase_crud.where(
            "test_collection", "test_field", "==", "test_value"
        )
        self.assertEqual(
            response, {"code": 500, "message": "Failed to retrieve documents: test"}
        )


if __name__ == "__main__":
    unittest.main()
