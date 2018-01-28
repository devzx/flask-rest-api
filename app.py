from flask import Flask
from flask_restful import Api
from flask_jwt_simple import JWTManager

from resources.item import Item, ItemList
from resources.user import UserRegister, UserList, UserLogin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tabels():
    db.create_all()


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/users')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
