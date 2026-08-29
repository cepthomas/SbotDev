import sys
import os
import subprocess
import platform
import traceback
import bdb
import datetime
import string
import re
import importlib
import socket
import random
import pathlib
import time
import sublime
import sublime_plugin
from . import sbot_common as sc


#-----------------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    sc.debug(f'plugin_loaded {__package__} with python {platform.python_version()} on {platform.platform()}')


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    '''Called per plugin instance.'''
    sc.info(f'plugin_unloaded {__package__}')


#-----------------------------------------------------------------------------------
class DevEvent(sublime_plugin.EventListener):
    ''' General listener. https://www.sublimetext.com/docs/api_reference.html#sublime_plugin.EventListener '''

    hostname = socket.gethostname()

    def on_init(self, views):
        ''' Called once with a list of views that were loaded before the EventListener was instantiated. '''
        # First thing that happens when plugin/window created. Initialize everything.
        pass

    def on_load(self, view):
        ''' Called when the file is finished loading. '''
        # Open logfile at end of file - option. https://forum.sublimetext.com/t/move-up-or-down-by-n-lines/42193/3
        if view.file_name() is not None and 'sbot.log' in view.file_name():
            # view.run_command("move_to", {"to": "eof"})
            view.show_at_center(view.size())

        # Adjust font size based on host.
        if self.hostname in ("host1", "host1.example.com", "host2"):
            view.settings().set("font_size", 20)

    def on_query_completions(self, view, prefix, locations):
        '''
        These are cryptic, hard to configure correctly. See also associated settings.
        on_query_completions(view: View, prefix: str, locations: List[Point])
                   -> Union[None, List[CompletionValue], Tuple[List[CompletionValue], AutoCompleteFlags], CompletionList]
        https://forum.sublimetext.com/t/annoying-autocomplete-c/59082
        https://forum.sublimetext.com/t/how-to-stop-tab-auto-complete-on-4126/63222/2
        '''
        # suppress too many offerings?
        # return ([], sublime.INHIBIT_WORD_COMPLETIONS)
        return ([], 0)

    def on_hover(self, view, point, hover_zone):
        # point - The closest point in the view to the mouse location. The mouse may not actually be located adjacent based on the value of hover_zone:
        #    TEXT = 1 The mouse is hovered over the text.
        #    GUTTER = 2 The mouse is hovered over the gutter.
        #    MARGIN = 3 The mouse is hovered in the white space to the right of a line.
        items = ['ietm1', 'item2', 'item3', 'item4']
        # view.show_popup_menu(items, self.on_hover_done)
        #   Show a popup menu at the caret, for selecting an item in a list.
        # show_popup(content: str, flags=PopupFlags.NONE, location: Point=-1, max_width: DIP=320,
        #   max_height: DIP=240, on_navigate:=None, on_hide:=None)
        #   Show a popup displaying HTML content.

    def on_hover_done(self, sel):
        pass

    def on_exit(self):
        # Called once after the API has shut down, immediately before the plugin_host process exits
        sc.info(f'on_exit {__package__}')


#-----------------------------------------------------------------------------------
class SbotGitCommand(sublime_plugin.TextCommand):

    def run(self, edit, git_cmd):
        ''' Simple git tools: status, diff, commit (no comment), push.
        https://github.com/kemayo/sublime-text-git.
        '''
        fn = self.view.file_name()

        if fn is not None:
            dir, fn = os.path.split(fn)
            if git_cmd == 'status':
                cmd = f'git status "{dir}"'
                cp = subprocess.run(cmd, cwd=dir, universal_newlines=True, capture_output=True, text=True, shell=True)
                self.proc_ret(cp, is_diff=True)

            elif git_cmd == 'diff':
                cmd = f'git diff "{fn}"'
                cp = subprocess.run(cmd, cwd=dir, universal_newlines=True, capture_output=True, text=True, shell=True)
                self.proc_ret(cp, is_diff=True)

            elif git_cmd == 'commit':
                msg = 'WIP.'
                # git commit --dry-run -a -m <msg> [<pathspec>]
                cmd = f'git commit -m "{msg}" {fn}'
                cp = subprocess.run(cmd, cwd=dir, universal_newlines=True, capture_output=True, text=True, shell=True)
                self.proc_ret(cp)

            elif git_cmd == 'push':
                cmd = 'git push'
                cp = subprocess.run(cmd, cwd=dir, universal_newlines=True, capture_output=True, text=True, shell=True)
                self.proc_ret(cp)

    def proc_ret(self, cp, is_diff=False):
        ''' Common process output handling  cp: the CompletedProcess, Note git writes some non-error stuff to stderr. '''
        text = []
        text.append(f'args:{cp.args}')
        text.append('')

        if cp.returncode != 0:
            text.append(f'GIT returncode:{cp.returncode}')
        if len(cp.stdout) > 0:
            text.append('GIT stdout')
            text.append(f'{cp.stdout}')
        if len(cp.stderr) > 0:
            text.append('GIT stderr')
            text.append(f'{cp.stderr}')
        new_view = sc.create_new_view(self.view.window(), '\n'.join(text))
        if is_diff:
            new_view.assign_syntax('Packages/Diff/Diff.sublime-syntax')

    def is_visible(self):
        # Could test for .git folder.
        return True


