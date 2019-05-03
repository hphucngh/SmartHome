import tornado.web
import BaseHandler
import Login
from config import Env


class ProfileUpdatePersonal(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        firstname = self.get_argument("firstname")
        lastname = self.get_argument("lastname")
        email = self.get_argument("email")
        phone = self.get_argument("phone")
        stateregion = self.get_argument("state/region")
        country = self.get_argument("country")
        zippostal = self.get_argument("zip/postal")
        citytown = self.get_argument("city/town")
        phone = self.get_argument("phone")
        street = self.get_argument("street")

        username = Login.username

        Env.database["homedb"].update(
            {
                "username": username
            },
            {
                "$set": {
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "phone": phone,
                    "state/region": stateregion,
                    "country": country,
                    "zip/postal": zippostal,
                    "city/town": citytown,
                    "phone": phone,
                    "street": street
                }
            }
        )

        self.redirect("/profile")

