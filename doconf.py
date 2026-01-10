import os
from conf import Configs

def do_conf():
    Configs.username = os.environ.get("un")
    Configs.password = os.environ.get("PW")
    Configs.serverurl = "https://app.wallabag.it"
    Configs.client = os.environ.get("client")
    Configs.secret = os.environ.get("SECRET")
