"""
Settings and configuration for wallabag-cli.
"""
import time
import re
import os
import sys
from getpass import getpass


DEFAULT_CONFIG_PATH = os.environ.get("HOME") + "/.wallabaggins.conf"


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


def config_from_file(filepath):
    """
    Parse the contents of the config
    """
    r = re.compile(r"^([^=]+)=(.+)$")
    try:
        lines = load(filepath).splitlines()
    except FileNotFoundError:
        print("Could not find config file.")
        lines = ""
    for line in lines:
        if not line:
            continue
        m = r.match(line)
        key, value = m.groups()
        if not hasattr(Configs, key):
            handle_invalid_config()
        setattr(Configs, key, value)


def prompt_for_missing_configs():
    """
    Prompt the user for missing config items they might know
    """
    user_config_items = [
        'serverurl',
        'username',
        'password',
        'client',
        'secret'
    ]
    for attr in user_config_items:
        if not getattr(Configs, attr):
            v = getpass(prompt=attr+": ")
            setattr(Configs, attr, v)


def do_conf(filepath=DEFAULT_CONFIG_PATH):
    """
    Get the config from wherever
    """
    config_from_file(filepath)
    prompt_for_missing_configs()
