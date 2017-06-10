from mongoengine import *
from model.food import Food
import mlab
from model.user import *


class RateFood(Document):
    food=ReferenceField("Food")
    users=ListField(ReferenceField("User"))


