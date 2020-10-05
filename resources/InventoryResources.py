import json
from datetime import date, datetime

from flask_restful import Resource, reqparse
from models.inventoryModel import InventoryModel
from Time_coversion import covert_time, is_expired_func
from Image_conversion import conversion_image_into_bs64

from flask_jwt import jwt_required


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

    # @jwt_required()
    def get(self, inventory_name):
        item = InventoryModel.find_by_name(inventory_name)
        if item:
            json_data = is_expired_func(item.expiry_time)
            current_json = item.json()
            current_json["is_expired"] = json_data
            return current_json, 200
        return {"message": f"{inventory_name} -> This item is not available in Inventory System."}, 400

    def post(self, inventory_name):
        data = InventoryResource.parse.parse_args()
        item = InventoryModel.find_by_name(inventory_name)

        if item:
            # Add item one more in inventory
            item.quantity = int(item.quantity) + 1

        else:
            # create Item in inventory

            # Time change function call
            date_data = covert_time(data["manufacturing_time"], data["expiry_time"])
            manufacturing_time_into_date, expiry_time_into_date = date_data
            data["manufacturing_time"] = manufacturing_time_into_date
            data["expiry_time"] = expiry_time_into_date

            # Image Conversion function call
            string_of_image = conversion_image_into_bs64(file_location=str(data["inventory_image"]))
            data["inventory_image"] = string_of_image

            item = InventoryModel(inventory_name=inventory_name,
                                  **data)
        try:
            item.save_to_db()
        except Exception as e:
            return {{"Exception": f"{e}"}}
        return item.json(), 201

    def delete(self, inventory_name):
        item = InventoryModel.find_by_name(inventory_name)
        if item:

            try:
                item.delete_from_db()
            except Exception as e:
                return {"Exception": f'{e}'}
        else:
            return {"message": f'{inventory_name} -> This item is not stored in Inventory System.'}

        return {"message": f'{inventory_name} -> This item is deleted.'}, 201

    def put(self, inventory_name):

        # InventoryModel.query.filter_by_id(inventory_id = 1).first()
        # here It can be delete and update

        data = InventoryResource.parse.parse_args()
        item = InventoryModel.find_by_name(inventory_name)
        if item:

            print("Image vlue", data.get('inventory_image', None), ">>>>>>>>>>>>>>>>>>>>>")
            print("Image vlue", data.get("quantity", None), ">>>>>>>>>>>>>>>>>>>>>")
            if data.get('inventory_image', None):
                string_of_image = conversion_image_into_bs64(file_location=str(data["inventory_image"]))
                item.inventory_image = string_of_image
            if data.get('quantity', None):
                item.quantity = data['quantity']
            if data.get('manufacturing_time', None):
                item.manufacturing_time = datetime.strptime(data['manufacturing_time'], "%Y/%m/%d").date()
            if data.get('expiry_time', None):
                item.expiry_time = datetime.strptime(data['expiry_time'], "%Y/%m/%d").date()

        else:
            item = InventoryModel(inventory_name, **data)

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    # def get(self):
    #     return {'items': list(map(lambda x: x.json() , InventoryModel.query.all()))}, 200

    def get(self):
        items_list = list()
        for per_item in InventoryModel.query.all():
            current_item_json = per_item.json()
            if is_expired_func(per_item.expiry_time):  # True when it is expired
                current_item_json["is_expired"] = "true"
                items_list.append(current_item_json)
            else:
                current_item_json["is_expired"] = "false"
                items_list.append(current_item_json)
        return {'items': items_list}
