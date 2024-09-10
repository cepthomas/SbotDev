import sys
import os
import subprocess
import platform
import traceback
import datetime
import importlib
import bdb
import sublime
import sublime_plugin
import unittest
from unittest.mock import MagicMock
from . import sbot_common as sc

from SbotFormat import sbot_format
from SbotHighlight import sbot_highlight
# from SbotALogger import sbot_logger
from Notr import notr, table


# Experiments with testing py code in general and ST plugins specifically.


DEV_SETTINGS_FILE = "SbotDev.sublime-settings"



#-----------------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    sc.info(f'Loading {__package__} with python {platform.python_version()} on {platform.platform()}')



#-----------------------------------------------------------------------------------
class TestStEmul(unittest.TestCase):
    ''' Test the sublime api emulation. '''

    _settings_file = os.path.join('files', 'test_settings.sublime-settings')
    _test_file1 = os.path.join('files', 'ross.txt')
    _test_file2 = os.path.join('files', 'messy.cs')

    def setUp(self):
        sublime._reset()

    def tearDown(self):
        pass

    #@unittest.skip
    def test_module(self):
        ''' sublime.module '''

        settings = sublime.load_settings(self._settings_file)
        self.assertEqual(len(settings), 3)

        sublime.set_clipboard('we need a little path')
        self.assertEqual(sublime.get_clipboard(), 'we need a little path')

        sublime.set_timeout(lambda: settings.set('a_null', None), 100)
        self.assertEqual(len(settings), 4)

        ## Not implemented.
        #view = sublime.View(-1)
        #self.assertRaises(NotImplementedError, view.run_command, 'a_command')


    #@unittest.skip
    def test_window(self):
        ''' sublime.Window() '''

        settings = sublime.load_settings(self._settings_file)

        # Make a window.
        window = sublime.Window(202)
        self.assertTrue(window.is_valid())
        self.assertEqual(len(window.settings()), 3)

        # Add some views.
        view1 = window.open_file(self._test_file1)
        view2 = window.new_file()
        view3 = window.open_file(self._test_file2)
        view4 = window.new_file()

        self.assertEqual(len(window.views()), 4)
        self.assertEqual(window.views()[0], view1)
        self.assertEqual(window.views()[3], view4)
        self.assertEqual(window.find_open_file(self._test_file2), view3)
        self.assertIsNone(window.find_open_file('Invalid filename'))
        self.assertEqual(window.get_view_index(view4), 3)

        ## Not implemented.
        #self.assertRaises(NotImplementedError, window.focus_view, view1)
        #self.assertRaises(NotImplementedError, window.run_command, 'a_command')


    #@unittest.skip
    def test_view(self):
        ''' sublime.View() '''
        window = sublime.Window(303)

        view1 = window.open_file(self._test_file1)
        view2 = window.new_file()
        view3 = window.open_file(self._test_file2)
        view4 = window.new_file()

        self.assertTrue(view1 == view1) # __eq__
        self.assertFalse(view2 == view3)

        self.assertEqual(len(view1), 1583) # __len__
        self.assertEqual(view1.size(), 1583)
        self.assertEqual(view1.id(), 1)
        self.assertTrue(view1) # __bool__
        self.assertEqual(view1.window(), window)
        self.assertEqual(view1.file_name(), self._test_file1)

        self.assertEqual(len(view2), 0)
        self.assertEqual(view2.size(), 0)
        self.assertEqual(view2.id(), 2)
        self.assertEqual(view2.window(), window)
        self.assertEqual(view2.file_name(), '')

        self.assertEqual(len(view3), 1327)
        self.assertEqual(view3.size(), 1327)
        self.assertEqual(view3.id(), 3)
        self.assertEqual(view3.window(), window)
        self.assertEqual(view3.file_name(), self._test_file2)

        self.assertEqual(len(view4), 0)
        self.assertEqual(view4.size(), 0)
        self.assertEqual(view4.id(), 4)
        self.assertEqual(view4.window(), window)
        self.assertEqual(view4.file_name(), '')

        # rowcol()
        self.assertEqual(view1.rowcol(0), (0, 0))
        self.assertEqual(view1.rowcol(100), (2, 57))
        self.assertEqual(view1.rowcol(1000), (13, 47))
        self.assertEqual(view1.rowcol(1582), (22, 94))
        self.assertRaises(ValueError, view1.rowcol, 1583)
        #self.assertEqual(view1.rowcol(1583), (22, 95))

        # text_point()
        self.assertEqual(view1.text_point(0, 0), 0)
        self.assertEqual(view1.text_point(8, 29), 666)
        self.assertEqual(view1.text_point(20, 46), 1466)
        #self.assertRaises(ValueError, view1.text_point, 23456, 34)

        # utilities
        lines = view1.split_by_newlines(sublime.Region(309, 1075))
        self.assertEqual(len(lines), 12)
        self.assertTrue(lines[0].startswith('I don\'t'))
        self.assertTrue(lines[11].endswith('the wo'))

        # find
        ss = view1.substr(17)
        self.assertEqual(ss, ':')
        ss = view1.substr(sublime.Region(373, 394))
        self.assertEqual(ss, 'ake these big decisio')

        reg = view1.word(0)
        self.assertEqual(view1.substr(reg), 'line-1')
        reg = view1.word(913)
        self.assertEqual(view1.substr(reg), 'fairytale')
        reg = view1.word(sublime.Region(1125, 1137))
        self.assertEqual(view1.substr(reg), 'everything can be happy.')
        reg = view1.word(sublime.Region(699, 720)) # has line end in middle
        self.assertEqual(view1.substr(reg), 'in the world.\nI like to')

        reg = view1.line(1140)
        self.assertEqual(view1.substr(reg), 'In this world, everything can be happy. If you hypnotize it, it will go away.')
        reg = view1.line(sublime.Region(1186, 1193))
        self.assertEqual(view1.substr(reg), 'Let your heart be your guide.')

        reg = view1.full_line(1194)
        self.assertEqual(view1.substr(reg), 'Let your heart be your guide.\n')
        reg = view1.full_line(sublime.Region(455, 470))
        self.assertEqual(view1.substr(reg), 'Don\'t hurry. Take your time and enjoy.\n')

        reg = view1.find('it really just happens', 100)
        self.assertIsNotNone(reg)
        self.assertEqual(view1.substr(reg), 'it really just happens')
        reg = view1.find('this is no good', 0)
        self.assertIsNone(reg)

        regs = view1.find_all('have')
        self.assertIsNotNone(regs)
        self.assertEqual(len(regs), 4)
        self.assertEqual(view1.substr(regs[1]), 'have')

        # edit
        num = view1.insert(None, 753, 'zzzzzzzzzz')
        self.assertEqual(num, 10)
        self.assertEqual(len(view1), 1593)

        num = view1.replace(None, sublime.Region(245, 265), '-----')
        self.assertEqual(num, 5)
        self.assertEqual(len(view1), 1578)

        # Not implemented. So far.
        #view = sublime.View(-1)
        #self.assertRaises(NotImplementedError, view.sel)
        #self.assertRaises(NotImplementedError, view.syntax)
        #self.assertRaises(NotImplementedError, view.scope_name, 0)
        #self.assertRaises(NotImplementedError, view.style_for_scope, '')
        #self.assertRaises(NotImplementedError, view.add_regions, '', []) #, scope="", icon="", flags=0)
        #self.assertRaises(NotImplementedError, view.get_regions, '')
        #self.assertRaises(NotImplementedError, view.erase_regions, '')
        #self.assertRaises(NotImplementedError, view.run_command, '')



