import tornado.web
from config import Env
from bson.json_util import dumps
import json

class Automatic(tornado.web.RequestHandler):
	def get(self):
		autoFanLivingRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"auto-fan-living-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
		autoLightKitchenRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"auto-light-kitchen-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]	
		autoClothesline = json.loads(dumps(Env.database["statusdb"].find({"name":"auto-clothesline"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
                autoHumidityLand = json.loads(dumps(Env.database["statusdb"].find({"name":"auto-humidity-land"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]	
		data = {autoFanLivingRoom['name']:autoFanLivingRoom['status'], autoLightKitchenRoom['name']:autoLightKitchenRoom['status'], autoClothesline['name']:autoClothesline['status'], autoHumidityLand['name']:autoHumidityLand['status']}
		#data = {"auto-fan-living-room": "off", "auto-light-kitchen-room":"off", "auto-clothesline": "off", "auto-humidity-land":"off"}
		data = json.dumps(data)
		self.render("automatic.html", data=data)
