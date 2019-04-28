import json
import Login
import BaseHandler
from config import Env
from bson.json_util import dumps


class Profile(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = Login.username
        data = dumps(Env.database["homedb"].find({"username": username}))
        data = json.loads(data)
        self.render("profile.html", data=data)
    def post(self):
        username = self.get_argument("user-name", "")
        password = self.get_argument("user-password", "")
        rows = Env.database["homedb"].find(
            {
                "username": username,
                "password": password
            }
        ).count()

        if rows != 0:
            self.redirect("/home")
        else:
            self.render("login.html")

