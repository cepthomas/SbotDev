import sys
import os
import random
import sublime
from unittesting import TestCase
from unittest.mock import MagicMock

# Import the code under test.
import sbot_common as sc


#-----------------------------------------------------------------------------------
class TestCommon(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()

        # # make sure we have a window to work with TODO needed?
        # s = sublime.load_settings("Preferences.sublime-settings")
        # s.set("close_windows_when_empty", False)
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
        sout = sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
        # print('>>>', sout)
        self.assertIsNotNone(sout)
        self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

        sout = sc.expand_vars(R'Sublime Text\$BAD_NAME\wwww')
        self.assertIsNone(sout)

        # sout = sc.get_store_fn()
        # # print('>>>', sout)
        # self.assertTrue(R'User\SBOT_DEV\SBOT_DEV.store' in sout)

        parts = sc.get_path_parts(window, ['invalid-path'])
        # print('>>>', parts)
        # Returns (dir, fn, path)
        self.assertEqual(len(parts), 3)
        self.assertIsNone(parts[0])
        self.assertIsNone(parts[1])
        # TODO1 in test actually returns parts[0]  self.assertIsNone(parts[2])

        # print('>>>', window)
        parts = sc.get_path_parts(window, [test_file_1, 'dont-care'])
        # print('>>>', parts)
        self.assertIsNotNone(parts)
        self.assertIsNotNone(parts[0])
        self.assertIsNotNone(parts[1])
        self.assertIsNotNone(parts[2])
        self.assertEqual(parts[0][-22:], R'Packages\SbotDev\tests')
        self.assertEqual(parts[1], R'ross.txt')
        self.assertTrue(R'Packages\SbotDev\tests\ross.txt' in parts[2])

        # Note: these are by inspection.
        # sc.open_path(test_file_1)    # -> in ST
        # sc.open_path(test_file_2)    # -> in irfanview
        # sc.open_path(test_path)      # -> in explorer
        # sc.open_terminal(test_path)  # -> in terminal

        # ### Windows and views. TODO fix these
        # vnew = sc.create_new_view(window, 'With practice comes confidence.', reuse=True)
        # # self.assertEqual(vnew.size(), 31)

        # vnew = sc.wait_load_file(window, test_file_1, 111)  # -> in window
        # # self.assertEqual(vnew.size(), 1620)

        hls = sc.get_highlight_info(which='all')
        self.assertEqual(len(hls), 9)

        # regs = sc.get_sel_regions(vnew)
        # self.assertEqual(len(regs), 1)
        # self.assertEqual(regs[0].a, 0)
        # self.assertEqual(regs[0].b, 1620)

        # caret = sc.get_single_caret(vnew)
        # self.assertEqual(caret, 1620)


    #------------------------------------------------------------
    def test_store(self):

        # Test file.
        fn = os.path.join(sublime.packages_path(), 'User', sc._plugin_name, f'{sc._plugin_name}.store')
        os.remove(fn)

        ind = random.randint(1, 999)

        testx = { f"apple{ind}": { "abool": True, "alist": [random.randint(1, 999), random.randint(1, 999)] }}

        sc.write_store(testx)

        ftext = '???'
        with open(fn, 'r') as fp:
            ftext = fp.read()

        self.assertIn(f"apple{ind}", ftext)
        # print('store text:', ftext)


    #------------------------------------------------------------
    def test_log(self):

        # test_path = os.path.join(os.path.dirname(__file__))
        # test_file_1 = f'{test_path}\\ross.txt'
        # test_file_2 = f'{test_path}\\felix200.jpg'

        ### Logging.
        sc.debug('This is a debug message')
        sc.info('This is an info message')
        
        sc.error('This is an error message with no traceback')

        try:
            x = 1 / 0
        except Exception as e:
            sc.error('This is an error message with traceback', e.__traceback__)







    ### old original
    # #------------------------------------------------------------
    # def test_basic(self):

    #     window = emu.Window(900)
    #     view = emu.View(901)

    #     test_path = os.path.join(os.path.dirname(__file__))
    #     test_file_1 = f'{test_path}\\ross.txt'
    #     test_file_2 = f'{test_path}\\felix200.jpg'

    #     ### Utilities.
    #     sout = sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
    #     # print('>>>', sout)
    #     self.assertIsNotNone(sout)
    #     self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

    #     sout = sc.expand_vars(R'Sublime Text\$BAD_NAME\wwww')
    #     self.assertIsNone(sout)

    #     # sout = sc.get_store_fn()
    #     # # print('>>>', sout)
    #     # self.assertTrue(R'User\SBOT_DEV\SBOT_DEV.store' in sout)

    #     parts = sc.get_path_parts(window, ['invalid-path'])
    #     # print('>>>', parts)
    #     # Returns (dir, fn, path)
    #     self.assertEqual(len(parts), 3)
    #     self.assertIsNone(parts[0])
    #     self.assertIsNone(parts[1])
    #     # TODO1 in test actually returns parts[0]  self.assertIsNone(parts[2])

    #     # print('>>>', window)
    #     parts = sc.get_path_parts(window, [test_file_1, 'dont-care'])
    #     # print('>>>', parts)
    #     self.assertIsNotNone(parts)
    #     self.assertIsNotNone(parts[0])
    #     self.assertIsNotNone(parts[1])
    #     self.assertIsNotNone(parts[2])
    #     self.assertEqual(parts[0][-22:], R'Packages\SbotDev\tests')
    #     self.assertEqual(parts[1], R'ross.txt')
    #     self.assertTrue(R'Packages\SbotDev\tests\ross.txt' in parts[2])

    #     # Note: these are by inspection.
    #     # sc.open_path(test_file_1)    # -> in ST
    #     # sc.open_path(test_file_2)    # -> in irfanview
    #     # sc.open_path(test_path)      # -> in explorer
    #     # sc.open_terminal(test_path)  # -> in terminal

    #     ### Windows and views.
    #     vnew = sc.create_new_view(window, 'With practice comes confidence.', reuse=True)
    #     # self.assertEqual(vnew.size(), 31)

    #     vnew = sc.wait_load_file(window, test_file_1, 111)  # -> in window
    #     self.assertEqual(vnew.size(), 1620)

    #     hls = sc.get_highlight_info(which='all')
    #     self.assertEqual(len(hls), 9)

    #     regs = sc.get_sel_regions(vnew)
    #     self.assertEqual(len(regs), 1)
    #     self.assertEqual(regs[0].a, 0)
    #     self.assertEqual(regs[0].b, 1620)

    #     caret = sc.get_single_caret(vnew)
    #     self.assertIsNone(caret)


    # #------------------------------------------------------------
    # def test_log(self):

    #     # test_path = os.path.join(os.path.dirname(__file__))
    #     # test_file_1 = f'{test_path}\\ross.txt'
    #     # test_file_2 = f'{test_path}\\felix200.jpg'

    #     ### Logging.
    #     sc.debug('This is a debug message')
    #     sc.info('This is an info message')
        
    #     sc.error('This is an error message with no traceback')

    #     try:
    #         x = 1 / 0
    #     except Exception as e:
    #         sc.error('This is an error message with traceback', e.__traceback__)

