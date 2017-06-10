from flask_restful import Resource, reqparse
import mlab
from model.user import User
from mongoengine import *
from model.food import *
from model.oder import  *

from flask import request


# class UserRegister(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument(name="id", type=str, location="json")
#         parser.add_argument(name="name", type = str, location = "json")
#         parser.add_argument(name="password", type = str, location = "json")
#
#         body = parser.parse_args()
#         id_user = body.id
#         name = body.name
#         password = body.password
#         old_user = User.objects(id_user=id_user).first()
#         if old_user is not None:
#             return old_user.get_id(), 202
#         user = User(id_user=id_user,name = name, password = password, total_spend=0)
#         user.save()
#         add_user = User.objects().with_id(user.id)
#         return add_user.get_id(), 200


class UserUpdate(Resource):
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="address", type=str, location="json")
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="phone_number", type=str, location="json")
        parser.add_argument(name="urlPic",type=str,location="json")
        parser.add_argument(name="urlFb",type=str,location="json")
        parser.add_argument(name="pass_word",type=str,location="json")
        body = parser.parse_args()
        address = body.address
        name = body.name
        phone_number = body.phone_number
        urlPic = body.urlPic
        urlFb = body.urlFb
        pass_word = body.pass_word
        user = User.objects().with_id(id);
        user.update(address=address, name=name, phone_number=phone_number,urlPic = urlPic,urlFb =urlFb,pass_word = pass_word)
        edit_user = User.objects().with_id(id)
        return mlab.item2json(edit_user), 200

    def get(self, id):
        user = User.objects().with_id(id)
        return mlab.item2json(user), 200

class UserFoodLike(Resource):
    def post(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body=parser.parse_args()
        id_food=body["id"]
        food=Food.objects().with_id(id_food)
        user=User.objects.with_id(id)
        foods=list(user.foods_like)
        for fo in foods:
            if fo==food:
                return {"message":"có rồi add cc đm"},401
        foods.append(food)
        user.update(set__foods_like=foods)
        return {"message":"ok"},200
    def get(self,id):
        user=User.objects().with_id(id)
        return [food.get_json() for food in user.foods_like]
    def delete(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body=parser.parse_args()
        id_food=body.id
        food=Food.objects().with_id(id_food)
        user=User.objects().with_id(id)
        foods=list(user.foods_like)
        foods.remove(food)
        user.update(set__foods_like=foods)
        return {"message":"ok"},200

class UserOrderVerify(Resource):
    def get(self,id):
        user=User.objects().with_id(id)
        orders=Oder.objects(user=user,is_Succues=False)
        return [order.get_json() for order in orders], 200

class UserOrderSuccess(Resource):
    def get(self,id):
        user=User.objects().with_id(id)
        orders=Oder.objects(user=user,is_Succues=True)
        return [order.get_json() for order in orders], 200

class UserSpend(Resource):
    def get(self,id):
        user=User.objects().with_id(id)
        return {"total_spend":str(user.total_spend)}


