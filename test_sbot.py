import sys
import os
import platform
import pdb
import unittest
from unittest.mock import MagicMock

import sublime
import sublime_plugin

from . import sbot_common as sc
from SbotFormat import sbot_format
from SbotHighlight import sbot_highlight
from Notr import notr, table


# TODO1 relocate to other packages.


# Experiments with testing py code in general and ST plugins specifically.

# print(f'Running {__file__} with python {platform.python_version()} on {platform.platform()}')


# Exclude unittests from production builds
# ->
# # git
# .github/ export-ignore
# .git export-ignore
# .gitignore export-ignore
# .gitattributes export-ignore
# # development utilities
# /dev/ export-ignore
# .travis.yml export-ignore
# tox.ini export-ignore
# # unittests
# tests/ export-ignore
# # example files
# /example-*.json export-ignore

# Add root unittesting.json:
# {
#     "tests_dir": "package_control/tests",
#     "pattern": "test*.py",
#     "verbosity": 1
# }



#-----------------------------------------------------------------------------------
class TestFormat(unittest.TestCase):

    def setUp(self):
        mock_settings = {
            "tab_size": 4,
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

    def tearDown(self):
        pass

    def test_format_json(self):
        v = sublime.View(601)

        with open(r'SbotDev\test_files\messy.json', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatJsonCommand(v)
            res = cmd._do_one(s)
            self.assertEqual(res[:50], '{\n    "MarkPitch": {\n        "Original": 0,\n      ')

            # Make it a bad file.
            s = s.replace('\"Original\"', '')
            res = cmd._do_one(s)
            self.assertEqual(res[:50], "Json Error: Expecting property name enclosed in do")

    def test_format_xml(self):
        v = sublime.View(602)

        with open(r'SbotDev\test_files\messy.xml', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatXmlCommand(v)
            res = cmd._do_one(s, '    ')

            if 'Error:' in res:
                self.fail(res)
            else:
                self.assertEqual(res[100:150], 'nType="Anti-IgG (PEG)" TestSpec="08 ABSCR4 IgG" Du')

            # Make it a bad file.
            s = s.replace('ColumnType=', '')
            res = cmd._do_one(s, '    ')
            self.assertEqual(res, "Error: not well-formed (invalid token): line 6, column 4")


#-----------------------------------------------------------------------------------
class TestHighlight(unittest.TestCase):

    def setUp(self):
        mock_settings = {
            "highlight_scopes": ["region.redish", "region.yellowish", "region.greenish", "region.cyanish", "region.bluish", "region.purplish"],
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

    def tearDown(self):
        pass

    def test_simple(self):
        window = sublime.Window(900)
        view = sublime.View(901)

        view.window = MagicMock(return_value=window)
        view.file_name = MagicMock(return_value='file123.abc')

        # Do the test.
        hl_vals = sbot_highlight._get_hl_vals(view, True)
        self.assertIsNotNone(hl_vals)


#-----------------------------------------------------------------------------------
class TestNotr(unittest.TestCase):

    def setUp(self):

        notr_files_path = os.path.join(sublime.packages_path(), 'Notr', 'files')

        mock_settings = {
            "projects": [],
            "sort_tags_alpha": True,
            "mru_size": 5,
            "fixed_hl_whole_word": True,
            "section_marker_size": 1,
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

        # Mock top level entities.
        self.view = sublime.View(10)
        self.window = sublime.Window(20)
        self.view.window = MagicMock(return_value=self.window)

        # Mock syntax interrogation.
        self.syntax = sublime.Syntax('', 'Notr', False, '')
        self.view.syntax = MagicMock(return_value=self.syntax)

    def tearDown(self):
        pass

    # @unittest.skip('')
    def test_parsing(self):
        ''' Tests the .ntr file parsing. '''

        # notr._process_notr_files()
        # for e in notr._parse_errors:
        #     print(f'parse error:{e}')

        # evt = notr.NotrEvent()
        # evt.on_init([self.view])

        # self.assertEqual(len(notr._tags), 7)
        # self.assertEqual(len(notr._links), 6)
        # self.assertEqual(len(notr._refs), 6)
        # self.assertEqual(len(notr._sections), 13)
        # self.assertEqual(len(notr._parse_errors), 0)

    @unittest.skip('')
    def test_GotoRef(self):
        cmd = notr.NotrGotoTargetCommand(self.view)
        cmd.run(None, False)

    # @unittest.skip('')
    # def test_InsertRef(self):
    #     cmd = notr.NotrInsertRefCommand(self.view)
    #     edit = sublime.Edit
    #     cmd.run(edit)


#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    # https://docs.python.org/3/library/unittest.html#unittest.main
    tp = unittest.main(verbosity=2, exit=False)
    print(tp.result)
