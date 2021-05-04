"""
Base test case
"""
import io
import json
import unittest
from unittest.mock import patch
from contexter import Contexter
from flask import Flask
from werkzeug.datastructures import FileStorage

from app.api import configure_endpoints
from tests.test_json_data.workflow_test_examples import TEST_EXAMPLE_1, TEST_EXAMPLE_2, TEST_EXAMPLE_3


class ApiBaseTest(unittest.TestCase):

    app = Flask(__name__)
    configure_endpoints(app)
    client = app.test_client()

    url = ''


class TestWorkflowsAPI(ApiBaseTest):
    url = "/process-json"
    user_data = {"user_id": "105398891", "pin": 2090}
    account_data = {"user_id": "105398891", "balance": 0}
    patches = {}

    def get_patches(self):
        self.patches = {
            "app.wrappers.userservice_wrapper.validate_user_wrapper":
                {"return_value": {"is_valid": True}},
            "app.wrappers.financialservice_wrapper.get_bank_account":
                {"return_value": {"user_id": "105398891", "balance": 0}},
            "app.wrappers.userservice_wrapper.validate_user_wrapper":
                {"return_value": {"is_valid": True}},
            "app.wrappers.financialservice_wrapper.update_bank_account_balance":
                {"return_value": {'result': 'Account updated successfully'}}
        }

        return build_patches(self.patches)

    def test_valid_workflow(self):
        input_json = json.dumps(TEST_EXAMPLE_1).encode("utf-8")

        with Contexter(*self.get_patches()):
            mock_file = FileStorage(
                stream=io.BytesIO(input_json),
                filename="test_example1.json",
                content_type="application/json",
            )
            response = self.client.post(
                self.url,
                data={
                    "json_file": mock_file,
                },
                content_type="multipart/form-data"
            )
            self.assertEqual(response.status_code, 200)

    def test_user_not_found_workflow(self):
        input_json = json.dumps(TEST_EXAMPLE_2).encode("utf-8")

        with Contexter(*self.get_patches()):
            mock_file = FileStorage(
                stream=io.BytesIO(input_json),
                filename="test_example1.json",
                content_type="application/json",
            )
            response = self.client.post(
                self.url,
                data={
                    "json_file": mock_file,
                },
                content_type="multipart/form-data"
            )
            self.assertEqual(response.status_code, 404)

    def test_user_unauthorized_workflow(self):
        input_json = json.dumps(TEST_EXAMPLE_3).encode("utf-8")

        with Contexter(*self.get_patches()):
            mock_file = FileStorage(
                stream=io.BytesIO(input_json),
                filename="test_example1.json",
                content_type="application/json",
            )
            response = self.client.post(
                self.url,
                data={
                    "json_file": mock_file,
                },
                content_type="multipart/form-data"
            )
            self.assertEqual(response.status_code, 401)


def build_patches(patches_dict):
    patches = []
    for k, v in patches_dict.items():
        patcher = patch(k, **v)
        patches.append(patcher)
    return patches
