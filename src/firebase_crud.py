import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.api_core.exceptions import NotFound

class FirebaseCRUD:
    def __init__(self):
        # Initialize Firebase app using credentials from the JSON file specified in an environment variable
        cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")
        if not cred_path:
            raise ValueError("The FIREBASE_CREDENTIALS_PATH environment variable is not set.")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create(self, collection, document_id, data):
        """Creates a document in the specified collection with the provided data."""
        try:
            self.db.collection(collection).document(document_id).set(data)
            return {"code": 200, "message": "Document created successfully"}
        except Exception as e:
            return {"code": 500, "message": f"Failed to create document: {str(e)}"}

    def read(self, collection, document_id):
        """Reads a document from the specified collection."""
        try:
            doc = self.db.collection(collection).document(document_id).get()
            if doc.exists:
                return {"code": 200, "message": "Document read successfully", "data": doc.to_dict()}
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
