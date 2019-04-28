import BaseHandler
from config import Env

username = None


class Login(BaseHandler.BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        user = self.get_argument("user-name", "")
        password = self.get_argument("user-password", "")
        rows = Env.database["homedb"].find(
            {
                "username": user,
                "password": password
            }
        ).count()

        if rows != 0:
            self.set_secure_cookie("user", self.get_argument("user-name", ""))
            self.redirect("/home")
            global username
            username = user
        else:
            self.render("login.html")
