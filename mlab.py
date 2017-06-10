import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds133290.mlab.com:33290/amita
# host = "ds133290.mlab.com"
# port = 33290
# db_name = "amita"
# username = "1"
# password = "1"


# mongodb://<dbuser>:<dbpassword>@ds155080.mlab.com:55080/shiptest
# host = "@ds155080.mlab.com"
# port = 55080
# db_name = "shiptest"
# username = "1"
# password = "1"
# mongodb://<dbuser>:<dbpassword>@ds119302.mlab.com:19302/order

host = "ds119302.mlab.com"
port = 19302
db_name = "order"
username = "khanh"
password = "khanh"

def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)


def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())