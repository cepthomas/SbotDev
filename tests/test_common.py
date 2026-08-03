import sys
import os
import random
import sublime
from unittesting import TestCase
from unittest.mock import MagicMock


#-----------------------------------------------------------------------------------
class TestCommon(TestCase):

    # Code under test.
    mod_sc = sys.modules["SbotDev.sbot_common"]

    def setUp(self):
        self.view = sublime.active_window().new_file()
        random.seed()

    def tearDown(self):
        # if self.view:
        self.view.set_scratch(True)
        self.view.window().focus_view(self.view)
        self.view.window().run_command("close_file")


    #------------------------------------------------------------
    def test_basic(self):

        window = self.view.window()
        # window = emu.Window(900)
        # view = emu.View(901)

        test_path = os.path.join(os.path.dirname(__file__))
        test_file_1 = f'{test_path}\\ross.txt'
        test_file_2 = f'{test_path}\\felix200.jpg'

        ### Utilities.
        sout = self.mod_sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
        self.assertIsNotNone(sout)
        self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

        sout = self.mod_sc.expand_vars(R'Sublime Text\$BAD_NAME\wwww')
        self.assertIsNone(sout)

        parts = self.mod_sc.get_path_parts(window, ['invalid-path'])
        # Returns (dir, fn, path)
        self.assertEqual(len(parts), 3)
        self.assertIsNone(parts[0])
        self.assertIsNone(parts[1])
        # TODO: in test this actually returns parts[0]:
        # self.assertIsNone(parts[2])

        parts = self.mod_sc.get_path_parts(window, [test_file_1, 'dont-care'])
        self.assertIsNotNone(parts)
        self.assertIsNotNone(parts[0])
        self.assertIsNotNone(parts[1])
        self.assertIsNotNone(parts[2])
        self.assertEqual(parts[0][-22:], R'Packages\SbotDev\tests')
        self.assertEqual(parts[1], R'ross.txt')
        self.assertTrue(R'Packages\SbotDev\tests\ross.txt' in parts[2])

        # Note: these are by inspection.
        # self.mod_sc.open_path(test_file_1)    # => in ST
        # self.mod_sc.open_path(test_file_2)    # => in irfanview
        # self.mod_sc.open_path(test_path)      # => in explorer
        # self.mod_sc.open_terminal(test_path)  # => in terminal

        # Windows and views.
        vnew = self.mod_sc.create_new_view(window, 'With practice comes confidence.', reuse=True)
        self.assertEqual(vnew.size(), 31)

        vnew = self.mod_sc.wait_load_file(window, test_file_1, 111)  # => in window
        self.assertEqual(vnew.size(), 1620)

        hls = self.mod_sc.get_highlight_info(which='all')
        self.assertEqual(len(hls), 9)

        regs = self.mod_sc.get_sel_regions(vnew)
        self.assertEqual(len(regs), 1)
        self.assertEqual(regs[0].a, 0)
        self.assertEqual(regs[0].b, 1620)

        caret = self.mod_sc.get_single_caret(vnew)
        self.assertEqual(caret, 1620)


    #------------------------------------------------------------
    def test_store(self):

        # Test file.
        fn = os.path.join(sublime.packages_path(), 'User', self.mod_sc._plugin_name, f'{self.mod_sc._plugin_name}.store')
        os.remove(fn)

        ind = random.randint(1, 999)

        testx = { f"apple{ind}": { "abool": True, "alist": [random.randint(1, 999), random.randint(1, 999)] }}

        self.mod_sc.write_store(testx)

        ftext = '???'
        with open(fn, 'r') as fp:
            ftext = fp.read()

        self.assertIn(f"apple{ind}", ftext)


    #------------------------------------------------------------
    def test_log(self):

        # test_path = os.path.join(os.path.dirname(__file__))
        # test_file_1 = f'{test_path}\\ross.txt'
        # test_file_2 = f'{test_path}\\felix200.jpg'

        ### Logging.
        self.mod_sc.debug('This is a debug message')
        self.mod_sc.info('This is an info message')
        
        self.mod_sc.error('This is an error message with no traceback')

        try:
            x = 1 / 0
        except Exception as e:
            self.mod_sc.error('This is an error message with traceback', e.__traceback__)
