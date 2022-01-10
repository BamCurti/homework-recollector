import unittest
import homework_recollector

class TestHC(unittest.TestCase):
    def test_uploading_pages(self):
        res = homework_recollector.fetch_homework()
        self.assertFalse(res, "The Homework is already uploaded")

if __name__ == '__main__':
    unittest.main()