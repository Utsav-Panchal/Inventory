from flask_jwt import JWT
from flask_restful import Api
from flask import Flask

# Import Resources over here
from authorization import authenticate, identity
from resources.InventoryResources import InventoryResource, ItemList
from resources.usersR import UserRegisterResource
from resources.CategoriesResorces import StoreList, Store
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory_data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/assignment_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'utsav'
api = Api(app)

# Resources adding
api.add_resource(UserRegisterResource, '/register')
api.add_resource(InventoryResource, '/inventory/<string:inventory_name>')
api.add_resource(ItemList, '/inventory/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # auth

if __name__ == "__main__":
    from models.db import db

    db.init_app(app)
    app.run(port=5001, debug=True)
