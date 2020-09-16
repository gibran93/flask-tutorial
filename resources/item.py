from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    # only the price element will be read from the json payload request
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item requires a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': f'Item {name} not found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Error Message': f'An item with name {name} already exists.'}, 400 # user request is bad

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) # data['price'], data['store_id']
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'Message': f'Item {name} was deleted.'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}