import tornado.web
from config import Env
import time
import BaseHandler

class ProfileUpdatePersonal(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):

        firstname = self.get_argument("firstname")
        lastname = self.get_argument("lastname")
        email = self.get_argument("email")
        phone = self.get_argument("phone")

        datapersonal = {"firstname": firstname, "lastname": lastname, "email": email, "phone": phone}
        username = "hphuc"

        Env.database["homedb"].update({"username": username}, {"$set": {"firstname": firstname, "lastname": lastname, "email": email, "phone": phone}})

        self.redirect("/profile")

