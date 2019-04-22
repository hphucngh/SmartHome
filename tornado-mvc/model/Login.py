import tornado.web
from config import Env
import Home
from model import BaseHandler
username = None

class Login(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        user = self.get_argument("user-name", "")
        password = self.get_argument("user-password", "")
        rows = Env.database["homedb"].find({"username": user, "password": password}).count()
        if rows !=  0 :
            self.redirect("/home")
            global username
            username = user
            self.set_secure_cookie("user", username)
        else:
            self.render("login.html")
