import database
import json

with open('config.json') as json_file:
    data = json.load(json_file)

password = data["password"]

def add_admin(password):
    test = database.check_username_exists('AdminUser')
    if not test:
        database.add_user("AdminUser",password)


add_admin(password)