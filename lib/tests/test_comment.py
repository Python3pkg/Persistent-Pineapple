#!/usr/bin/env python

__author__ = "Timothy McFadden"
__copyright__ = "Copyright 2014"
__credits__ = ["Timothy McFadden", "Jason Unrein"]
__license__ = "GPL"
__version__ = "0.0.0.2"  # file version
__maintainer__ = "Jason Unrein"
__email__ = "JasonAUnrein@gmail.com"
__status__ = "Development"

# Imports #####################################################################
import re
import sys
import unittest
from os import path, unlink
from persistent_pineapple._json import CommentedJSON


if sys.version_info[0] == 3:
    basestring = str


###############################################################################
class CommentTest(unittest.TestCase):
    test_path = path.dirname(path.realpath(__file__))
    test_file = "test1.json"
    fqtest = path.join(test_path, test_file)
    fqlist = path.join(test_path, "list.json")
    fqcomment = path.join(test_path, "test-comment.json")

    @classmethod
    def tearDownClass(cls):
        if path.isfile(CommentTest.fqcomment):
            unlink(CommentTest.fqcomment)

    def test_load(self):
        CommentedJSON().load(path=CommentTest.fqtest)

    def test_string(self):
        obj = CommentedJSON()
        data = obj.load(path=CommentTest.fqtest)
        result = obj.as_string(data)

        self.assertIsInstance(result, basestring)

        with open(self.fqtest, 'rb') as fh:
            lines = list(fh)[:2]

        lines = [x.strip() for x in lines]
        header = result.split("\n")[:2]

        if sys.version_info[0] == 3:
            header = list(map(lambda x: bytes(x, 'UTF-8'), header))

        self.assertEqual(lines, header)

        self.assertTrue(re.search("a setting's comment\n\s+\"setting1", result))
        self.assertTrue(re.search("\"setting3\".*// inline", result))

    def test_list(self):
        obj = CommentedJSON()
        data = obj.load(path=CommentTest.fqlist)
        result = obj.as_string(data)

        self.assertTrue(re.search("2,\s+// hanging", result))

    def test_store(self):
        obj = CommentedJSON()
        data = obj.load(path=CommentTest.fqtest)
        result = obj.as_string(data)

        obj.store(data=data, path=CommentTest.fqcomment)

        with open(CommentTest.fqcomment, 'rb') as fh:
            file_text = fh.read()

        if sys.version_info[0] == 3:
            file_text = file_text.decode('UTF-8')

        self.assertEqual(result, file_text)

    def test_load_from_string(self):
        string = '//heading line1\n//heading line2\n{\n    //test\n    "setting1": 2\n}'
        obj = CommentedJSON()
        data = obj.load(string=string)

        self.assertEqual(data, {"setting1": 2})

        as_string = obj.as_string(data)
        self.assertEqual(string.split("\n")[:2], as_string.split("\n")[:2])


###############################################################################
if __name__ == "__main__":
    unittest.main()
