import unittest
from unittest.mock import MagicMock
from flask import Flask, request
from dataclasses import dataclass, field
from typing import List
from utils.request_utils import create_instance_from_request


app = Flask(__name__)

@dataclass
class MockDataClass:
    field1: str
    field2: int
    field3: List[str] = field(default_factory=list)
    field4: bool = False

class TestRequestUtils(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_instance_from_request_failure_invalid_data(self):
        with app.test_request_context(json={'field1': 'test', 'field2': 'invalid'}):
            result = create_instance_from_request(request, MockDataClass)
            self.assertIsInstance(result, tuple)
            response, status_code = result
            self.assertEqual(status_code, 400)
            self.assertIn("Invalid type for field field2", response.get_json()["message"])

    def test_create_instance_from_request_failure_invalid_data(self):
        with app.test_request_context(json={'field1': 'test', 'field2': 'invalid'}):
            result = create_instance_from_request(request, MockDataClass)
            self.assertIsInstance(result, tuple)
            response, status_code = result
            self.assertEqual(status_code, 400)
            self.assertIn("Invalid type for field field2", response.get_json()["message"])

    def test_create_instance_from_request_success(self):
        with app.test_request_context(json={'field1': 'test', 'field2': 123, 'field3': ['item1', 'item2'], 'field4': True}):
            result = create_instance_from_request(request, MockDataClass)
            self.assertIsInstance(result, MockDataClass)
            self.assertEqual(result.field1, 'test')
            self.assertEqual(result.field2, 123)
            self.assertEqual(result.field3, ['item1', 'item2'])
            self.assertEqual(result.field4, True)


if __name__ == '__main__':
    unittest.main()
