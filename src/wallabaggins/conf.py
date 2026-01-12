"""
Settings and configuration for wallabag-cli.
"""
import time
import re
import os
import sys



class Configs():  # pylint: disable=too-few-public-methods
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


def save():
    """
    Saves the config into a file.
    """
    return False


def load(filepath):
    """
    Loads the config to a string
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def handle_invalid_config():
    """
    Handle case where the config parse fails
    """
    print("Invalid config file.")
    sys.exit(1)


def do_conf(filepath):
    """
    Parse the contents of the config
    """
    r = re.compile(r"^([^=]+)=(.+)$")
    for line in load(filepath).splitlines():
        if not line:
            continue
        m = r.match(line)
        key, value = m.groups()
        if not hasattr(Configs, key):
            handle_invalid_config()
        setattr(Configs, key, value)
