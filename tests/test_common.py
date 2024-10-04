import sys
import os
import unittest
from unittest.mock import MagicMock

# Add path to code under test.
test_path = os.path.join(os.path.dirname(__file__), '..')
if test_path not in sys.path:
      sys.path.insert(0, test_path)

# Now import the sublime emulation.
import emu_sublime
import emu_sublime_plugin
sys.modules["sublime"] = emu_sublime
sys.modules["sublime_plugin"] = emu_sublime_plugin

# Now import the code under test.
import sbot_common as sc


#-----------------------------------------------------------------------------------
class TestCommon(unittest.TestCase):

    def setUp(self):

        notr_files_path = os.path.join(emu_sublime.packages_path(), 'Notr', 'files')

        mock_settings = {
            "projects": [],
            "sort_tags_alpha": True,
            "mru_size": 5,
            "fixed_hl_whole_word": True,
            "section_marker_size": 1,
        }
        emu_sublime.load_settings = MagicMock(return_value=mock_settings)

        # Mock top level entities.
        self.view = emu_sublime.View(10)
        self.window = emu_sublime.Window(20)
        self.view.window = MagicMock(return_value=self.window)

        # Mock syntax interrogation.
        self.syntax = emu_sublime.Syntax('', 'Notr', False, '')
        self.view.syntax = MagicMock(return_value=self.syntax)

    def tearDown(self):
        pass

    @unittest.skip('')
    def test_something(self):
        sc.error("amamamamama")

    def test_simple(self):

        # settings = emu_sublime.load_settings("DEV_SETTINGS_FILE")
        # print(type(settings))
        # print(dir(settings))
        # print(settings)


        window = emu_sublime.Window(900)
        view = emu_sublime.View(901)

        view.window = MagicMock(return_value=window)
        view.file_name = MagicMock(return_value='file123.abc')

        # Do the tests. TODO fix broken ones.
        
        # sc.create_new_view(window, "text", reuse=True)
        
        sc.debug("message")
        
        sc.error("message", tb=None)
        
        sc.expand_vars("s")
        
        sc.get_highlight_info(which='all')
        
        sc.get_path_parts(window, ["paths"])
        
        # sc.get_sel_regions(view)
        
        # sc.get_single_caret(view)
        
        sc.get_store_fn("fn")
        
        sc.info("message")
        
        # sc.open_path("path")
        
        # sc.open_terminal("where")
        
        sc.wait_load_file(window, "fpath", 111)


