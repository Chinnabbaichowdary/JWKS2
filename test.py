import unittest
from app import app, initialize_database, generate_rsa_keys
import os
import re

class FlaskServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure the database is initialized and keys are generated
        initialize_database()
        generate_rsa_keys()
        # Configure Flask app for testing
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_server_response(self):
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 404, "Root path should not return 404")

    def test_db_presence(self):
        self.assertTrue(os.path.isfile("./totally_not_my_privateKeys.db"), "Database file should exist")

class FlaskAuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_auth_methods(self):
        # Testing different HTTP methods on /auth endpoint
        methods = ['get', 'patch', 'put', 'delete', 'head']
        for method in methods:
            response = getattr(self.client, method)('/auth')
            self.assertEqual(response.status_code, 405, f"Method {method.upper()} should not be allowed on /auth")

    def test_auth_post_response(self):
        # Test POST request to /auth endpoint
        response = self.client.post('/auth')
        self.assertEqual(response.status_code, 200, "POST to /auth should return status code 200")

class FlaskJWKSTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_jwks_methods(self):
        # Testing different HTTP methods on /.well-known/jwks.json endpoint
        methods = ['post', 'patch', 'put', 'delete', 'head']
        for method in methods:
            response = getattr(self.client, method)('/.well-known/jwks.json')
            self.assertEqual(response.status_code, 405, f"Method {method.upper()} should not be allowed on /.well-known/jwks.json")

    def test_jwks_get_response(self):
        # Test GET request to /.well-known/jwks.json endpoint
        response = self.client.get('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200, "GET to /.well-known/jwks.json should return status code 200")

class FlaskResponseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_jwks_response_format(self):
        # Testing JWKS response format
        response = self.client.get('/.well-known/jwks.json')
        self.assertTrue('keys' in response.json, "JWKS response should contain 'keys'")
        # Additional tests for key details can be added here

    def test_auth_response_format(self):
        # Test that POST to /auth returns JWT in expected format
        response = self.client.post('/auth')
        self.assertTrue(re.match(r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$', response.json['jwt']), 
                        "JWT should be in the correct format")

if __name__ == '__main__':
    unittest.main()
