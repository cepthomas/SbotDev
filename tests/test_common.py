import sys
import os
import traceback
import unittest
from unittest.mock import MagicMock

# Set up the sublime emulation environment.
import emu_sublime_api as emu

# Import the code under test.
import sbot_common as sc


#-----------------------------------------------------------------------------------
class TestCommon(unittest.TestCase):

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
        test_file_2 = f'{test_path}\\felix.jpg'

        ### Logging.
        sc.debug('This is a debug message')
        sc.info('This is an info message')
        
        sc.error('This is an error message with no traceback')
        try:
            x = 1 / 0
        except Exception as e:
            sc.error('This is an error message with traceback', e.__traceback__)

        ### Utilities.
        sout = sc.expand_vars('$APPDATA/Sublime Text/Packages/SbotDev')
        self.assertIsNotNone(sout)
        self.assertTrue(r'\AppData\Roaming/Sublime Text/Packages/SbotDev' in sout)

        sout = sc.expand_vars('C:/Sublime Text/$BAD_NAME\\wwww')
        self.assertIsNone(sout)

        sout = sc.get_store_fn()
        self.assertTrue(r'Packages\User\Dev\Dev.store' in sout)

        parts = sc.get_path_parts(window, ['invalid-path'])
        # Returns (dir, fn, path)
        self.assertEqual(len(parts), 3)
        self.assertIsNone(parts[0])
        self.assertIsNone(parts[1])
        self.assertIsNone(parts[2])

        parts = sc.get_path_parts(window, [test_file_1, 'dont-care'])
        self.assertIsNotNone(parts)
        self.assertIsNotNone(parts[0])
        self.assertIsNotNone(parts[1])
        self.assertIsNotNone(parts[2])
        self.assertEqual(parts[0][-22:], r'Packages\SbotDev\tests')
        self.assertEqual(parts[1], r'ross.txt')
        self.assertTrue(r'Packages\SbotDev\tests\ross.txt' in parts[2])

        # Note: these are by inspection.
        # sc.open_path(test_file_1)    # -> in ST
        # sc.open_path(test_file_2)    # -> in irfanview
        # sc.open_path(test_path)      # -> in explorer
        # sc.open_terminal(test_path)  # -> in terminal

        ### Windows and views. TODOT more tests
        vnew = sc.create_new_view(window, 'With practice comes confidence.', reuse=True)
        # self.assertEqual(vnew.size(), 31)

        vnew = sc.wait_load_file(window, test_file_1, 111)  # -> in window
        self.assertEqual(vnew.size(), 1597)

        hls = sc.get_highlight_info(which='all')
        self.assertEqual(len(hls), 9)

        regs = sc.get_sel_regions(vnew)
        self.assertEqual(len(regs), 1)
        self.assertEqual(regs[0].a, 0)
        self.assertEqual(regs[0].b, 1597)
        
        caret = sc.get_single_caret(vnew)
        self.assertIsNone(caret)
