import unittest
from . import manager

class testNotionManager(unittest.TestCase):
    def test_search(self):
        ans = manager.search_homework('127340000000303128')
        self.assertTrue(ans, "This homework is already on Notion")
        
        ans = manager.search_homework('This is not on Notion')
        self.assertFalse(ans, "This is not on Notion")
        