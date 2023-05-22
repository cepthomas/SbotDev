import sys
import unittest
from unittest.mock import MagicMock
import sublime
import sublime_plugin
from sbot_common_src import *


import SbotFormat.sbot_format as sformat



#-----------------------------------------------------------------------------------
class TestFormat(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_json(self):
        v = sublime.View(601)

        with open(r'.\files\messy.json', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sformat.SbotFormatJsonCommand(v)
            res = cmd._do_one(s)
            self.assertEqual(res[:50], '{\n    "MarkPitch": {\n        "Original": 0,\n      ')

            # Make it a bad file.
            s = s.replace('\"Original\"', '')
            res = cmd._do_one(s)
            self.assertEqual(res[:50], "Json Error: Expecting property name enclosed in do")


    def test_format_xml(self):
        v = sublime.View(602)

        with open(r'.\files\messy.xml', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sformat.SbotFormatXmlCommand(v)
            res = cmd._do_one(s)
            self.assertEqual(res[100:150], 'nType="Anti-IgG (PEG)" TestSpec="08 ABSCR4 IgG" Du')

            # Make it a bad file.
            s = s.replace('ColumnType=', '')
            res = cmd._do_one(s)
            self.assertEqual(res, "Error: not well-formed (invalid token): line 6, column 4")


#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