#-----------------------------------------------------------------------------------
class TestFormat(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_json(self):
        v = sublime.View(601)

        with open(r'.\test_files\messy.json', 'r') as fp:
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

        with open(r'.\test_files\messy.xml', 'r') as fp:
            # The happy path.
            s = fp.read()
            cmd = sbot_format.SbotFormatXmlCommand(v)
            res = cmd._do_one(s)
            self.assertEqual(res[100:150], 'nType="Anti-IgG (PEG)" TestSpec="08 ABSCR4 IgG" Du')

            # Make it a bad file.
            s = s.replace('ColumnType=', '')
            res = cmd._do_one(s)
            self.assertEqual(res, "Error: not well-formed (invalid token): line 6, column 4")


#-----------------------------------------------------------------------------------
class TestHighlight(unittest.TestCase):

    def setUp(self):
        mock_settings = {
            # List of up to 6 scope names for highlight commands.
            "highlight_scopes": [ "region.redish", "region.yellowish", "region.greenish", "region.cyanish", "region.bluish", "region.purplish" ],
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
class TestLogger(unittest.TestCase):

    def setUp(self):
        mock_settings = {
            "file_size": 5,
            "notify_cats": ["EXC", "ERR", "WRN"],
            "ignore_cats": [],
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)
        # sbot_logger.plugin_loaded()

    def tearDown(self):
        # sbot_logger.plugin_unloaded()
        pass

    def test_log_exception(self):
        # Force an unhandled exception.
        def _force_exc():
            i = 222 / 0

        # try:
        #     _force_exc()
        # except Exception as e:
        #     sbot_logger._notify_exception(e, 'value', e.__traceback__)

    def test_simple(self):
        # Do the test.
        sc.slog('TST', 'dsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsds')


#-----------------------------------------------------------------------------------
class TestNotr(unittest.TestCase):

    #------------------------------------------------------------
    def setUp(self):

        notr_files_path = os.path.join(sublime.packages_path(), 'Notr', 'files')

        # Mock settings.
        mock_settings = {
            "visual_line_length": 100,
            "fixed_hl": [["2DO", "things"], ["user", "dynamic"], ["and_a", "and_b", "and_c"]],
            "fixed_hl_whole_word": True,
        }
        mock_settings["notr_paths"] = [notr_files_path]
        mock_settings["notr_index"] = os.path.join(notr_files_path, 'test-index.ntr')
        sublime.load_settings = MagicMock(return_value=mock_settings)

        # Mock top level entities.
        self.view = sublime.View(10)
        self.window = sublime.Window(20)
        self.view._window = MagicMock(return_value=self.window)

        # Mock syntax interrogation.
        self.syntax = sublime.Syntax('', 'Notr', False, '')
        self.view.syntax = MagicMock(return_value=self.syntax)


    #------------------------------------------------------------
    def tearDown(self):
        pass


    #------------------------------------------------------------
    @unittest.skip
    def test_parsing(self):
        ''' Tests the ntr file parsing. '''

        # notr._process_notr_files()
        # for e in notr._parse_errors:
        #     print(f'parse error:{e}')

        evt = notr.NotrEvent()
        evt.on_init([self.view])

        self.assertEqual(len(notr._tags), 7)
        self.assertEqual(len(notr._links), 6)
        self.assertEqual(len(notr._refs), 6)
        self.assertEqual(len(notr._sections), 13)
        self.assertEqual(len(notr._parse_errors), 0)


    #------------------------------------------------------------
    @unittest.skip
    def test_GotoRef(self):
        cmd = notr.NotrGotoRefCommand(self.view)
        cmd.run(None)


    #------------------------------------------------------------
    @unittest.skip
    def test_GotoSection(self):
        cmd = notr.NotrGotoSectionCommand(self.view)
        cmd.run(None)


    #------------------------------------------------------------
    @unittest.skip
    def test_InsertRef(self):
        cmd = notr.NotrInsertRefCommand(self.view)
        cmd.run(None)

#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    # https://docs.python.org/3/library/unittest.html#unittest.main
    tp = unittest.main(verbosity=2, exit=False)
    print(tp.result)