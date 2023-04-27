import unittest
from unittest.mock import MagicMock
import sublime
import SbotCommon.sbot_common
import SbotUtils.sbot_utils as sutils  #TODO fix these from .sbot_common import *


#-----------------------------------------------------------------------------------
class TestDev(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_something(self):
        '''Also has tests for the simple sbot.py.'''
        # self.assertEqual('foo'.upper(), 'FOO')

        view = sublime.View(600)

        sel = sublime.Selection(view.id())
        sel.add(sublime.Region(10, 20, 101))
        view.sel = MagicMock(return_value = sel)

        evt = sutils.SbotEvent()
        evt.on_selection_modified(view)

        #self.assertEqual(1, 2, 'just a test test')


#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
