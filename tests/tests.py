import unittest
from wallabaggins import entry


class TestEntry(unittest.TestCase):

    def test_entry_init(self):
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
