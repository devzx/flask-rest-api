from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from models.item import ItemModel


class Item(Resource):
    allowed_args = {
        'price': fields.Float(required=True),
    }

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    @use_args(allowed_args)
    def post(self, args, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item aleady exists'}
        item = ItemModel(name, **args)
        item.upsert()
        return item.json(), 201

    @use_args(allowed_args)
    def put(self, args, name):
        pass

    def delete(self, name):
        pass
