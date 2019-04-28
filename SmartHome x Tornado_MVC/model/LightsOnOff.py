import time
import datetime
import json
import RPi.GPIO as GPIO
import BaseHandler
from config import Env
from bson.json_util import dumps


class LightsOnOff(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        pinLightLivingRoom = 4
        pinLightKitchenRoom = 17
        pinLightBedRoom = 27

        pinLightFrontDoors = 22
        pinLightBackDoors = 5
        pinLightGarage = 6

        pinWaterTree = 9
        pinClothesline = 21

        pinFrontDoors = 11
        pinGarage = 10

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(pinLightLivingRoom, GPIO.OUT)
        GPIO.setup(pinLightKitchenRoom, GPIO.OUT)
        GPIO.setup(pinLightBedRoom, GPIO.OUT)

        GPIO.setup(pinLightFrontDoors, GPIO.OUT)
        GPIO.setup(pinLightBackDoors, GPIO.OUT)
        GPIO.setup(pinLightGarage, GPIO.OUT)

        GPIO.setup(pinFrontDoors, GPIO.OUT)
        GPIO.setup(pinGarage, GPIO.OUT)

        GPIO.setup(pinWaterTree, GPIO.OUT)
        GPIO.setup(pinClothesline, GPIO.OUT)
        ServoRain = GPIO.PWM(pinClothesline, 50)
        ServoFrontDoors = GPIO.PWM(pinFrontDoors, 50)
        ServoGarage = GPIO.PWM(pinGarage, 50)

        key = self.get_argument("key")
        status = self.get_argument("value")

        def writeOnLight(key, status, starttime, iddevice, data):
            new_status = {"name": key, "status": status, "data": data, "starttime": starttime, "endtime": None, "iddevice": iddevice}
            Env.database["statusdb"].insert(new_status)
        def writeOffLight(key, endtime, status):
            finds = json.loads(dumps(Env.database["statusdb"].find({"name": key}, {"status": 1, "_id": 0}).sort([("_id", -1)]).limit(1)))[0]
            f = finds["status"]
            Env.database["statusdb"].update({"name": key, "status": f}, {"$set": {"endtime": endtime, "status": status}})
        if key == "light-living-room":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinLightLivingRoom, GPIO.HIGH)
                iddevice = "lightLivingRoom"
                data = "on light"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinLightLivingRoom, GPIO.LOW)
                writeOffLight(key, endtime, status)

        elif key == "light-kitchen-room":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinLightKitchenRoom, GPIO.HIGH)
                iddevice = "lightKitchenRoom"
                data = "on light"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinLightKitchenRoom, GPIO.LOW)
                writeOffLight(key, endtime, status)

        elif key == "light-bed-room":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinLightBedRoom, GPIO.HIGH)
                iddevice = "lightBedRoom"
                data = "on light"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinLightBedRoom, GPIO.LOW)
                writeOffLight(key, endtime, status)

        elif key == "light-front-doors":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinLightFrontDoors, GPIO.HIGH)
                iddevice = "lightFrontDoors"
                data = "on light"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinLightFrontDoors, GPIO.LOW)
                writeOffLight(key, endtime, status)

        elif key == "light-back-doors":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinLightBackDoors, GPIO.HIGH)
                iddevice = "lightBackDoors"
                data = "on light"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinLightBackDoors, GPIO.LOW)
                writeOffLight(key, endtime, status)

        elif key == "light-garage":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinLightGarage, GPIO.HIGH)
                iddevice = "lightGarage"
                data = "on light"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinLightGarage, GPIO.LOW)
                writeOffLight(key, endtime, status)

        elif key == "clothesline":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                ServoRain.start(2.5)
                ServoRain.ChangeDutyCycle(11.5)
                time.sleep(1)
                GPIO.output(pinClothesline, False)
                ServoRain.ChangeDutyCycle(0)
                ServoRain.stop()
                iddevice = "clothesline"
                data = "on clothesline"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                ServoRain.start(11.5)
                ServoRain.ChangeDutyCycle(2.5)
                time.sleep(1)
                GPIO.output(pinClothesline, False)
                ServoRain.ChangeDutyCycle(0)
                ServoRain.stop()
                writeOffLight(key, endtime, status)

        elif key == "water-tree":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                GPIO.output(pinWaterTree, GPIO.LOW)
                iddevice = "waterTree"
                data = "on water tree"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                GPIO.output(pinWaterTree, GPIO.HIGH)
                writeOffLight(key, endtime, status)

        elif key == "front-doors":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                ServoFrontDoors.start(2.5)
                ServoFrontDoors.ChangeDutyCycle(7)
                time.sleep(1)
                GPIO.output(pinFrontDoors, False)
                ServoFrontDoors.ChangeDutyCycle(0)
                ServoFrontDoors.stop()
                iddevice = "frontDoors"
                data = "on front doors"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                ServoFrontDoors.start(7)
                ServoFrontDoors.ChangeDutyCycle(2.5)
                time.sleep(1)
                GPIO.output(pinFrontDoors, False)
                ServoFrontDoors.ChangeDutyCycle(0)
                ServoFrontDoors.stop()
                writeOffLight(key, endtime, status)

        elif key == "garage-doors":
            if status == "on":
                starttime = datetime.datetime.utcnow()
                ServoGarage.start(2.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(4.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(6.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(7.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(9)
                time.sleep(0.5)
                GPIO.output(pinGarage, False)
                ServoGarage.ChangeDutyCycle(0)
                ServoGarage.stop()
                iddevice = "garagedoors"
                data = "on garage doors"
                writeOnLight(key, status, starttime, iddevice, data)
            if status == "off":
                endtime = datetime.datetime.utcnow()
                ServoGarage.start(9)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(7.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(6.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(4.5)
                time.sleep(1)
                ServoGarage.ChangeDutyCycle(2.5)
                time.sleep(0.5)
                GPIO.output(pinGarage, False)
                ServoGarage.ChangeDutyCycle(0)
                ServoGarage.stop()
                writeOffLight(key, endtime, status)

        elif key == "all-on-interior":
            status = "on"
            # device la danh sach thiet bi, sau se nang cap bang cach truy xuat database
            device = ["light-living-room", "light-kitchen-room", "light-bed-room"]

            # Truy van database dong thoi chuyen thanh kieu list
            finds = json.loads(dumps(Env.database["statusdb"].find({"status": "on", "endtime": None}, {"name": 1, "_id": 0})))

            new_dict = {}
            new = []
            print str(finds)
            # Thuc hien chuyen finds thanh kieu dict
            for item in finds:
                name = item["name"]
                new_dict[name] = item
            print str(new_dict) + "  dict "
            # Lay cac ten thiet bi theo val ma trong val co them {'name': [ten thiet bi]} nen append vao mot list moi
            for key, val in new_dict.items():
                new.append(val["name"])

            statusDeviceOn = []
            # Neu trong list truy van trong truy van khong co thiet bi thi append ... cac thiet bi dang OFF
            for i in device:
                if i not in new:
                    statusDeviceOn.append(i)

            starttime = datetime.datetime.utcnow()
            data = "on all"
            for devicename in statusDeviceOn:
                if devicename == ("light-living-room"):
                    GPIO.output(pinLightLivingRoom, GPIO.HIGH)
                    iddevice = "lightLivingRoom"
                    writeOnLight(devicename, status, starttime, iddevice, data)
                elif devicename == ("light-kitchen-room"):
                    GPIO.output(pinLightKitchenRoom, GPIO.HIGH)
                    iddevice = "lightKitchenRoom"
                    writeOnLight(devicename, status, starttime, iddevice, data)
                elif devicename == ("light-bed-room"):
                    GPIO.output(pinLightBedRoom, GPIO.HIGH)
                    iddevice = "lightBedRoom"
                    writeOnLight(devicename, status, starttime, iddevice, data)

        elif key == "all-off-interior":
            status = "off"

            # device la danh sach thiet bi, sau se nang cap bang cach truy xuat database
            device = ["light-living-room", "light-kitchen-room", "light-bed-room"]

            # Truy van database dong thoi chuyen thanh kieu list
            finds = json.loads(dumps(Env.database["statusdb"].find({"status": status}, {"name": 1, "_id": 0})))

            new_dict = {}
            new = []

            # Thuc hien chuyen finds thanh kieu dict
            for item in finds:
                name = item["name"]
                new_dict[name] = item

            # Lay cac ten thiet bi theo val ma trong val co them {'name': [ten thiet bi]} nen append vao mot list moi
            for key, val in new_dict.items():
                new.append(val["name"])

            statusDeviceOn = []
            # Neu trong list truy van trong truy van khong co thiet bi thi append ... cac thiet bi dang OFF
            for i in device:
                if i not in new:
                    statusDeviceOn.append(i)

            endtime = datetime.datetime.utcnow()
            for devicename in new:
                if devicename == ("light-living-room"):
                    GPIO.output(pinLightLivingRoom, GPIO.LOW)
                    writeOffLight(devicename, endtime, status)

                elif devicename == ("light-kitchen-room"):
                    GPIO.output(pinLightKitchenRoom, GPIO.LOW)
                    writeOffLight(devicename, endtime, status)

                elif devicename == ("light-bed-room"):
                    GPIO.output(pinLightBedRoom, GPIO.LOW)
                    writeOffLight(devicename, endtime, status)

        elif key == "all-on-exterior":
            status = "on"
            # device la danh sach thiet bi, sau se nang cap bang cach truy xuat database
            device = ["light-front-doors", "light-back-doors", "light-garage"]

            # Truy van database dong thoi chuyen thanh kieu list
            finds = json.loads(dumps(Env.database["statusdb"].find({"status": status, "endtime": None}, {"name": 1, "_id": 0})))

            new_dict = {}
            new = []

            # Thuc hien chuyen finds thanh kieu dict
            for item in finds:
                name = item["name"]
                new_dict[name] = item

            # Lay cac ten thiet bi theo val ma trong val co them {'name': [ten thiet bi]} nen append vao mot list moi
            for key, val in new_dict.items():
                new.append(val["name"])

            statusDeviceOn = []
            # Neu trong list truy van trong truy van khong co thiet bi thi append ... cac thiet bi dang OFF
            for i in device:
                if i not in new:
                    statusDeviceOn.append(i)

            starttime = datetime.datetime.utcnow()
            data = "on all"
            for devicename in statusDeviceOn:
                if devicename == ("light-front-doors"):
                    GPIO.output(pinLightFrontDoors, GPIO.HIGH)
                    iddevice = "lightFrontDoors"
                    writeOnLight(devicename, status, starttime, iddevice, data)
                elif devicename == ("light-back-doors"):
                    GPIO.output(pinLightBackDoors, GPIO.HIGH)
                    iddevice = "lightBackDoors"
                    writeOnLight(devicename, status, starttime, iddevice, data)
                elif devicename == ("light-garage"):
                    GPIO.output(pinLightGarage, GPIO.HIGH)
                    iddevice = "lightGarage"
                    writeOnLight(devicename, status, starttime, iddevice, data)

        elif key == "all-off-exterior":
            status = "off"

            # device la danh sach thiet bi, sau se nang cap bang cach truy xuat database
            device = ["light-front-doors", "light-back-doors", "light-garage"]

            # Truy van database dong thoi chuyen thanh kieu list
            finds = json.loads(dumps(Env.database["statusdb"].find({"status": status}, {"name": 1, "_id": 0})))

            new_dict = {}
            new = []

            # Thuc hien chuyen finds thanh kieu dict
            for item in finds:
                name = item["name"]
                new_dict[name] = item

            # Lay cac ten thiet bi theo val ma trong val co them {'name': [ten thiet bi]} nen append vao mot list moi
            for key, val in new_dict.items():
                new.append(val["name"])

            statusDeviceOn = []
            # Neu trong list truy van trong truy van khong co thiet bi thi append ... cac thiet bi dang OFF
            for i in device:
                if i not in new:
                    statusDeviceOn.append(i)
            endtime = datetime.datetime.utcnow()
            for devicename in new:
                if devicename == ("light-front-doors"):
                    GPIO.output(pinLightFrontDoors, GPIO.LOW)
                    writeOffLight(devicename, endtime, status)

                elif devicename == ("light-back-doors"):
                    GPIO.output(pinLightBackDoors, GPIO.LOW)
                    writeOffLight(devicename, endtime, status)

                elif devicename == ("light-garage"):
                    GPIO.output(pinLightGarage, GPIO.LOW)
                    writeOffLight(devicename, endtime, status)