#-----------------------------------------------------------------------------------
class SbotTestPanelCommand(sublime_plugin.WindowCommand):

    def run(self):
        # self.one_way()
        self.another_way()

    def one_way(self):
        directions = ["north", "south", "east", "west", "up", "down", "left", "right"]
        items = []
        for dir in directions:
            items.append(sublime.QuickPanelItem(
                trigger=dir,
                details="<i>details</i><b>more</b>",
                annotation=f"look_{dir}",
                kind=(sublime.KIND_ID_COLOR_REDISH + directions.index(dir), dir[:1], '????') ))

        self.window.show_quick_panel(items, self.on_done, on_highlight=self.on_highlight, placeholder="type here")
        # self.window.show_quick_panel(items, self.on_done, flags=sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT, selected_index=2, on_highlight=self.on_highlight, placeholder="place-xxx")

    def another_way(self):
        items = []

        items.append(sublime.QuickPanelItem(trigger='COLOR_REDISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_REDISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_ORANGISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_ORANGISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_YELLOWISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_YELLOWISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_GREENISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_GREENISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_CYANISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_CYANISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_BLUISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_BLUISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_PURPLISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_PURPLISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_PINKISH', annotation='==> annotation', kind=(sublime.KindId.COLOR_PINKISH, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_DARK', annotation='==> annotation', kind=(sublime.KindId.COLOR_DARK, 'X', '???')))
        items.append(sublime.QuickPanelItem(trigger='COLOR_LIGHT', annotation='==> annotation', kind=(sublime.KindId.COLOR_LIGHT, 'X', '???')))

        # items.append(sublime.QuickPanelItem(trigger='AMBIGUOUS', annotation='==> annotation', kind=(sublime.KindId.AMBIGUOUS, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='KEYWORD', annotation='==> annotation', kind=(sublime.KindId.KEYWORD, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='TYPE', annotation='==> annotation', kind=(sublime.KindId.TYPE, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='FUNCTION', annotation='==> annotation', kind=(sublime.KindId.FUNCTION, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='NAMESPACE', annotation='==> annotation', kind=(sublime.KindId.NAMESPACE, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='NAVIGATION', annotation='==> annotation', kind=(sublime.KindId.NAVIGATION, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='MARKUP', annotation='==> annotation', kind=(sublime.KindId.MARKUP, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='VARIABLE', annotation='==> annotation', kind=(sublime.KindId.VARIABLE, 'X', '???')))
        # items.append(sublime.QuickPanelItem(trigger='SNIPPET', annotation='==> annotation', kind=(sublime.KindId.SNIPPET, 'X', '???')))

        self.window.show_quick_panel(items, self.on_done, on_highlight=self.on_highlight, placeholder="type here")

    def on_done(self, *args, **kwargs):
        sel = args[0]

    def on_highlight(self, *args, **kwargs):
        hlt = args[0]


#-----------------------------------------------------------------------------------
class SbotTestPanelInputCommand(sublime_plugin.WindowCommand):

    def run(self):
        # Bottom input area.
        self.window.show_input_panel(self.window.extract_variables()['folder'] + '>', "", self.on_done, None, None)

    def on_done(self, text):
        sc.create_new_view(self.window, text)
        sc.debug(f'Got:{text}')


#-----------------------------------------------------------------------------------
class SbotTestVisualsCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super(SbotTestVisualsCommand, self).__init__(view)
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, "my_key")
        self.count = 0

    def run(self, edit):
        ### Phantoms.
        image = os.path.join(sublime.packages_path(), "SbotDev", "felix200.jpg")
        img_html = '<img src="file://' + image + '" width="32" height="32">'
        # Old way works too:
        # self.view.erase_phantoms("test")
        # for sel in self.view.sel():
        #     self.view.add_phantom ("test", sel, img_html, sublime.LAYOUT_BLOCK)

        # Clean first. Note - phantoms need to be managed externally rather than instantiate each time cmd is loaded.
        phantoms = []
        self.phantom_set.update(phantoms)

        html = f'<div>|image LAYOUT_INLINE at 200:210|{img_html}|</div>'
        region = sublime.Region(200, 210)
        phantom = sublime.Phantom(region, html, sublime.LAYOUT_INLINE)
        phantoms.append(phantom)

        html = f'<div>|image LAYOUT_BELOW at 400:410|{img_html}|</div>'
        region = sublime.Region(400, 410)
        phantom = sublime.Phantom(region, html, sublime.LAYOUT_BELOW)
        phantoms.append(phantom)

        html = f'<div>|image LAYOUT_BLOCK at 600:610|{img_html}|</div>'
        region = sublime.Region(600, 610)
        phantom = sublime.Phantom(region, html, sublime.LAYOUT_BLOCK)
        phantoms.append(phantom)

        href = "https://www.sublimetext.com/docs/api_reference.html"
        href = "abcdef12345"

        html = f'<div><a href="{href}">|href LAYOUT_BLOCK at 800:810|</a></div>'
        region = sublime.Region(800, 810)
        phantom = sublime.Phantom(region, html, sublime.LAYOUT_BLOCK, self.nav)
        phantoms.append(phantom)

        self.phantom_set.update(phantoms)

        ### Coloring, annotations, icons.
        regions = []
        anns = []
        for i in range(3):
            p = 1000 + i * 200
            regions.append(sublime.Region(p, p + 5)) # color range
            anns.append(f'Annotation=<b>{i}</b>')

        self.view.add_regions(key='dev_region_name', regions=regions, scope='markup.user_hl6', # color = cyan
                              annotations=anns, annotation_color='red',
                              icon='circle', flags=sublime.RegionFlags.DRAW_STIPPLED_UNDERLINE)

    def nav(self, href):
        # href is attribute of the link clicked.
        pass


#-----------------------------------------------------------------------------------
from functools import partial
from mmap import ACCESS_READ, mmap
def _bin_stuff():
    # https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte

    BUFF_SIZE = 4096
    LINE_SIZE = 16
    # A mebibyte (MiB) is equal to 1,048,576 bytes (1,024 × 1,024), or 1,024 kibibytes.
    BIN_FILE_NAME = os.path.join(os.path.dirname(__file__), 'tests', 'mebibyte.bin')
    BIN_FILE_SIZE = 2**20

    def dummy_byte_op(b):
        x = b

    def file_byte_iterator(path):
        ''' Return an iterator over the path/file that lazily loads the file.'''
        with open(BIN_FILE_NAME, "rb") as f:
            reader = partial(f.read1, BUFF_SIZE)
            file_iterator = iter(reader, bytes())
            for chunk in file_iterator:
                yield from chunk

    # def test_byte_by_byte():
    with open(BIN_FILE_NAME, "rb") as f:
        while (b := f.read(1)):
            dummy_byte_op(b)

    # def test_line_by_line()/:
    with open(BIN_FILE_NAME, "rb") as f:
        while (bs := f.read(LINE_SIZE)):
            for b in bs:
                dummy_byte_op(b)

    # def test_by_buff():
    with open(BIN_FILE_NAME, "rb") as f:
        while (bs := f.read(BUFF_SIZE)):
            for b in bs:
                dummy_byte_op(b)

    # def test_by_whole():
    with open(BIN_FILE_NAME, "rb") as f:
        bs = f.read()
        for b in bs:
            dummy_byte_op(b)

    # def test_by_read1_list():
    # Load into list.
    l = list(file_byte_iterator(BIN_FILE_NAME))
    for b in l:
        dummy_byte_op(b)

    # def test_by_read1_iterator():
    # Direct iterator access.
    for b in file_byte_iterator(BIN_FILE_NAME):
        dummy_byte_op(b)

    # def test_by_mmap():
    with open(BIN_FILE_NAME, "rb") as f, mmap(f.fileno(), 0, access=ACCESS_READ) as s:
        for b in s: # length is equal to the current file size
            dummy_byte_op(b)

    # def create_test_file():
    path = BIN_FILE_NAME
    pathobj = pathlib.Path(path)
    pathobj.write_bytes(bytes(random.randint(0, 255) for _ in range(BIN_FILE_SIZE)))

    def do_test(func, func_name):
        start_time = time.perf_counter_ns()
        func()
        print(f'{func_name}: {(time.perf_counter_ns() - start_time) / 1000000}')
