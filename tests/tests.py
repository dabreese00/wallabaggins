import unittest
from unittest.mock import patch
from argparse import Namespace
from wallabaggins import entry
from wallabaggins import cli
from wallabaggins import api
from wallabaggins import conf


class TestEntry(unittest.TestCase):
    """
    Tests for Entry object
    """

    def test_entry_init(self):
        """
        Test creating a basic Entry
        """
        d = {
            'id': '1',
            'title': 'Big Article',
            'content': 'Big but not long',
            'url': 'https://example.com/',
            'is_archived': 0,
            'is_starred': 0,
        }
        e = entry.Entry(d)
        self.assertEqual(e.entry_id, '1')
        self.assertEqual(e.title, 'Big Article')
        self.assertEqual(e.content, 'Big but not long')


class TestCli(unittest.TestCase):
    """
    Tests for CLI module
    """

    @patch("wallabaggins.api.__request_get")
    @patch("wallabaggins.api.__request_post")
    def test_add_success(self, __request_post, __request_get):
        """
        Test using CLI to add an entry
        """
        __request_post.return_value = api.Response(200, "")
        __request_get.return_value = api.Response(
            200,
            '{"access_token": "ZGJmNTA2MDdmYTdmNWFiZjcxOWY3MWYyYzkyZDdlNWIzOTU4NWY3NTU1MDFjOTdhMTk2MGI3YjY1ZmI2NzM5MA","expires_in": 3600,"refresh_token": "OTNlZGE5OTJjNWQwYzc2NDI5ZGE5MDg3ZTNjNmNkYTY0ZWZhZDVhNDBkZTc1ZTNiMmQ0MjQ0OThlNTFjNTQyMQ","scope": null,"token_type": "bearer"}'
        )

        args = Namespace()
        args.verbose = False
        args.url = "https://example.com/some_article"

        cli.handle_add(args)

        __request_post.assert_called()
        __request_get.assert_called()

    @patch("wallabaggins.api.api_token")
    @patch("wallabaggins.api.__request_get")
    def test_list_success(self, __request_get, api_token):
        """
        Test using CLI to list entries
        """
        __request_get.return_value = api.Response(200, '''
{"_embedded": {"items": [{"is_archived": 0, "is_starred": 1, "id": 32402211, "title": "Queer Folks Mobilize for Palestine", "content": "testing 1", "url": "https://example.com/article1"}, {"is_archived": 1, "is_starred": 0, "id": 32402086, "title": "A progressive researcher said a conservative pundit twice her age tweeted out her Tinder profile. The replies were 'gross' but she turned it into a 'visual aid' on online harassment.", "content": "testing 2", "url": "https://example.com/article2"}, {"is_archived": 1, "is_starred": 0, "id": 32402015, "title": "Hill liberals push for shutdown clash over ICE funding but face resistance in Democratic ranks | CNN Politics", "content": "testing 3", "url": "https://example.com/article3"}]}}
''')
        api_token.return_value = api.Response(200, '''
{"access_token": "ZGJmNTA2MDdmYTdmNWFiZjcxOWY3MWYyYzkyZDdlNWIzOTU4NWY3NTU1MDFjOTdhMTk2MGI3YjY1ZmI2NzM5MA","expires_in": 3600,"refresh_token": "OTNlZGE5OTJjNWQwYzc2NDI5ZGE5MDg3ZTNjNmNkYTY0ZWZhZDVhNDBkZTc1ZTNiMmQ0MjQ0OThlNTFjNTQyMQ","scope": null,"token_type": "bearer"}''')

        args = Namespace()
        args.verbose = False
        args.count = 3

        cli.handle_list(args)

        __request_get.assert_called()

    @patch("wallabaggins.api.api_token")
    @patch("wallabaggins.api.__request_get")
    def test_show_success(self, __request_get, api_token):
        """
        Test using CLI to show an entry details
        """
        __request_get.return_value = api.Response(200, '''
{"is_archived": 0,"is_starred": 1,"id": 32402211,"title": "Queer Folks Mobilize for Palestine","content": "testing 1","url": "https://example.com/article1"}
''')
        api_token.return_value = api.Response(200, '''
{"access_token": "ZGJmNTA2MDdmYTdmNWFiZjcxOWY3MWYyYzkyZDdlNWIzOTU4NWY3NTU1MDFjOTdhMTk2MGI3YjY1ZmI2NzM5MA","expires_in": 3600,"refresh_token": "OTNlZGE5OTJjNWQwYzc2NDI5ZGE5MDg3ZTNjNmNkYTY0ZWZhZDVhNDBkZTc1ZTNiMmQ0MjQ0OThlNTFjNTQyMQ","scope": null,"token_type": "bearer"}''')

        args = Namespace()
        args.verbose = False
        args.entry_id = 0

        cli.handle_show(args)


class TestConf(unittest.TestCase):
    """
    Tests for the conf module
    """

    @patch("wallabaggins.conf.load")
    def test_do_conf(self, load):
        """
        Test the do_conf method
        """
        load.return_value = '''
serverurl=https://example.com
username=myuser
password=abc123
client=14331
secret=asfsdfsd
'''
        conf.do_conf("/home/wallabaggins/.conf")

        self.assertEqual(conf.Configs.serverurl, "https://example.com")
        self.assertEqual(conf.Configs.username, "myuser")
        self.assertEqual(conf.Configs.password, "abc123")
        self.assertEqual(conf.Configs.client, "14331")
        self.assertEqual(conf.Configs.secret, "asfsdfsd")
