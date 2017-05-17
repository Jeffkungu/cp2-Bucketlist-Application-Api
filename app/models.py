# import db connection
from app import db
import datetime



class Bucketlist(db.Model):
    """Create bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        '''Adds a new bucketlist to db'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Deletes existing bucketlist from db'''
        db.session.delete(self)
        db.session.commit()    


    @staticmethod
    def get_all():
        '''Gets all bucketlists in a single query'''
        return Bucketlist.query.all()


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
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)
    status = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
                                                'bucketlist.bucketlist_id',
                                                onupdate="CASCADE",
                                                ondelete="CASCADE"),
                              nullable=False)

    def __init__(self, name, description, status, bucketlist_id):
        self.name = name
        self.description = description
        self.status = status
        self.bucketlist_id = bucketlist_id                          


class User(db.Model):
    '''Create User Table'''

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    bucketlist = db.relationship('Bucketlist', backref='user',
                                 cascade='all,delete', passive_deletes=True)       
