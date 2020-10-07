from flask_restful import Resource

from businesslogic.CategoriesBL import CategoriesBL, StoreListBL


class Store(Resource):
    def get(self, name):
        get_category = CategoriesBL(name=name)
        return get_category.get_res()

    def post(self, name):
        post_category = CategoriesBL(name=name)
        return post_category.post_res()

    def delete(self, name):
        delete_category = CategoriesBL(name=name)
        return delete_category.del_res()


class StoreList(Resource):
    def get(self):
        list_of_stores = StoreListBL()
        return list_of_stores.get_store_list()