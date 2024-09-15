import sys
import os
import platform
import pdb
import unittest
from unittest.mock import MagicMock

import sublime
import sublime_plugin

# from . import sbot_common as sc
from SbotDev import sbot_common as sc
from SbotFormat import sbot_format
from SbotHighlight import sbot_highlight
from Notr import notr, table

# Experiments with testing py code in general and ST plugins specifically.


# print(f'Running {__file__} with python {platform.python_version()} on {platform.platform()}')


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

        view._window = MagicMock(return_value=window)
        view.file_name = MagicMock(return_value='file123.abc')

        # Do the test.
        hl_vals = sbot_highlight._get_hl_vals(view, True)
        self.assertIsNotNone(hl_vals)


#-----------------------------------------------------------------------------------
class TestNotr(unittest.TestCase):

    def setUp(self):

        notr_files_path = os.path.join(sublime.packages_path(), 'Notr', 'files')

        # TODO projects look like this:
        # {
        #     "notr_paths": [
        #         "$APPDATA\\Sublime Text\\Packages\\Notr\\example"
        #     ],
        #     "notr_index": "$APPDATA\\Sublime Text\\Packages\\Notr\\example\\my-index.ntr",
        #     "fixed_hl": [
        #         ["2DO", "and_a"],
        #         ["user", "and_b"],
        #         ["dynamic", "and_c"]
        #     ],
        #     "sticky": [
        #         "notr-spec#section no tags",
        #         "my-index#Other Files of Interest"
        #     ]
        # }

        mock_settings = {
            "projects": [],
            # in notr.store
            # {
            #     "C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Packages\\Notr\\example\\notr-demo.nproj": {
            #         "active": false,
            #         "mru": [
            #             "my-index#Common Links",
            #             "notr-spec#section no tags"
            #         ]
            #     },
            #     "C:\\Users\\cepth\\OneDrive\\OneDriveDocuments\\notes\\main.nproj": {
            #         "active": true,
            #         "mru": [
            #             "ascii#All",
            #             "tech-misc#Win batch",
            #             "sublime-notes#general",
            #             "sublime-commands#Plugins",
            #             "python-notes#import"
            #         ]
            #     }
            # }            
            "sort_tags_alpha": True,
            "mru_size": 5,
            "fixed_hl_whole_word": True,
            "section_marker_size": 1,
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

        # Mock top level entities.
        self.view = sublime.View(10)
        self.window = sublime.Window(20)
        self.view._window = MagicMock(return_value=self.window)

        # Mock syntax interrogation.
        self.syntax = sublime.Syntax('', 'Notr', False, '')
        self.view.syntax = MagicMock(return_value=self.syntax)

    def tearDown(self):
        pass

    # @unittest.skip
    def test_parsing(self):
        ''' Tests the ntr file parsing. '''

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

    @unittest.skip
    def test_GotoRef(self):
        cmd = notr.NotrGotoTargetCommand(self.view)
        cmd.run(None, False)

    # @unittest.skip
    def test_InsertRef(self):
        cmd = notr.NotrInsertRefCommand(self.view)
        cmd.run(None)


#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    # https://docs.python.org/3/library/unittest.html#unittest.main
    tp = unittest.main(verbosity=2, exit=False)
    print(tp.result)
