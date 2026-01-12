"""
Settings and configuration for wallabag-cli.
"""
import time
import re
import os
import sys
from getpass import getpass
import secretstorage


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


def save_secret_to_keyring(label):
    """
    Save a secret into the keyring
    """
    with secretstorage.dbus_init() as dbus:
        collection = secretstorage.get_default_collection(dbus)
        attributes = {"application": "wallabaggins"}
        collection.create_item(label, attributes, getattr(Configs, label))


def load_secret_from_keyring(label):
    """
    Load a secret from the keyring
    """
    with secretstorage.dbus_init() as dbus:
        collection = secretstorage.get_default_collection(dbus)
        our_items = collection.search_items({"application": "wallabaggins"})
        for item in our_items:
            if label == item.get_label():
                setattr(Configs, label, item.get_secret())
                return


def load_missing_secrets_from_keyring():
    """
    Load any missing secrets from keyring
    """
    for attr in ["password", "secret"]:
        if not getattr(Configs, attr):
            load_secret_from_keyring(attr)


def load_missing_secrets_from_envvars():
    """
    Load any missing secrets from keyring
    """
    for attr in ["password", "secret"]:
        if not getattr(Configs, attr):
            varname = "WBGINS_" + attr.upper()
            val = os.environ.get(varname)
            setattr(Configs, attr, val)


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


def load_config_via_prompt(label, hidden=True):
    """
    Read a config item in via a text prompt
    """
    prompt = label + ": "
    if hidden:
        v = getpass(prompt=prompt)
    else:
        v = input(prompt)
    setattr(Configs, label, v)


def prompt_for_missing_configs():
    """
    Fill in the missing configs, using either Secret Service or prompts
    """
    user_config_items = [
        'serverurl',
        'username',
        'password',
        'client',
        'secret',
    ]
    prompted_secrets = []
    for attr in user_config_items:
        if not getattr(Configs, attr):
            if attr in ['password', 'secret']:
                load_config_via_prompt(attr, hidden=True)
                prompted_secrets.append(attr)
            else:
                load_config_via_prompt(attr, hidden=False)
    for attr in prompted_secrets:
        res = input(f"Save {attr} to keyring? (Y/n)")
        if res in ["Y", "y", "yes", "Yes", "YES", ""]:
            save_secret_to_keyring(attr)


def do_conf(filepath=DEFAULT_CONFIG_PATH, skip_keyring=False):
    """
    Get the config from wherever
    """
    config_from_file(filepath)
    load_missing_secrets_from_envvars()
    if not skip_keyring:
        load_missing_secrets_from_keyring()
    prompt_for_missing_configs()
