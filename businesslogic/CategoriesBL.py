from models.categoriesM import StoreModel


class CategoriesBL:

    def __init__(self, name):
        self.name = name

    def get_res(self):
        store = StoreModel.find_by_name(self.name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post_res(self):
        if StoreModel.find_by_name(self.name):
            return {'message': "A store with name '{}' already exists.".format(self.name)}, 400

        store = StoreModel(self.name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def del_res(self):
        store = StoreModel.find_by_name(self.name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}, 200


class StoreListBL:
    def get_store_list(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
