from pymongo import MongoClient

class Env:
    # DB_HOST = "localhost"
    # DB_NAME = "smarthome"
    # DB_USER = "root"
    # DB_PASSWORD = "hphuc"

    PORT = 8888
    con = MongoClient("localhost", 27017)
    database = con.smarthome
