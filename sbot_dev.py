import sys
import os
import subprocess
import platform
import traceback
import datetime
import importlib
import sublime
import sublime_plugin
from .SbotCommon import common as sc
from .SbotCommon import logger as log
# from .SbotCommon import tracer as tr
from . import test_tracer as tt

# from .SbotCommon.tracer import *
# import .SbotCommon.tracer
# importlib.reload(tracer)


print(f'>>> (re)load {__name__}')
importlib.reload(sc)
importlib.reload(log)
importlib.reload(tt)

# Initialize logging.
log.init(sc.get_store_fn('sbot.log'))


# TODO1 SbotCommon README.md Finish/clean. Maybe move test_tracer.py here and document the file and the output.
# TODO production (not DEBUG) disables all tracing and sets log level to > debug.




#------------------- Dev stuff ----------------------
# Clean dump file.
_dump_fn = os.path.join(os.path.dirname(__file__), '_dump.log')
with open(_dump_fn, 'w'):
    pass

# Write dump file.
def _dump(txt):
    with open(_dump_fn, 'a') as f:
        f.write(txt + '\n')
        f.flush()


# # Stuff like this works:
# ff = sc.expand_vars
# s9 = ff('I am $USERNAME')
# print('>>>', s9)

# globals() — The dictionary of the current module.
# _dump(f'### globals of {__name__}:\n{globals()}')
# print(f'### dir of {__name__}:\n{sys.modules[__name__]}')


#------------------- Real stuff ----------------------

DEV_SETTINGS_FILE = "SbotDev.sublime-settings"


#-----------------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    log.info(f'Loading {__package__} with python {platform.python_version()} on {platform.platform()}')


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    '''Ditto.'''
    # log.info(f'Unloading {__package__}')
    pass


#-----------------------------------------------------------------------------------
class DevEvent(sublime_plugin.EventListener):
    ''' General listener. https://www.sublimetext.com/docs/api_reference.html#sublime_plugin.EventListener '''

    def on_init(self, views):
        ''' Called once with a list of views that were loaded before the EventListener was instantiated. '''
        # First thing that happens when plugin/window created. Initialize everything.
        settings = sublime.load_settings(DEV_SETTINGS_FILE)

    def on_load(self, view):
        ''' Called when the file is finished loading. '''
        # Open logfile at end of file - option. https://forum.sublimetext.com/t/move-up-or-down-by-n-lines/42193/3
        if view.file_name() is not None and 'sbot.log' in view.file_name():
            # view.run_command("move_to", {"to": "eof"})
            view.show_at_center(view.size())

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
        print(f'on_hover_done:{sel}')


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit, what):
        if what == 'reload':
            # TODO1 reload imports in subdirs when the file changes
            # This works if imported like from .SbotCommon import utils as sc
            # importlib.reload(sc)
            # This also:
            # import .SbotCommon.tracer
            # importlib.reload(tracer)
            # but this doesn't because the module itself is not imported:
            # from .SbotCommon.tracer import *
            # importlib.reload(tracer)
            pass

        elif what == 'trace':
            from . import test_tracer
            trace_fn = os.path.join(os.path.dirname(__file__), '_tracer.log')
            test_tracer.do_trace_test(trace_fn)
            
        elif what == 'rpdb':
            print('>>> Before running rpdb')
            from . import remote_pdb
            try:
                remote_pdb.RemotePdb(host='127.0.0.1', port=4444).set_trace()
            except Exception as e:
                print(f'>>> RemotePdb exception: {e}')
            print('>>> After running rpdb')

        elif what == 'boom':
            # Blow stuff up. Force unhandled exception.
            log.debug('Forcing unhandled exception!')
            sc.open_path('not-a-real-file')
            # i = 222 / 0

        elif what == 'folding':
            ''' 
            is_folded(region: Region) → bool
            folded_regions() → list[sublime.Region]
            fold(x: Region | list[sublime.Region]) → bool
            unfold(x: Region | list[sublime.Region]) → list[sublime.Region]
            '''
            regions = self.view.folded_regions()
            text = ["folded_regions"]
            for r in regions:
                s = f'region:{r}'
                text.append(s)
            new_view = sc.create_new_view(self.view.window(), '\n'.join(text))


#-----------------------------------------------------------------------------------
class SbotGitCommand(sublime_plugin.TextCommand):

    def run(self, edit, git_cmd):
        ''' Simple git tools: diff, commit (TODO with comment?), push? https://github.com/kemayo/sublime-text-git. '''
        # TODO show previous version.
        fn = self.view.file_name()

        if fn is not None:
            dir, fn = os.path.split(fn)
            if git_cmd == 'diff':
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
        # log.debug('abra')
        directions = ["north", "south", "east", "west", "up", "down", "left", "right"]

        items = []
        for dir in directions:
            items.append(sublime.QuickPanelItem(
                trigger=dir,
                details=["<i>details</i>", "<b>more</b>"],
                annotation=f"look_{dir}",
                kind=(sublime.KIND_ID_COLOR_REDISH + directions.index(dir), dir[:1], '????') ))

        self.window.show_quick_panel(items, self.on_done, on_highlight=self.on_highlight, placeholder="type here")
        # self.window.show_quick_panel(items, self.on_done, flags=sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT, selected_index=2, on_highlight=self.on_highlight, placeholder="place-xxx")

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
        log.debug(f'Got:{text}')


#-----------------------------------------------------------------------------------
class SbotTestVisualsCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super(SbotTestVisualsCommand, self).__init__(view)
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, "my_key")
        self.count = 0

    def run(self, edit):
        ### Phantoms.
        image = os.path.join(sublime.packages_path(), "SbotDev", "felix.jpg")
        img_html = '<img src="file://' + image + '" width="16" height="16">'
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

        ### Annotations.
        regions = []
        anns = []
        for i in range(3):
            p = 1000 + i * 200
            regions.append(sublime.Region(p, p + 20))
            anns.append(f'Annotation=<b>{i}</b>')

        self.view.add_regions(key='dev_region_name', regions=regions, scope='markup.user_hl6',
                              annotations=anns, annotation_color='red',
                              icon='circle', flags=sublime.RegionFlags.DRAW_STIPPLED_UNDERLINE)

    def nav(self, href):
        # href is attribute of the link clicked.
        pass


#-----------------------------------------------------------------------------------
def _notify_exception(type, value, tb):
    '''Process unhandled exceptions and notify user. log full stack.'''
    msg = f'Unhandled exception {type.__name__}: {value}'
    log.error(msg, tb)

    # Show the user some info.
    frame = traceback.extract_tb(tb)[-1]

    info = [msg]
    info.append(f'at {frame.name}({frame.lineno})')
    info.append(f'See the log for detail')
    sublime.error_message('\n'.join(info))  # This goes to console too.


#-----------------------------------------------------------------------------------
#----------------------- Finish initialization -------------------------------------
#-----------------------------------------------------------------------------------

# Connect the last chance hook.
sys.excepthook = _notify_exception
