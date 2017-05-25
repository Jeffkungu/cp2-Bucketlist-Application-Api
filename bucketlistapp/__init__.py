import os.path
import sys
import flask_sqlalchemy

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import make_response, request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from bucketlistapp.models import Bucketlist, BucketListItem, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def create_andget_bucketlists():
        '''
        Creates new bucketlist
        Login is required.
        '''

        header = request.headers['Authorization']
        get_token = header

        if get_token:
            user = User.decode_token(get_token)
            if not isinstance(user, str):
                if request.method == 'POST':
                    try:
                        bucketlist_name = str(request.data.get('name', ''))
                        if bucketlist_name:
                            bucketlist = Bucketlist(name=bucketlist_name, created_by=user)
                            bucketlist.save()
                            response = jsonify({
                                    'id': bucketlist.id,
                                    'name': bucketlist.name,
                                    'date_created': bucketlist.date_created,
                                    'date_modified': bucketlist.date_modified,
                                    'created_by': user
                            })
                            response.status_code = 201
                            return response
                    except Exception as error:
                        response = {
                            'message': str(error)
                        }
                        return make_response(jsonify(response)), 401

                if request.method == 'GET':
                    try:
                        if request.args.get("page"):
                            page = int(request.args.get("page"))
                        else:
                            page = 1
                        if request.args.get("limit") and int(request.args.get("limit"))<100:
                            limit = int(request.args.get("limit"))
                        else:
                            limit = 20
                        fetch_bucketlists_object = Bucketlist.query.filter_by(created_by=user).paginate(page, limit, False)
                        fetch_bucketlists = fetch_bucketlists_object.items
                        bucketlists = []

                        if fetch_bucketlists_object.has_next:
                            nextpage = "/bucketlists/?page=" + str(page + 1) + "&limit=" + str(limit)
                        else:
                            nextpage = None

                        if fetch_bucketlists_object.has_prev:
                            previouspage = "/bucketlists/?page=" + str(page - 1) + "&limit=" + str(limit)
                        else:
                            previouspage = None 
                        
                        if request.args.get('q'):
                            q = str(request.args.get('q')).lower()
                            fetch_bucketlists_object = Bucketlist.query.filter(Bucketlist.name.like('%{}%'.format(q))).filter_by(
                                                                created_by=user).paginate(page, limit, False)
                        for bucketlist in fetch_bucketlists:
                            data = {
                                    'id': bucketlist.id,
                                    'name': bucketlist.name,
                                    'date_created': bucketlist.date_created,
                                    'date_modified': bucketlist.date_modified,
                                    'created_by': bucketlist.created_by
                            }
                            bucketlists.append(data)
                            response = {
                                "nextpage": nextpage,
                                "Previouspage": previouspage,
                                "Data": bucketlists
                            }
                        return make_response(jsonify(response)), 200

                    except Exception as error:
                        response = {
                            'message': str(error)
                        }
                        return make_response(jsonify(response)), 401    
            else:
                message = user
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    
    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def get_andupdate_bucketlistid(id, **kwargs):
        '''
        Retrieves a bucketlist using its id.
        Updates the bucketlist using the PUT method
        Deletes the bucketlist using the delete method
        '''

        header = request.headers['Authorization']
        get_token = header

        if get_token:
            user = User.decode_token(get_token)
            if not isinstance(user, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()

                if not bucketlist:
                    abort(404)

                if request.method == 'GET':
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified
                    })
                    response.status_code = 200
                    return response

                if request.method == 'PUT':
                    bucketlist_name = str(request.data.get('name', ''))
                    bucketlist.name = bucketlist_name
                    bucketlist.save()
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified
                    })
                    response.status_code = 200
                    return response

                if request.method == 'DELETE':
                    bucketlist.delete()
                    return {"message": "bucketlist {} was successfully deleted.".format(bucketlist.id)}, 200

            else:
                message = user
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:id>/items', methods=['POST', 'GET'])
    def create_andget_bucketlistsitems(id, **kwargs):
        '''
        Creates bucketlist items.
        Login is required
        '''

        header = request.headers['Authorization']
        get_token = header

        if get_token:
            user = User.decode_token(get_token)
            if not isinstance(user, str):
                if request.method == 'POST':
                    try:
                        bucketlist = Bucketlist.query.filter_by(id=id).first()
                        if bucketlist:
                            bucketlist_name = str(request.data.get('name', ''))
                            if bucketlist_name:
                                bucketlist_item = BucketListItem(name=bucketlist_name, id=id)
                                bucketlist_item.save()
                                response = jsonify({
                                    'id': bucketlist_item.id,
                                    'name': bucketlist_item.name,
                                    'date_created': bucketlist_item.date_created,
                                    'date_modified': bucketlist_item.date_modified
                                })
                                return make_response(response), 201
                               
                            else:
                                response = jsonify({
                                    "message": "No name, please give the item a name."
                                })
                                return make_response(response), 400
                        else:
                            abort(404)
                    except Exception as error:
                        response = {
                            'message': str(error)
                        }
                        return make_response(jsonify(response)), 401
                else:
                    abort(400)

    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
    def get_andupdate_bucketlistsitems(id, item_id, **kwargs):
        '''
        Retrieves a bucketlist item using its id.
        Updates the bucketlist item using the PUT method
        Deletes the bucketlist item using the delete method
        '''

        header = request.headers['Authorization']
        get_token = header

        if get_token:
            user = User.decode_token(get_token)
            if not isinstance(user, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                bucketlist_item = BucketListItem.query.filter_by(item_id=id).first()

                if not bucketlist:
                    abort(404)

                if not bucketlist_item:
                    abort(404)

                if request.method == 'PUT':
                    item_name = str(request.data.get('name', ''))

                    if item_name:
                        bucketlist_item.name = item_name
                        bucketlist_item.save()
                        response = {
                            'id': bucketlist_item.id,
                            'name': bucketlist_item.name,
                            'date_created': bucketlist_item.date_created,
                            'date_modified': bucketlist_item.date_modified
                        }
                        return make_response(jsonify(response)), 200
                    else:
                        response = jsonify({
                            "message": "Error. Invalid item"
                        })
                        return make_response(response), 400

                if request.method == 'DELETE':
                    bucketlist_item.delete()
                    return {"message": "Item {} was successfully deleted.".format(bucketlist_item.id)}, 200

            else:
                message = user
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    from .user import blueprint
    app.register_blueprint(blueprint)
    return app

        