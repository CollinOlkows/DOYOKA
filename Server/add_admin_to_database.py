import database
import json

with open('config.json') as json_file:
    data = json.load(json_file)

password = data["password"]
username = data["admin_username"]

def add_admin(password):
    test = database.check_username_exists(username)
    if not test:
        database.add_user(username,password)


add_admin(password)