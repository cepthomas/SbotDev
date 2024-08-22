import sys
import os
import subprocess
import platform
import traceback
import datetime
import importlib
import bdb
import sublime
import sublime_plugin
from . import sbot_common as sc

# Benign reload in case of edited.
importlib.reload(sc)


# TODO1 insert/delete lua dbg() and sbot_pdb.set_trace() from ST.
# TODO1 PRODUCTION flag disables all tracing, sets log level to >= info, disable all sbot_pdb.set_trace().
#   => https://stackoverflow.com/questions/13352677/python-equivalent-for-ifdef-debug



DEV_SETTINGS_FILE = "SbotDev.sublime-settings"


#-----------------------------------------------------------------------------------
# Clean dump file.
_dump_fn = os.path.join(os.path.dirname(__file__), '_dump.log')
with open(_dump_fn, 'w'):
    pass

# Write to dump file.
def _dump(txt):
    with open(_dump_fn, 'a') as f:
        f.write(txt + '\n')
        f.flush()


#-----------------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    sc.info(f'Loading {__package__} with python {platform.python_version()} on {platform.platform()}')


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    '''Called per plugin instance.'''
    # sc.info(f'Unloading {__package__}')
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
        pass


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit, what):
        if what == 'tb':
            _fun_with_traceback()

        elif what == 'boom':
            # Blow stuff up. Force unhandled exception.
            sc.debug('Forcing unhandled exception!')
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
        ''' Simple git tools: diff, commit (TODO with comment?), push.
        TODO show previous version?
        https://github.com/kemayo/sublime-text-git.
        '''
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
def _fun_with_traceback():

    # tb => traceback object.
    # limit => Print up to limit stack trace entries (starting from the invocation point) if limit is positive.
    #   Otherwise, print the last abs(limit) entries. If limit is omitted or None, all entries are printed.
    # f => optional argument can be used to specify an alternate stack frame to start. Otherwise uses current.
    # FrameSummary attributes of interest: 'filename', 'line', 'lineno', 'locals', 'name'.

    # [FrameSummary] traceback.extract_tb(tb, limit=None)  Useful for alternate formatting of stack traces.
    # [FrameSummary] traceback.extract_stack(f=None, limit=None)  Extract the raw traceback from the current stack frame.
    # [string] traceback.format_list([FrameSummary])  Kind of ugly printable format with dangling newlines.
    # [string] traceback.format_tb(tb, limit=None)  A shorthand for format_list(extract_tb(tb, limit)).
    # [string] traceback.format_stack(f=None, limit=None)  A shorthand for format_list(extract_stack(f, limit)).

    def my_frame_formatter(frame):
        return(f'file:{frame.filename} func:{frame.name} lineno:{frame.lineno} line:{frame.line}')

    # Get most recent frame => traceback.extract_tb(tb)[:-1], traceback.extract_stack()[:-1]

    _dump('====== Dump a stack - most recent last')
    for f in traceback.extract_stack():
        _dump(my_frame_formatter(f))

    _dump('====== Dump a traceback - most recent last')
    try:
        1 / 0
    except Exception as e:
        for f in traceback.extract_tb(e.__traceback__):
            _dump(my_frame_formatter(f))

    _dump('====== Dump stack detail using sys._getframe()')
    stkpos = 0
    buff = []
    try:
        while True:
            frame = sys._getframe(stkpos)
            code = frame.f_code
            buff.append(f'>>> stkpos:{stkpos}')
            buff.append(f'    file:{code.co_filename}')
            # buff.append(f'    frame.f_locals:{frame.f_locals}')
            buff.append(f'    lineno:{frame.f_lineno}')
            buff.append(f'    first lineno:{code.co_firstlineno}')
            buff.append(f'    argcount:{code.co_argcount}')
            # buff.append(f'    co_consts:{code.co_consts}')
            if 'self' in frame.f_locals:
                buff.append(f'    class:{frame.f_locals["self"].__class__.__name__}')
            buff.append(f'    func:{code.co_name}')
            # buff.append(f'    co_names:{code.co_names}')
            buff.append(f'    varnames:{code.co_varnames}')
            # co_cellvars = ()
            # co_freevars = ()
            # co_kwonlyargcount = 0
            # co_posonlyargcount = 0
            # co_nlocals = 5
            # co_stacksize = 6

            stkpos += 1
    except:
        # End of stack.
        _dump('\n'.join(buff))
        pass


#-----------------------------------------------------------------------------------
def _notify_exception(type, value, tb):
    '''
    Process unhandled exceptions. This catches for all current plugins and is mainly
    used for debugging the sbot pantheon. Logs the full stack and pops up a message box
    with summary.
    '''

    # Sometimes gets this on shutdown: FileNotFoundError '...Log\plugin_host-3.8-on_exit.log'
    if issubclass(type, FileNotFoundError) and 'plugin_host-3.8-on_exit.log' in str(value):
        sys.__excepthook__(type, value, traceback)
        return

    # This happens with hard shutdown of SbotPdb.
    if issubclass(type, bdb.BdbQuit):
        sys.__excepthook__(type, value, traceback)
        return

    msg = f'Unhandled exception {type.__name__}: {value}'
    sc.error(msg, tb)

    # Show the user some context info.
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
