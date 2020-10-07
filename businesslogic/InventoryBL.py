from datetime import datetime

from common.utils import conversion_image_into_bs64, is_expired_func, covert_time
from models.inventoryModel import InventoryModel


class InventoryBL:

    def __init__(self, inventory_name):
        self.inventory_name = inventory_name

    def get_res(self):
        item = InventoryModel.find_by_name(self.inventory_name)
        if item:
            json_data = is_expired_func(item.expiry_time)
            current_json = item.json()
            current_json["is_expired"] = json_data
            return current_json, 200
        return {"message": f"{self.inventory_name} -> This item is not available in Inventory System."}, 400

    def post_res(self, data):
        item = InventoryModel.find_by_name(self.inventory_name)

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

            item = InventoryModel(inventory_name=self.inventory_name,
                                  **data)
        try:
            item.save_to_db()
        except Exception as e:
            return {{"Exception": f"{e}"}}
        return item.json(), 201

    def del_res(self):

        item = InventoryModel.find_by_name(self.inventory_name)

        if item:

            try:
                item.delete_from_db()
            except Exception as e:
                return {"Exception": f'{e}'}
        else:
            return {"message": f'{self.inventory_name} -> This item is not stored in Inventory System.'}

        return {"message": f'{self.inventory_name} -> This item is deleted.'}, 201

    def put_res(self, data):
        item = InventoryModel.find_by_name(self.inventory_name)
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
            item = InventoryModel(self.inventory_name, **data)

        item.save_to_db()
        return item.json(), 200


class InventoryListBL:

    def get_list_inventory(self):
        items_list = list()
        for per_item in InventoryModel.query.all():
            current_item_json = per_item.json()
            if is_expired_func(per_item.expiry_time):  # True when it is expired
                current_item_json["is_expired"] = True
                items_list.append(current_item_json)
            else:
                current_item_json["is_expired"] = False
                items_list.append(current_item_json)
        return {'items': items_list}, 200
