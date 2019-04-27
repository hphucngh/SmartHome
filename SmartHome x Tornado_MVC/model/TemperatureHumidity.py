import tornado.web
from config import Env #
import time
import datetime
from bson.json_util import dumps
import json
import RPi.GPIO as GPIO
import Adafruit_DHT
import BaseHandler

class TemperatureHumidity(BaseHandler.BaseHandler):
    @tornado.web.authenticated

# Adafruit_DHT ho tro nhieu loai cam bien DHT, o day dung DHT11 nen chon cam bien  DHT11
	def get(self):
		chon_cam_bien = Adafruit_DHT.DHT11

		GPIO.setmode(GPIO.BCM)

# chan DATA duoc noi vao chan GPIO25 cua PI
		pin_sensor = 25

		print ("RASPI.VN Demo cam bien do am DHT 11");
		try:
			while(1):
				do_am, nhiet_do = Adafruit_DHT.read_retry(chon_cam_bien, pin_sensor)
				if do_am is not None and nhiet_do is not None:
					print ("NNhiet Do = {0:0.1f}  Do Am = {1:0.1f}\n")
					print ("RASPI.VN cho 2 giay de tiep tuc do ...\n")
					time.sleep(2)
				else:
					print("Loi khong the doc tu cam bien DHT11 :(\n")
		except KeyboardInterrupt:
			GPIO.cleanup() 