from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from businesslogic.InventoryBL import InventoryBL, InventoryListBL


class InventoryResource(Resource):

    parse = reqparse.RequestParser()

    parse.add_argument('inventory_image',
                       required=False,
                       help="inventory_image can not be blank.")

    parse.add_argument('quantity',
                       required=False,
                       help="quantity can not be blank.")

    parse.add_argument('manufacturing_time',
                       required=False,
                       help="manufacturing_time can not be blank.")

    parse.add_argument('expiry_time',
                       required=False,
                       help="expiry_time can not be blank.")

    parse.add_argument('store_id',
                       type=int,
                       required=True,
                       help="category_id can not be blank.")

    @jwt_required()
    def get(self, inventory_name):
        get_item = InventoryBL(inventory_name=inventory_name)
        return get_item.get_res()

    def post(self, inventory_name):
        data = InventoryResource.parse.parse_args()
        post_item = InventoryBL(inventory_name=inventory_name)
        return post_item.post_res(data)

    def delete(self, inventory_name):
        del_item = InventoryBL(inventory_name=inventory_name)
        return del_item.del_res()

    def put(self, inventory_name):

        data = InventoryResource.parse.parse_args()

        del_item = InventoryBL(inventory_name=inventory_name)
        return del_item.put_res(data)
        

class ItemList(Resource):

    def get(self):
        list_of_items = InventoryListBL()
        return list_of_items.get_list_inventory()
