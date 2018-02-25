from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from models.item import ItemModel


class Item(Resource):
    allowed_args = {
        'price': fields.Float(required=True),
        'store_id': fields.Integer(required=True),
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
        item.save_to_db()
        return item.json(), 201

    @use_args(allowed_args)
    def put(self, args, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.price = args['price']
            item.save_to_db()
            return item.json(), 200
        item = ItemModel(name, **args)
        item.save_to_db()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
