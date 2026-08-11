import sys
import os
import sublime
from unittesting import TestCase
from unittest.mock import MagicMock


# Play with ST unittesting
# from https://github.com/SublimeText/UnitTesting
#      https://github.com/randy3k/UnitTesting-example/blob/master/tests/test_hw.py

#-----------------------------------------------------------------------------------
# Interact with the target window.
class TestHelloWorldCommand(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # # make sure we have a window to work with ... not really needed?
        # s = sublime.load_settings("Preferences.sublime-settings")
        # s.set("close_windows_when_empty", False)

    def tearDown(self):
        # if self.view:
        self.view.set_scratch(True)
        self.view.window().focus_view(self.view)
        self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_hello_world(self):
        # print('==============================')
        self.setText("new ")
        self.view.run_command("hello_world")
        first_row = self.getRow(0)
        self.assertEqual(first_row, "new hello world")


#-----------------------------------------------------------------------------------
class TestFunctions(TestCase):
    # unit test non-ST code

    # Code under test.
    mod_dev = sys.modules["SbotDev.sbot_dev"]

    def test_foo(self):
        x = self.mod_dev.foo(1)
        # print('+++ foo=', x)
        self.assertEqual(x, 2)

    def test_new(self):
        self.mod_dev._dump('googoogogogogogogo')

        # can access common from here too!
        sout = self.mod_dev.sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
        self.mod_dev._dump(f'>>> [{sout}]')
        self.assertIsNotNone(sout)
        self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

        # print('+++', dir(mod_dev))
        # 'DevEvent'
        # 'HelloWorldCommand'
        # 'SbotDebugCommand'
        # '_dump'
        # 'foo'
        # 'pbot_path'
        # 'pbot_pdb'
        # 'sc'
