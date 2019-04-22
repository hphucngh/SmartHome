import tornado.web
from config import Env
from bson.json_util import dumps
import json
from datetime import datetime

class Reload(tornado.web.RequestHandler):
	def get(self):	
		thBedRoom = json.loads(dumps(Env.database["statusdb"].find({"name":"temperature-humidity-bedroom"},{"_id":0}).sort([("_id", -1)]).limit(1)))[0]			
		data = {
				"temperature": thBedRoom['temperature'],
				"humidity": thBedRoom['humidity']
				}
		data = json.dumps(data)
		self.write( data)
