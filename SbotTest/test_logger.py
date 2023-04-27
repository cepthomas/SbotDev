from socket import setdefaulttimeout
import sys
import unittest
from unittest.mock import MagicMock#, patch
import traceback
import sublime

import SbotCommon.sbot_common as sbot
import SbotALogger.sbot_logger as slogger


'''
[in test_my_module]
@patch('external_module.api_call')
def test_some_func(self, mock_api_call): 
    mock_api_call.return_value = MagicMock(status_code=200,response=json.dumps({'key':'value'}))

my_module.some_func()

[in my_module]
import external_module
def some_func(): 
    response = external_module.api_call()  
    #normally returns a Response object, but now returns a MagicMock
    #response == mock_api_call.return_value == MagicMock(status_code=200, response=json.dumps({'key':'value'}))

Note that the argument passed to test_some_func, i.e., mock_api_call, is a MagicMock and we are setting return_value 
to another MagicMock. When mocking, everything is a MagicMock.
'''


#-----------------------------------------------------------------------------------
class TestLogger(unittest.TestCase):

    def setUp(self):
        #slogger.plugin_loaded()
        pass

    def tearDown(self):
        #slogger.plugin_unloaded()
        pass

    @unittest.mock.patch('sublime.load_settings')
    def test_log_exception(self, mock_load_settings):

        mock_settings = sublime.Settings(999)
        mock_settings.set('file_size', 5)
        mock_settings.set('notify_cats', ["EXC", "ERR", "WRN"])
        mock_settings.set('ignore_cats', [])
        mock_load_settings.return_value = mock_settings

        # This does the configuration.
        slogger.plugin_loaded()

        # Do the test. Force an unhandled exception.
        try:
            self._force_exc()
        except Exception as e:
            slogger._notify_exception(e, 'value', e.__traceback__)

        # Clean up.
        slogger.plugin_unloaded()


    def _force_exc(self):
        i = 222 / 0

    @unittest.mock.patch('sublime.load_settings')
    def test_simple(self, mock_load_settings):

        mock_settings = sublime.Settings(999)
        mock_settings.set('file_size', 5)
        mock_settings.set('notify_cats', ["EXC", "ERR", "WRN"])
        mock_settings.set('ignore_cats', [])
        mock_load_settings.return_value = mock_settings

        # This does the configuration.
        slogger.plugin_loaded()

        # Do the test.
        slog('TST', 'dsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsds')

        # Clean up.
        slogger.plugin_unloaded()


#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
