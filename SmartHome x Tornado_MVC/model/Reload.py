import json
import BaseHandler
from config import Env
from bson.json_util import dumps


class Reload(BaseHandler.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thBedRoom = json.loads(
            dumps(
                Env.database["statusdb"]
                    .find(
                    {
                        "name": "temperature-humidity-bedroom"
                    },
                    {
                        "_id": 0
                    }
                )
                .sort([("_id", -1)])
                .limit(1)
            )
        )[0]
        data = {
            "temperature": thBedRoom["temperature"],
            "humidity": thBedRoom["humidity"]
        }
        data = json.dumps(data)
        self.write(data)

