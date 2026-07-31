import sys
import os
import traceback
import unittest
import importlib
# from unittest.mock import MagicMock

# Set up the sublime emulation environment.
import emu_sublime_api as emu

# Set up path to code under test.
# print('--- sys.path before', sys.path)
cut_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if cut_path not in sys.path: sys.path.insert(0, cut_path)
# print('--- sys.path after', sys.path)

# Now import cut.
import sbot_dev as sdev

# A local file in this directory.
import sbot_common as sc





#-----------------------------------------------------------------------------------
class TestDev(unittest.TestCase):

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
        # sout = sc.expand_vars(R'$APPDATA\Sublime Text\Packages\SbotDev')
        # # print('>>>', sout)
        # self.assertIsNotNone(sout)
        # self.assertTrue(R'AppData\Roaming\Sublime Text\Packages\SbotDev' in sout)

        # sout = sc.expand_vars(R'Sublime Text\$BAD_NAME\wwww')
        # self.assertIsNone(sout)

        # sout = sc.get_store_fn()
        # # print('>>>', sout)
        # self.assertTrue(R'User\SBOT_DEV\SBOT_DEV.store' in sout)

