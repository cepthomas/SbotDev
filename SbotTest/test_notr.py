import unittest
from unittest.mock import MagicMock
import sublime
import sublime_plugin
#from sbot_common import *
import Notr.notr as snotr


#-----------------------------------------------------------------------------------
class TestNotr(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        '''...'''
        # self.assertEqual('foo'.upper(), 'FOO')

        # Old stuff
        view = sublime.View(600)
        sel = sublime.Selection(view.id())
        sel.add(sublime.Region(10, 20, 101))
        view.sel = MagicMock(return_value = sel)

        # Mock syntax.
        syntax = sublime.Syntax()
        syntax.name = MagicMock(return_value = 'Notr')
        view.syntax = MagicMock(return_value = syntax)

        # Mock settings.
        mock_settings = {
            "notr_paths": ["C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Packages\\Notr", "C:\\Users\\cepth\\OneDrive\\OneDrive Documents\\_notes"],
            "visual_line_length": 100,
            "user_hl": [["2DO", "things"], ["user"], ["dynamic"], ["and_a"], ["and_b"], ["and_c"]],
            "user_hl_whole_word": True,
        }
        sublime.load_settings = MagicMock(return_value = mock_settings)

        # Mock settings with side effect.
        #settings = sublime.load_settings('NOTR_SETTINGS_FILE')
        #notr_paths = settings.get('notr_paths')
        #def settings_get_side_effect(*args, **kwargs):
        #    if args[0] == 'notr_paths':
        #        return ["C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Packages\\Notr",
        #                "C:\\Users\\cepth\\OneDrive\\OneDrive Documents\\_notes" ]
        #    else:
        #        raise Exception('haha')
        #settings.get = MagicMock(side_effect = settings_get_side_effect)


        ##### Run code under test. #####

        ### NotrEvent(sublime_plugin.EventListener):
        evt = snotr.NotrEvent()
        evt.on_init([view])
        #self.assertEqual(1, 2, 'just a test test')


        text_cmd = sublime_plugin.TextCommand(view)
        edit = sublime.Edit('token')

        ### NotrGotoRefCommand(sublime_plugin.TextCommand):
        cmd = snotr.NotrGotoRefCommand(view)
        cmd.run(edit)



        ### NotrGotoSectionCommand(sublime_plugin.TextCommand):


        ### NotrInsertRefCommand(sublime_plugin.TextCommand):



        #def test_something(self):
        #    '''...'''
        #    # self.assertEqual('foo'.upper(), 'FOO')
        #    view = sublime.View(600)
        #    sel = sublime.Selection(view.id())
        #    sel.add(sublime.Region(10, 20, 101))
        #    view.sel = MagicMock(return_value = sel)
        #    evt = sutils.SbotEvent()
        #    evt.on_selection_modified(view)
        #    #self.assertEqual(1, 2, 'just a test test')

        #def test_format_json(self):
        #    v = sublime.View(601)
        #    with open(r'.\files\messy.json', 'r') as fp:
        #        # The happy path.
        #        s = fp.read()
        #        cmd = sformat.SbotFormatJsonCommand(v)
        #        res = cmd._do_one(s)
        #        self.assertEqual(res[:50], '{\n    "MarkPitch": {\n        "Original": 0,\n      ')
        #        # Make it a bad file.
        #        s = s.replace('\"Original\"', '')
        #        res = cmd._do_one(s)
        #        self.assertEqual(res[:50], "Json Error: Expecting property name enclosed in do")



#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
