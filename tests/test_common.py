import sys
import os
import platform
import unittest
from unittest.mock import MagicMock

# Set path to code under test.
test_path = os.path.join(os.path.dirname(__file__), '..')

if test_path not in sys.path:
    sys.path.append(test_path)  # sys.path.insert(0, test_path)

# Now import the mocks.
import sublime
import sublime_plugin

# Now import the code under test.
import sbot_common as sc

# Exclude unittests from production builds
# ->
# # git
# .github/ export-ignore
# .git export-ignore
# .gitignore export-ignore
# .gitattributes export-ignore
# # development utilities
# /dev/ export-ignore
# .travis.yml export-ignore
# tox.ini export-ignore
# # unittests
# tests/ export-ignore
# # example files
# /example-*.json export-ignore

# Add root unittesting.json:
# {
#     "tests_dir": "package_control/tests",
#     "pattern": "test*.py",
#     "verbosity": 1
# }


#-----------------------------------------------------------------------------------
class TestXXX(unittest.TestCase):

    def setUp(self):

        notr_files_path = os.path.join(sublime.packages_path(), 'Notr', 'files')

        mock_settings = {
            "projects": [],
            "sort_tags_alpha": True,
            "mru_size": 5,
            "fixed_hl_whole_word": True,
            "section_marker_size": 1,
        }
        sublime.load_settings = MagicMock(return_value=mock_settings)

        # Mock top level entities.
        self.view = sublime.View(10)
        self.window = sublime.Window(20)
        self.view.window = MagicMock(return_value=self.window)

        # Mock syntax interrogation.
        self.syntax = sublime.Syntax('', 'Notr', False, '')
        self.view.syntax = MagicMock(return_value=self.syntax)

    def tearDown(self):
        pass

    # @unittest.skip('')
    def test_parsing(self):
        ''' Tests the .ntr file parsing. '''

        # notr._process_notr_files()
        # for e in notr._parse_errors:
        #     print(f'parse error:{e}')

        # evt = notr.NotrEvent()
        # evt.on_init([self.view])

        # self.assertEqual(len(notr._tags), 7)
        # self.assertEqual(len(notr._links), 6)
        # self.assertEqual(len(notr._refs), 6)
        # self.assertEqual(len(notr._sections), 13)
        # self.assertEqual(len(notr._parse_errors), 0)

    # @unittest.skip('')
    # def test_GotoRef(self):
    #     cmd = notr.NotrGotoTargetCommand(self.view)
    #     cmd.run(None, False)

    # @unittest.skip('')
    # def test_InsertRef(self):
    #     cmd = notr.NotrInsertRefCommand(self.view)
    #     edit = sublime.Edit
    #     cmd.run(edit)


# #-----------------------------------------------------------------------------------
# if __name__ == '__main__':
#     # https://docs.python.org/3/library/unittest.html#unittest.main
#     tp = unittest.main(verbosity=2, exit=False)
#     print(tp.result)
