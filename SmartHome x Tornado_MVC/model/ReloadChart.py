import tornado.web
from config import Env
from bson.json_util import dumps
import json
from datetime import datetime
import BaseHandler

class ReloadChart(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        chartBedRoom = json.loads(dumps(Env.database["statusdb"].find({"name": "temperature-humidity-bedroom"}, {"temperature": 1, "humidity": 1, "time": 1, "_id": 0}).sort([("_id", -1)]).limit(10)))

        chartTemperature = []
        chartHumidity = []
        chartDateTime = []

        for arrayTemperature in chartBedRoom:
            chartTemperature.append(arrayTemperature["temperature"])

        for arrayHumidity in chartBedRoom:
            chartHumidity.append(arrayHumidity["humidity"])

        for arrayDateTime in chartBedRoom:
            dateTime = datetime.utcfromtimestamp(arrayDateTime["time"]["$date"] / 1000.0)
            hour = dateTime.strftime("%H:%M:%S")
            chartDateTime.append(hour)

        chart = {"chart": {"labels": chartDateTime, "series": [chartHumidity, chartTemperature]}}
        data = json.dumps(chart)
        self.write(data)

