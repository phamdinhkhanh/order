from mongoengine import Document, StringField
from flask_restful import Resource, reqparse
import mlab
from model.food import *
from model.user import *
from model.rate import *


class FoodRes(Resource):
    def get(self):
        food = Food.objects()
        return mlab.list2json(food), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="url", type=str, location="json")
        parser.add_argument(name="coint_old", type=str, location="json")
        parser.add_argument(name="coint_new", type=str, location="json")
        body = parser.parse_args()
        name = body.name
        url = body.url
        coint_old = body.coint_old
        coint_new = body.coint_new
        try:
            old = float(coint_old)
            new = float(coint_new)
        except:
            return {"message": "post cái lol gì? giá là số ok? bỏ chữ Đ hay VND đi"}, 401
        cout_rate = 0
        rate = 5
        if name is None or url is None or coint_new is None or coint_old is None:
            return {"message": "Gửi cc thiếu trường đcm"}, 401
        food = Food(name=name, url=url, coint_new=coint_new, coint_old=coint_old, cout_rate=cout_rate, rate=rate)
        food.save()
        add_food = Food.objects().with_id(food.id)
        return mlab.item2json(add_food), 200


class FoodRate(Resource):
    def put(self, id):
        food=Food.objects().with_id(id)
        parser = reqparse.RequestParser()
        parser.add_argument(name="rate", type=float, location="json")
        parser.add_argument(name="id_user", type=str, location="json")
        body = parser.parse_args()
        id_user=body["id_user"]
        rate_request = float(body["rate"])
        ratefood=RateFood.objects(food=food)
        user=User.objects.with_id(id_user)
        if(RateFood(ratefood)["users"] is None):
            arr_user=[]
            arr_user.append(user)
            ratefood=RateFood(users=arr_user,food=food)
            ratefood.save()
            return {"message":"Đã rate"}
        else:
            arr_user=ratefood["users"]
        if user in arr_user:
            return {"message":"đã rate món này rồi"},401

        if rate_request < 0 or rate_request > 5:
            return {"message": "rate từ 0 đến 5 sao, đm óc chó à???"}, 401
        try:
            food = Food.objects().with_id(id)
        except:
            return {"message": "Đánh giá cái lol gì food k tồn tại?? gửi id trong mlab lưu!"}, 401
        cout_rate = food["cout_rate"]
        rate = food["rate"]
        rates = (float(rate) * int(cout_rate)) + float(rate_request)
        rate = rates / (int(cout_rate) + 1)
        food.update(set__rate=rate, set__cout_rate=cout_rate + 1)
        food = Food.objects().with_id(id)
        list(arr_user).append(user)
        if(ratefood is None):
            ratefood=RateFood(food=food,users=arr_user)
            ratefood.save()
        else:
            ratefood.update(set__users =arr_user)
        return mlab.item2json(food), 200


class FoodGetHotSales(Resource):
    def get(self):
        listFood = []
        foods = Food.objects()
        for food in foods:
            if (float(food.coint_old) - float(food.coint_new)) > 0:
                listFood.append(food)

        return [foo.get_json() for foo in listFood]


class FoodFavorite(Resource):
    def get(self):
        foods = Food.objects(is_favorite=True)
        return [food.get_json() for food in foods]


class FoodLike(Resource):
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body = parser.parse_args()
        id_food = body["id"]
        food = Food.objects().with_id(id_food)
        user = User.objects.with_id(id)
        foods = list(user.foods_like)
        for fo in foods:
            if fo == food:
                return {"message": "có rồi add cc đm"}, 401
        return {"message": "ok"}, 200

class FoodInfoRes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        parser.add_argument(name="info", type=str, location="json")
        body=parser.parse_args()

        id=body["id"]
        info=body["info"]

        food=Food.objects.with_id(id)
        food_infor=FoodInfo(food=food, info=info)
        return food_infor.get_json()


class FoodInfoGetRes(Resource):
    def get(self,id):
        foodInfor=FoodInfo.objects().with_id(id)
        return foodInfor.get_json()

class GetCover(Resource):
    def get(self):
        return {"url":"http://res.cloudinary.com/dumfykuvl/image/upload/v1491386363/sen_ysaxgl.jpg"}
