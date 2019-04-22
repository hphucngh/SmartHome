import tornado.web

class My404(tornado.web.RequestHandler):
    def get(self):
        self.render("404")

from .VersionHandler import VersionHandler
from .Login import Login
from .Home import Home
from .Lights import Lights
from .Profile import Profile
from .Climate import Climate
from .ProfileUpdatePersonal import ProfileUpdatePersonal
from .TemperatureHumidity import TemperatureHumidity
from .Reload import Reload
from .ReloadChart import ReloadChart
from .Automatic import Automatic
from .AutoFanLivingRoom import AutoFanLivingRoom
from .AutoLightKitchenRoom import AutoLightKitchenRoom
from .AutoHumidityLand import AutoHumidityLand
from .AutoClothesline import AutoClothesline
from .StreamCamera import StreamCamera
from .OnOffDevice import OnOffDevice
from .BaseHandler import BaseHandler
from .LightsOnOff import LightsOnOff

__all__ = {

    ("VersionHandler", "My404"),
    ("Login", "My404"),
    ("Home", "My404"),
    ("Lights", "My404"),
    ("Profile", "My404"),
    ("Climate", "My404"),
    ("ProfileUpdatePersonal", "Profile"),
    ("OnOffDevice", "My404"),
    ("TemperatureHumidity", "My404"),
    ("Reload", "My404"),
    ("ReloadChart", "My404"),
    ("Automatic", "My404"),
    ("AutoFanLivingRoom", "My404"),
    ("AutoLightKitchenRoom", "My404"),
    ("AutoHumidityLand", "My404"),
    ("AutoClothesline", "My404"),
    ("StreamCamera", "My404"),
    ("LightsOnOff", "My404")
}
