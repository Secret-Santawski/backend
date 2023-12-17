import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.api_core.exceptions import NotFound


class FirebaseCRUD:
    def __init__(self):
        # Initialize Firebase app
        if not firebase_admin._apps:
            # Use credentials from the JSON file specified in an environment variable
            secret_credentials = json.loads(os.environ.get("FIREBASE_CREDENTIALS"))
            if not secret_credentials:
                raise Exception(
                    "Firebase credentials not found. Please set the FIREBASE_CREDENTIALS environment variable."
                )

            cred = credentials.Certificate(secret_credentials)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create(self, collection, data):
        """Creates a document in the specified collection with the provided data."""
        try:
            doc_ref = self.db.collection(collection).document()
            doc_ref.set(data)
            doc_id = doc_ref.id
            return {
                "code": 200,
                "message": "Document created successfully",
                "id": doc_id,
            }
        except Exception as e:
            return {"code": 500, "message": f"Failed to create document: {str(e)}"}

    def read(self, collection, document_id):
        """Reads a document from the specified collection."""
        try:
            doc = self.db.collection(collection).document(document_id).get()
            # add document ID to data
            if doc.exists:
                data = doc.to_dict()
                data["id"] = doc.id
                return {
                    "code": 200,
                    "message": "Document read successfully",
                    "data": data,
                }
            else:
                return {"code": 404, "message": "Document not found"}
        except Exception as e:
            return {"code": 500, "message": f"Failed to read document: {str(e)}"}

    def update(self, collection, document_id, data):
        """Updates a document in the specified collection with the provided data."""
        try:
            self.db.collection(collection).document(document_id).update(data)
            return {"code": 200, "message": "Document updated successfully"}
        except NotFound:
            return {"code": 404, "message": "Document to update not found"}
        except Exception as e:
            return {"code": 500, "message": f"Failed to update document: {str(e)}"}

    def delete(self, collection, document_id):
        """Deletes a document from the specified collection."""
        try:
            self.db.collection(collection).document(document_id).delete()
            return {"code": 200, "message": "Document deleted successfully"}
        except NotFound:
            return {"code": 404, "message": "Document to delete not found"}
        except Exception as e:
            return {"code": 500, "message": f"Failed to delete document: {str(e)}"}

    def where(self, collection, field, operator, value):
        """Retrieves all documents from the specified collection that match the provided query."""
        try:
            docs = self.db.collection(collection).where(field, operator, value).get()
            # add document ID to data
            data = []
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data["id"] = doc.id
                data.append(doc_data)
            return {
                "code": 200,
                "message": "Documents retrieved successfully",
                "data": data,
            }
        except Exception as e:
            return {"code": 500, "message": f"Failed to retrieve documents: {str(e)}"}
