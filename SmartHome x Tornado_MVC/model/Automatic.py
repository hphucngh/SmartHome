import tornado.web
from config import Env
from bson.json_util import dumps
import json
import BaseHandler


class Automatic(BaseHandler.BaseHandler):
    @tornado.web.authenticated

    def get(self):
        result = Env.database.statusdb.aggregate(
            [
                {"$group": {"_id": "$name", "status": {"$last": "$status"}}}
            ]
        )
        finds = (result.get("result"))
        new_dict = {}

        for item in finds:
            name = item['_id']
            status = item['status']
            new_dict[name] = status
        # autoFanLivingRoom = json.loads(dumps(
        #     Env.database["statusdb"].find({"name": "auto-fan-living-room"}, {"name": 1, "status": 1, "_id": 0}).sort(
        #         [("_id", -1)]).limit(1)))[0]
        # autoLightKitchenRoom = json.loads(dumps(
        #     Env.database["statusdb"].find({"name": "auto-light-kitchen-room"}, {"name": 1, "status": 1, "_id": 0}).sort(
        #         [("_id", -1)]).limit(1)))[0]
        # autoClothesline = json.loads(dumps(
        #     Env.database["statusdb"].find({"name": "auto-clothesline"}, {"name": 1, "status": 1, "_id": 0}).sort(
        #         [("_id", -1)]).limit(1)))[0]
        # autoHumidityLand = json.loads(dumps(
        #     Env.database["statusdb"].find({"name": "auto-humidity-land"}, {"name": 1, "status": 1, "_id": 0}).sort(
        #         [("_id", -1)]).limit(1)))[0]
        # data = {autoFanLivingRoom['name']: autoFanLivingRoom['status'],
        #         autoLightKitchenRoom['name']: autoLightKitchenRoom['status'],
        #         autoClothesline['name']: autoClothesline['status'],
        #         autoHumidityLand['name']: autoHumidityLand['status']}
        # data = {"auto-fan-living-room": "off", "auto-light-kitchen-room":"off", "auto-clothesline": "off", "auto-humidity-land":"off"}
        data = json.dumps(new_dict)
        self.render("automatic.html", data=data)
