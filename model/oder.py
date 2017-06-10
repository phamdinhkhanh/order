from mongoengine import *
from model.food import Food
import mlab
from model.user import *


class SingleOrder(EmbeddedDocument):
    food = ReferenceField("Food")
    count = IntField()

    def get_json(self):
        return {
            "food": Food.objects().with_id(self.food.id).get_json(),
            "count": self.count
        }

class Oder(Document):
    items = ListField(EmbeddedDocumentField("SingleOrder"))
    date = StringField()
    address = StringField()
    phone_number = StringField()
    user = ReferenceField("User")
    is_Succues = BooleanField()
    spend=FloatField()
    ship_money=FloatField()
    code=StringField()
    code_price=FloatField()

    def get_json(self):
        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "id":oid,
            "items": [item.get_json() for item in self.items],
            "spend":self.spend,
            "date":self.date,
            "address": self.address,
            "phone_number": self.phone_number,
            "user": self.user.get_json(),
            "is_Succues": self.is_Succues,
            "ship_money":self.ship_money,
            "code":self.code,
            "code_price":self.code_price
        }

