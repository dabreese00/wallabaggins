import os
import re
from conf import Configs

RE_CONFIGLINE = r"^([^=]+)=(.+)$"
CONFIG_FILENAME = ".wallabaggins.conf"
ALLOWED_KEYS = [
    "serverurl",
    "username",
    "password",
    "client",
    "secret"
]

def handle_invalid_config():
    print("Invalid config file.")
    exit(1)

def load_conf(filename):
    r = re.compile(RE_CONFIGLINE)
    with open(filename, 'r') as f:
        for line in f:
            m = r.match(line)
            key, value = m.groups()
            if not key in ALLOWED_KEYS:
                handle_invalid_config()
            setattr(Configs, key, value)

def do_conf():
    load_conf(CONFIG_FILENAME)
