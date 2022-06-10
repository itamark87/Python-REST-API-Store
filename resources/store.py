from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):

        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'msg': f"Store with name {name} does not exist."}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {"message": f"A store with name {name} already exists."}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'msg': "An error occurred."}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'msg': 'Store deleted.'}, 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
