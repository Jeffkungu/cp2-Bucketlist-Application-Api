from . import blueprint
from bucketlistapp.models import User
from flask.views import MethodView
from flask import make_response, request, jsonify
import re


class UserRegistration(MethodView):
    '''Define a class based view for user registration method'''

    def post(self):
        '''
        Checks if user exists in database,
        if not creates a new user and adds to the data base.
        '''

        check_user = User.query.filter_by(email=request.data['email']).first()

        if not check_user:
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                username = post_data['username']
                match = re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)
                if email is None or password is None:
                    response = {
                        'message': 'Invalid input. Check email or password'}
                    return jsonify(response)
                if match:
                    check_user = User(
                        email=email, password=password, username=username)
                    check_user.save()

                    response = {
                        'message': 'Successfully registered.'
                    }
                    return make_response(jsonify(response)), 201
                else:
                    response = {'message': 'Invalid email input'}
                    return jsonify(response)
            except Exception as error:
                response = {
                    'message': str(error)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'Sorry, user already exists.'
            }
            return make_response(jsonify(response)), 409


class UserLogin(MethodView):
    '''Define a class based view for user login method'''

    def post(self):
        '''
        Checks if user exists in database, then generates access token.
        if not returns a message to prompt user to try registering first.
        '''

        try:
            fetched_user = User.query.filter_by(
                email=request.data['email']).first()
            if fetched_user and fetched_user.validate_password(request.data['password']):
                gen_token = fetched_user.get_authentication_token(
                    (fetched_user.id))
                if gen_token:
                    response = {
                        'message': 'Log-in Successfull.',
                        'access_token': gen_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Sorry, login info you submitted might not be registered. Please try registering firts.'
                }
                return make_response(jsonify(response)), 401
        except Exception as error:
            response = {
                'message': str(error)
            }
            return make_response(jsonify(response)), 500


user_registration = UserRegistration.as_view('register_user')
user_login = UserLogin.as_view('login_user')

blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=user_registration,
    methods=['POST'])

blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=user_login,
    methods=['POST'])
