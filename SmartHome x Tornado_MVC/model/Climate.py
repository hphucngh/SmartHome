import tornado.web
from config import Env
from bson.json_util import dumps
import json
import BaseHandler

class Climate(BaseHandler.BaseHandler):
    @tornado.web.authenticated

	def get(self):

		fanLivingRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"fan-living-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]
		fanBedRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"fan-bed-room"},{"name":1, "status":1, "_id":0}).sort([("_id", -1)]).limit(1)))[0]	
		thBedRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"temperature-humidity-bedroom"},{"_id":0}).sort([("_id", -1)]).limit(1)))[0]

		data = {
				fanLivingRoom['name']:fanLivingRoom['status'], 
				fanBedRoom['name']:fanBedRoom['status'],
				"temperature-humidity-bedroom": "off", 
				"temperature-humidity":{
										"temperature": thBedRoom['temperature'],
										"humidity": thBedRoom['humidity']
										}
				}
		data = json.dumps(data)

		self.render("climate.html", data=data)
