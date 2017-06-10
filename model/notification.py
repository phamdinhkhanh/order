from mongoengine import *
import mlab


class Notification(Document):
    message_title = StringField()
    message_body = StringField()
    datetime = StringField()

    def get_json(self):
        return mlab.item2json(self)
