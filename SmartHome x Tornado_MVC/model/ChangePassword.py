import tornado.web
import BaseHandler
import Login
from config import Env


class ChangePassword(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def post(self):
        password = self.get_argument("password")
        newpassword = self.get_argument("newpassword")
        confirmpassword = self.get_argument("confirmpassword")
        
        username = Login.username
        rows = Env.database["homedb"].find(
            {
                "username": username,
                "password": password
            }
        ).count()

        if rows != 0:
            Env.database["homedb"].update(
            {
                "username": username
            },
            {
                "$set": {
                    "password": newpassword
                }
            }
            )
        else:
            self.redirect("/profile")
            
            

        

        self.redirect("/profile")


