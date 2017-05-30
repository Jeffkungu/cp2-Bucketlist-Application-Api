import unittest
import json
from bucketlistapp import create_app, db


class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        '''Set up tests variables.'''

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'email': 'jeffkungu@example.com',
            'password': 'jeffkungu',
            'username': 'jeff'
        }
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        '''Tests if user is registered successfully'''

        method = self.client().post(
                                    '/api/v1/auth/register',
                                    data=self.user_data)
        result = json.loads(method.data.decode())
        self.assertEqual(result['message'], "Successfully registered.")
        self.assertEqual(method.status_code, 201)

    def test_register_already_registered_user(self):
        '''
        Tests if an already registered user,
        can be registered using same details.
        '''

        method = self.client().post(
                                    '/api/v1/auth/register',
                                    data=self.user_data)
        # self.assertEqual(method.status_code, 201)
        method_two = self.client().post(
                                        '/api/v1/auth/register',
                                        data=self.user_data)
        # self.assertEqual(method_two.status_code, 202)
        result = json.loads(method_two.data.decode())
        self.assertEqual(result['message'], "Sorry, user already exists.")

    def test_user_login(self):
        '''
        Tests if user can login succesfully.
        Ristersts a user then logs-in the user.
        Checks for the return message after user is successfully logged in.
        '''

        reg_method = self.client().post(
                                        '/api/v1/auth/register',
                                        data=self.user_data)
        self.assertEqual(reg_method.status_code, 201)
        login_method = self.client().post(
                                          '/api/v1/auth/login',
                                          data=self.user_data)
        result = json.loads(login_method.data.decode())
        self.assertEqual(result['message'], "Log-in Successfull.")
        self.assertEqual(login_method.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_login_noneregistered_user(self):
        '''
        Tests if API can login user who is not registered.
        Creates an unregistered user and logs-in with the details.
        '''

        uregistered_user = {
            'email': 'johndoe@example.com',
            'password': 'johndoe1234'
        }

        login_method = self.client().post(
                                          '/api/v1/auth/login',
                                          data=uregistered_user)
        result = json.loads(login_method.data.decode())
        self.assertEqual(login_method.status_code, 401)
        self.assertEqual(
            result['message'], "Sorry, Please try registering firts.")
