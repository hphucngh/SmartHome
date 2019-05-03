import tornado.web
import json
import BaseHandler
from config import Env


class Home(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(
            self.current_user
        )
        result = Env.database.statusdb.aggregate(
            [
                {
                    "$group": {
                        "_id": "$name",
                        "status": {
                            "$last": "$status"
                        },
                    }
                }
            ]
        )
        finds = result.get("result")
        new_dict = {}
        for item in finds:
            name = item["_id"]
            status = item["status"]
            new_dict[name] = status

        #        lightLivingRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"light-living-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        lightKitchenRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"light-kitchen-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        lightBedRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"light-bed-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        lightFrontDoors = json.loads(dumps(Env.database["statusdb"].find({"name":"light-front-doors"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        lightBackDoors = json.loads(dumps(Env.database["statusdb"].find({"name":"light-back-doors"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        lightGarage = json.loads(dumps(Env.database["statusdb"].find({"name":"light-garage"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        clothesline = json.loads(dumps(Env.database["statusdb"].find({"name":"clothesline"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        waterTree = json.loads(dumps(Env.database["statusdb"].find({"name":"water-tree"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        frontDoors = json.loads(dumps(Env.database["statusdb"].find({"name":"front-doors"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #        garageDoors = json.loads(dumps(Env.database["statusdb"].find({"name":"garage-doors"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
        #
        #        data = {
        #                lightLivingRoom["name"]:lightLivingRoom["status"],
        #                lightKitchenRoom["name"]:lightKitchenRoom["status"],
        #                lightBedRoom["name"]:lightBedRoom["status"],
        #                lightFrontDoors["name"]:lightFrontDoors["status"],
        #                lightBackDoors["name"]:lightBackDoors["status"],
        #                lightGarage["name"]:lightGarage["status"],
        #                clothesline["name"]:clothesline["status"],
        #                waterTree["name"]:waterTree["status"],
        #                frontDoors["name"]:frontDoors["status"],
        #                garageDoors["name"]:garageDoors["status"],
        #                }
        # data = {"light-living-room":"off", "light-kitchen-room":"off", "light-bed-room":"off", "light-front-doors":"off", "light-back-doors":"off", "light-garage":"off"}
        data = json.dumps(new_dict)
        self.render("home.html", data=data)

