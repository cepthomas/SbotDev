import sys
import os
import sublime
from unittesting import TestCase


# from https://github.com/SublimeText/UnitTesting
#      https://github.com/randy3k/UnitTesting-example/blob/master/tests/test_hw.py


#-----------------------------------------------------------------------------------
class TestHelloWorldCommand(TestCase):
    # using sublime view/window TODO1 fully replace my emu (Notr, SbotDev)?

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_hello_world(self):
        self.setText("new ")
        self.view.run_command("hello_world")
        first_row = self.getRow(0)
        self.assertEqual(first_row, "new hello world")


#-----------------------------------------------------------------------------------
class TestFunctions(TestCase):
    # unit test non-ST code

    sdev = sys.modules["SbotDev.sbot_dev"] # was ["UnitTesting-example.helloworld"]

    def test_foo(self):
        x = self.sdev.foo(1)
        print('+++ foo=', x)
        self.assertEqual(x, 2)

    def test_new(self):
        self.sdev._dump('googoogogogogogogo')

        # can access common from here too!
        sout = self.sdev.sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
        self.sdev._dump(f'>>> [{sout}]')
        self.assertIsNotNone(sout)
        self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

        # print('+++', dir(sdev))
        # 'DevEvent'
        # 'HelloWorldCommand'
        # 'SbotDebugCommand'
        # '_dump'
        # 'foo'
        # 'pbot_path'
        # 'pbot_pdb'
        # 'sc'




''' My original way
import sys
import os
import importlib
from unittest import TestCase
# from unittest.mock import MagicMock

# Set up the sublime emulation environment.
import emu_sublime_api as emu

# Set up path to code under test.
print('---', 'sys.path before', sys.path)
cut_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if cut_path not in sys.path: sys.path.insert(0, cut_path)
print('---', 'sys.path after', sys.path)

# Now import cut.
import sbot_dev as sdev
# A local file in this directory.
import sbot_common as sc


#-----------------------------------------------------------------------------------
class TestDev(TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    #------------------------------------------------------------
    def test_basic(self):
        window = emu.Window(900)
        view = emu.View(901)

        test_path = os.path.join(os.path.dirname(__file__))
        test_file_1 = f'{test_path}\\ross.txt'
        test_file_2 = f'{test_path}\\felix200.jpg'

        sout = sc.get_store_fn()
        print('>>> store_fn:', sout)
        self.assertTrue(R'User\SBOT_DEV\SBOT_DEV.store' in sout)

        ### Utilities.
        sout = sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
        # print('>>>', sout)
        self.assertIsNotNone(sout)
        self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

        # sout = sc.expand_vars(R'Sublime Text\$BAD_NAME\wwww')
        # self.assertIsNone(sout)

        # sout = sc.get_store_fn()
        # # print('>>>', sout)
        # self.assertTrue(R'User\SBOT_DEV\SBOT_DEV.store' in sout)
'''
