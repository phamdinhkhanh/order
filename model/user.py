from mongoengine import *
import mlab


class User(Document):
    id_user = StringField()
    name = StringField()
    address = StringField()
    total_spend = FloatField()
    phone_number = StringField()
    oid = StringField()
    urlPic = StringField()
    urlFb = StringField()
    pass_word = StringField()
    foods_like = ListField(ReferenceField("Food"))
    token = StringField()
    def get_json(self):

        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "id_data": oid,
            "id_user": self.id_user,
            "name": self.name,
            "address": self.address,
            "total_spend": self.total_spend,
            "phone_number": self.phone_number,
            "urlPic":self.urlPic,
            "urlFb":self.urlFb,
            "pass_word":self.pass_word
        }

    def get_id(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {"_id": {
            "$oid": oid
        }}
