from db import db


class InventoryModel(db.Model):
    __table_name__ = 'Inventory'

    id = db.Column(db.INTEGER, primary_key=True)
    inventory_name = db.Column(db.String(100))
    inventory_category = db.Column(db.String(100))
    inventory_image = db.Column(db.LargeBinary, nullable=True)
    quantity = db.Column(db.Integer)
    manufacturing_time = db.Column(db.Date)
    expiry_time = db.Column(db.Date)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, inventory_name, inventory_image, quantity, manufacturing_time, expiry_time, store_id):
        self.inventory_name = inventory_name
        self.inventory_image = inventory_image
        self.quantity = quantity
        self.manufacturing_time = manufacturing_time
        self.expiry_time = expiry_time
        self.store_id = store_id

    def json(self):
        return {"inventory_name": self.inventory_name,
                "inventory_image": str(self.inventory_image),
                "quantity": self.quantity,
                "manufacturing_time": str(self.manufacturing_time),
                "expiry_time": str(self.expiry_time),
                "store_id": self.store_id
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        # db.session.query(InventoryModel).filter(
        #     InventoryModel.inventory_name.ilike("W%")
        # ).delete(synchronize_session='fetch')
        db.session.commit()

    @classmethod
    def find_by_name(cls, inventory_name):
        return cls.query.filter_by(inventory_name=inventory_name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_image_file(self, absolute_path):
        # path: /home/utsav/Downloads/philosophy.png
        # from path it will get data and store into sqlite
        file = open(f"static/{absolute_path}")
        InventoryModel.inventory_image = file.read()
        try:
            InventoryModel.save_to_db()
        except Exception as e:
            return {"Exception": "Image File has not stored"}
