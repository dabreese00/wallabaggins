"""
Settings and configuration for wallabag-cli.
"""
import base64
import json
import time
import re
from collections import OrderedDict
# from Crypto.Cipher import AES
# from Crypto.Hash import MD5
import getpass
import math
import os
from pathlib import Path
import socket
from sys import exit

CONFIG_DIRECTORY = os.path.expanduser("~")
CONFIG_FILENAME = ".wallabaggins.conf"
RE_CONFIGLINE = r"^([^=]+)=(.+)$"
ALLOWED_KEYS = [
    "serverurl",
    "username",
    "password",
    "client",
    "secret"
]


__global_custom_path = None


class Configs():
    """
    Static struct for storing the global configs.
    """

    # wallabag server
    serverurl = ""
    username = ""
    password = ""

    # wallabag api oauth2
    client = ""
    secret = ""

    # oauth2 token
    access_token = ""
    expires = 0


def is_token_expired():
    """
    Returns if the last created oauth2 token is expired.
    """
    if os.environ.get("WB_DEBUG"):
        print("token is expired")
    return Configs.expires - time.time() < 0


def save(custom_path=None):
    """
    Saves the config into a file.
    """
    return False


def load(filepath):
    """
    Loads the config into a dictionary.
    """
    d = {}
    r = re.compile(RE_CONFIGLINE)
    with open(filepath, 'r') as f:
        for line in f:
            m = r.match(line)
            key, value = m.groups()
            if not key in ALLOWED_KEYS:
                handle_invalid_config()
            d[key] = value
    return d


def handle_invalid_config():
    print("Invalid config file.")
    exit(1)


def do_conf(filepath):
    for k, v in load(filepath).items():
        setattr(Configs, k, v)
