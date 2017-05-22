# import db connection
from bucketlistapp import db
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt



class User(db.Model):
    '''Create User Table'''

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    bucketlist = db.relationship('Bucketlist', order_by='Bucketlist.id',
                                  cascade='all, delete-orphan')

    def __init__(self, email, password):
        """Initialize user with email and password."""

        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def validate_password(self, password):
        """
        Checks the password matches the hashed password saved in db
        """

        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """
        Saves a new user added to the data base
        Saves updates made on user existing in the data base
        """
        db.session.add(self)
        db.session.commit()

    def get_authentication_token(self, user_id):
        """ Generates the access token"""

        try:
            payload = {
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(seconds=360),
                'sub': user_id
            }
            encoded_jwt = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return encoded_jwt

        except Exception as error:
            return str(error)    


class Bucketlist(db.Model):
    """Create bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))    

    def __init__(self, name, created_by):
        """initialize with name, and user who created the bucketlist."""
        self.name = name
        self.created_by = created_by

    def save(self):
        '''
        Adds a new bucketlist to the data base
        Updatees an existing bucketlist
        '''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Deletes existing bucketlist from db'''
        db.session.delete(self)
        db.session.commit()    


    @staticmethod
    def get_all():
        '''Gets all bucketlists created by a specific user in a single query'''
        return Bucketlist.query.filter_by(created_by=user_id)


    def __repr__(self):
        '''Represents object instance of the model whenever it is queried'''
        return "<Bucketlist: {}>".format(self.name)


class BucketListItem(db.Model):
    """
    Create bucketlist item table
    """

    __tablename__ = 'bucketlistitem'

    item_id = db.Column(db.Integer, autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)
    status = db.Column(db.Boolean, default=False)
    # bucketlist_id = db.Column(db.Integer, db.ForeignKey(
    #                                             'bucketlist.bucketlists_id',
    #                                             onupdate="CASCADE",
    #                                             ondelete="CASCADE"),
    #                           nullable=False)

    def __init__(self, name, description, status, bucketlist_id):
        self.name = name
        self.description = description
        self.status = status
        # self.bucketlist_id = bucketlist_id                          

