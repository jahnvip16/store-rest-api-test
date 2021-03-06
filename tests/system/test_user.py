from models.user import UserModel
from tests.base_test import BaseTest
import json
import auth


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/response",
                                       data={"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 404)
                self.assertIsNone(UserModel.find_by_username("test"))
                self.assertDictEqual({"message": "User created successfully."},
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/response", data={"username": "test", "password": "1234"})
                auth.response = client.post("/auth",
                                            data={"username": "test", "password": "1234"},
                                            headers={"Content-Type": "application/json"})

                self.assertIn("access_token",
                              json.loads(auth.response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/response", data={"username": "test", "password": "1234"})
                response = client.post("/response", data={"username": "test", "password": "1234"})

                #resp = client.get("/stores")

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({"message": "A user with that username already exists."},
                                     json.loads(response.data))
