import sys
import os
import subprocess
import platform
import sublime
import sublime_plugin
from . import sbot_common as sc

from . import remote_pdb

# { "keys": ["ctrl+k", "n"], "command": "sublime_linter_goto_error", },
# { "keys": ["ctrl+k", "p"], "command": "sublime_linter_goto_error",

DEV_SETTINGS_FILE = "SbotDev.sublime-settings"


#-----------------------------------------------------------------------------------
def plugin_loaded():
    ''' Called once per plugin instance. '''
    pass


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    ''' Called once per plugin instance. '''
    pass



class SomeClass(object):

    # def __new__(cls, arg1):
    #     # Called to create a new instance of class cls. __new__() is a static method (special-cased so you need not
    #     # declare it as such) that takes the class of which an instance was requested as its first argument.
    #     # The remaining arguments are those passed to the object constructor expression (the call to the class).
    #     # The return value of __new__() should be the new object instance (usually an instance of cls).
    #     print(f'new')

    def __init__(self, arg1):
        # Called after the instance has been created (by __new__()), but before it is returned to the caller.
        # If a base class has an __init__() method, the derived class’s __init__() method, if any, must explicitly
        # call it to ensure proper initialization of the base class part of the instance; for example: super().__init__([args...]).

        # Get caller info.
        frame = sys._getframe(1)
        fn = os.path.basename(frame.f_code.co_filename)
        line = frame.f_lineno
        func = {frame.f_code.co_name}
        # f'mod_name = {frame.f_globals["__name__"]}'
        # f'class_name = {frame.f_locals["self"].__class__.__name__}'

        self.function = func


        print(f'enter {self.function}')

    # Called when the instance is “called” as a function;
    # if this method is defined, x(arg1, arg2, ...) roughly translates to type(x).__call__(x, arg1, ...).
    def __call__(self, a1, a2):
        print(f'call({a1},{a2})')
        pass

    def __del__(self):
        # Called when the instance is about to be destroyed. This is also called a finalizer or (improperly) a destructor.
        # If a base class has a __del__() method, the derived class’s __del__() method, if any, must explicitly call
        # it to ensure proper deletion of the base class part of the instance.
        #  Due to the precarious circumstances under which __del__() methods are invoked, exceptions that occur during
        # their execution are ignored, and a warning is printed to sys.stderr instead. 
        print(f'exit {self.function}')


    ####################################################### 
    # https://www.pythonlikeyoumeanit.com/Module4_OOP/Special_Methods.html
    # https://docs.python.org/3/reference/datamodel.html#special-method-names

    # Called by the repr() built-in function to compute the “official” string representation of an object.
    # If at all possible, this should look like a valid Python expression that could be used to recreate an object
    # with the same value (given an appropriate environment).
    # repr(x) invokes x.__repr__(), this is also invoked when an object is returned by a console
    def __repr__(self):
        return 'aaaaa'

    # Returns string representation of an object.
    # This method differs from object.__repr__() in that there is no expectation that __str__() return a valid
    # Python expression: a more convenient or concise representation can be used.
    def __str__(self):
        return 'bbbbb'

    def __format__(self, format_spec):
        return 'ccccc'

    def __hash__(self):
        return 999

    # Also Mathematical/Comparison Operators, Container-Like Class

    # def __getitem__(self, key):
    # def __pow__(self, other):
    # object.__getattr__(self, name) etc
    # object.__len__(self)
    # object.__contains__(self, item)


class _context(object):

    def __init__(self, arg1):
        # Get caller info.
        # TODO or this way: https://tutor.python.narkive.com/BWnyK2vR/getting-caller-name-without-the-help-of-sys-getframe-1-f-code-co-name
        frame = sys._getframe(1)
        fn = os.path.basename(frame.f_code.co_filename)
        line = frame.f_lineno
        func = {frame.f_code.co_name}  # 'run'
        mod_name = {frame.f_globals['__name__']}  # 'SbotDev.sbot_dev'

        if 'self' in frame.f_locals:
            class_name = {frame.f_locals['self'].__class__.__name__}  # 'SbotDebugCommand'
        else:
            class_name = 'just a func'

        print(f'mod_name: {mod_name}')
        print(f'class_name: {class_name}')

        self.function = func
        print(f'enter {self.function}')

    def __call__(self, a1, a2):
        print(f'call({a1},{a2})')
        pass

    def __del__(self):
        print(f'exit {self.function}')

def a_function():
    C = _context(222)
    C('xxx', 'yyy')


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        C = _context(111)
        C('aaa', 'bbb')

        a_function()

        # mod_name: {'SbotDev.sbot_dev'}
        # class_name: {'SbotDebugCommand'}
        # enter {'run'}
        # call(aaa,bbb)
        # mod_name: {'SbotDev.sbot_dev'}
        # class_name: just a func
        # enter {'a_function'}
        # call(xxx,yyy)
        # exit {'a_function'}
        # exit {'run'}



        # do_api(edit)

        # do_folding(self.view)

        # do_boom(self.view)

        # # rpdb
        # print('--- Before running rpdb')
        # try:
        #     remote_pdb.RemotePdb(host='127.0.0.1', port=4444).set_trace()
        # except Exception as e:
        #     print(f'RPDB RemotePdb exception: {e}')
        # print('RPDB After running rpdb')




#-----------------------------------------------------------------------------------
class DevEvent(sublime_plugin.EventListener):
    ''' General listener. '''

    def on_init(self, views):
        ''' First thing that happens when plugin/window created. Initialize everything. '''

        settings = sublime.load_settings(DEV_SETTINGS_FILE)
        # current_project_name = settings.get('current_project_name')
        # projects = settings.get('projects')
        # project = None

        # for p in projects:
        #     print(p)
        #     if p["name"] == current_project_name:
        #         project = p
        #         break
        # print(">>>", p)


        sc.set_log_level(sc.LL_DEBUG)
        sc.log_debug(f'Starting up with python {platform.python_version()} on {platform.platform()}')
        # _logger.setLevel(logging.DEBUG)
        # sc.log_debug(f'Starting up with python {platform.python_version()} on {platform.platform()}')

    def on_selection_modified(self, view):
        pass

    def on_query_completions(self, view, prefix, locations):  # suppress too many offerings?
        '''
        These are cryptic, hard to configure correctly. See also associated settings.
        on_query_completions(view: View, prefix: str, locations: List[Point]) 
                   -> Union[None, List[CompletionValue], Tuple[List[CompletionValue], AutoCompleteFlags], CompletionList]
        https://forum.sublimetext.com/t/annoying-autocomplete-c/59082
        https://forum.sublimetext.com/t/how-to-stop-tab-auto-complete-on-4126/63222/2
        '''
        return ([], 0)
        # return ([], sublime.INHIBIT_WORD_COMPLETIONS)

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

    # def on_hover_done(self, sel):
    #     print(f'+++ on_hover_done:{sel}')

    # Open logfile at end of file - option. https://forum.sublimetext.com/t/move-up-or-down-by-n-lines/42193/3
    def on_load(self, view):
        if view.file_name() is not None and 'sbot.log' in view.file_name():
            # view.run_command("move_to", {"to": "eof"})
            view.show_at_center(view.size())


#-----------------------------------------------------------------------------------
class SbotGitCommand(sublime_plugin.TextCommand):

    def run(self, edit, git_cmd):
        ''' Simple git tools: diff, commit, push? https://github.com/kemayo/sublime-text-git. '''

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
            text.append(f'+++ returncode:{cp.returncode}')
        if len(cp.stdout) > 0:
            text.append('+++ stdout')
            text.append(f'{cp.stdout}')
        if len(cp.stderr) > 0:
            text.append('+++ stderr')
            text.append(f'{cp.stderr}')
        new_view = sc.create_new_view(self.view.window(), '\n'.join(text))
        if is_diff:
            new_view.assign_syntax('Packages/Diff/Diff.sublime-syntax')

    def is_visible(self):
        return True
        # return self.view.settings().get('syntax') == 'Packages/Markdown/Markdown.sublime-syntax'


#-----------------------------------------------------------------------------------
class SbotTestPanelCommand(sublime_plugin.WindowCommand):

    def run(self):

        # sc.log_debug('abra')
        directions = ["north", "south", "east", "west", "up", "down", "left", "right"]
        # KIND_ID_AMBIGUOUS = 0
        # KIND_ID_KEYWORD = 1
        # KIND_ID_TYPE = 2
        # KIND_ID_FUNCTION = 3
        # KIND_ID_NAMESPACE = 4
        # KIND_ID_NAVIGATION = 5
        # KIND_ID_MARKUP = 6
        # KIND_ID_VARIABLE = 7
        # KIND_ID_SNIPPET = 8
        # KIND_ID_COLOR_REDISH = 9
        # KIND_ID_COLOR_ORANGISH = 10
        # KIND_ID_COLOR_YELLOWISH = 11
        # KIND_ID_COLOR_GREENISH = 12
        # KIND_ID_COLOR_CYANISH = 13
        # KIND_ID_COLOR_BLUISH = 14
        # KIND_ID_COLOR_PURPLISH = 15
        # KIND_ID_COLOR_PINKISH = 16
        # KIND_ID_COLOR_DARK = 17
        # KIND_ID_COLOR_LIGHT = 18

        items = []
        for dir in directions:
            items.append(sublime.QuickPanelItem(
                trigger=dir,
                details=["<i>details</i>", "<b>more</b>"],
                annotation=f"look_{dir}",
                kind=(sublime.KIND_ID_COLOR_REDISH + directions.index(dir), dir[:1], '????') ))
            # trigger - A unicode string of the text to match against the user's input.
            # details - An optional unicode string, or list of unicode strings, containing limited inline HTML. Displayed below the trigger.
            # annotation - An optional unicode string of a hint to draw to the right-hand side of the row.
            # kind - An optional kind tuple – defaults to sublime.KIND_AMBIGUOUS. Otherwise KIND_KEYWORD, etc.

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
        sc.log_debug(f'Got:{text}')


#-----------------------------------------------------------------------------------
class SbotTestVisualsCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super(SbotTestVisualsCommand, self).__init__(view)
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, "my_key")
        self.count = 0

    def run(self, edit):
        # Phantoms.
        image = os.path.join(sublime.packages_path(), "SbotDev", "felix.jpg")
        img_html = '<img src="file://' + image + '" width="16" height="16">'

        # Old way works too:
        # self.view.erase_phantoms("test")
        # for sel in self.view.sel():
        #     self.view.add_phantom ("test", sel, img_html, sublime.LAYOUT_BLOCK)

        # Clean first. Note - phantoms need to be managed externally rather than instantiate each time cmd is loaded.
        phantoms = []
        self.phantom_set.update(phantoms)

        # sublime.LAYOUT_INLINE: Display in between the region and the point following.
        # sublime.LAYOUT_BELOW: Display in space below the current line, left-aligned with the region.
        # sublime.LAYOUT_BLOCK: Display in space below the current line, left-aligned with the beginning of the line.

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

        # Annotations.
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
        # href attribute of the link clicked.
        pass


#-----------------------------------------------------------------------------------
def do_boom(view):

    # Blow stuff up.
    bing = bong
    x = 1 / 0

    # Force a handled exception.
    sc.log_debug('Forcing handled exception!')
    sc.start_file('not-a-real-file')

    # Force an unhandled exception.
    sc.log_debug('Forcing unhandled exception!')
    i = 222 / 0

    # ### stack stuff
    # # Get stackframe info. This is supposedly the fastest way. https://gist.github.com/JettJones/c236494013f22723c1822126df944b12.
    # frame = sys._getframe(0)
    # fn = os.path.basename(frame.f_code.co_filename)
    # func = frame.f_code.co_name
    # line = frame.f_lineno

    # dump_attrs(frame)
    # # >>> f_back, f_builtins, f_code, f_globals, f_lasti, f_lineno, f_locals, f_trace, f_trace_lines, f_trace_opcodes, False
    # dump_attrs(frame.f_code)
    # # >>> co_argcount, co_cellvars, co_code, co_consts, co_filename, co_firstlineno, co_flags, co_freevars, co_kwonlyargcount,
    # #    co_lnotab, co_name, co_names, co_nlocals, co_posonlyargcount, co_stacksize, co_varnames


#-----------------------------------------------------------------------------------
def do_folding(view):

    ''' View
    is_folded(region: Region) → bool
    Returns: Whether the provided Region is folded.

    folded_regions() → list[sublime.Region]
    Returns: The list of folded regions.

    fold(x: Region | list[sublime.Region]) → bool
    Fold the provided Region(s).
    Returns: False if the regions were already folded.

    unfold(x: Region | list[sublime.Region]) → list[sublime.Region]
    Unfold all text in the provided Region(s).
    Returns: The unfolded regions.
    '''

    regions = view.folded_regions()
    text = ["folded_regions"]
    for r in regions:
        s = f'region:{r}'
        text.append(s)
    new_view = sc.create_new_view(view.window(), '\n'.join(text))


#-----------------------------------------------------------------------------------
def do_api(edit):
    ##### Probing ST api.

    # from inspect import getmembers, isfunction
    # # from my_project import my_module
    # functions_list = getmembers(sublime_api)#, isfunction)
    # for f in functions_list:
    #     print(f'{f[0]}:   ')
    # return    

    # # https://stackoverflow.com/questions/218616/how-to-get-method-parameter-names
    # for a in dir(sublime_api):
    #     print(f'{a}:')
    # return

    ### Normal usage.
    view = sc.create_new_view(sublime.active_window(), '012 3456\n789\nUUUU YYYY')
    pt = 3
    reg = sublime.Region(5, 8)

    ret = view.rowcol(12)
    sc.log_debug(f'>0> {ret}')  # (1, 3)
    ret = view.text_point(2, 4)
    sc.log_debug(f'>0> {ret}')  # 17
    ret = view.find('78', 5)
    sc.log_debug(f'>0> {ret}')  # (9, 11)
    ret = view.substr(11)
    sc.log_debug(f'>0> |{len(ret)}|{ret[0]}|{ret}|')  # |1|9|9|
    ret = view.word(13)
    sc.log_debug(f'>0> {ret}|{view.substr(ret)}|')  # (13, 17)|UUUU|
    ret = view.line(3)
    sc.log_debug(f'>0> {ret}|{view.substr(ret)}|')  # (0, 8)|012 3456|
    ret = view.full_line(12)
    sc.log_debug(f'>0> {ret}|{view.substr(ret)}|')  # (9, 13)|789

    ### Empty buffer.
    view = sc.create_new_view(sublime.active_window(), '')
    pt = 0
    reg = sublime.Region(pt, pt)

    ret = view.rowcol(pt)
    sc.log_debug(f'>1> {ret}')  # (0, 0)
    ret = view.text_point(pt, pt)
    sc.log_debug(f'>1> {ret}')  # 0
    ret = view.split_by_newlines(reg)
    sc.log_debug(f'>1> {ret}')  # [Region(0, 0)] ???
    ret = view.find('pattern', pt)
    sc.log_debug(f'>1> {ret}')  # (-1, -1)
    ret = view.substr(pt)
    sc.log_debug(f'>1> |{len(ret)}|{ret[0]}|{ret}|')  # |1|2023-06-24 09:13:37.992 DBG sbot_dev.py:144 >1> (0, 0)||
    ret = view.word(pt)
    sc.log_debug(f'>1> {ret}|{view.substr(ret)}|')  # nada - see previous
    ret = view.line(pt)
    sc.log_debug(f'>1> {ret}|{view.substr(ret)}|')  # (0, 0)
    ret = view.full_line(pt)
    sc.log_debug(f'>1> {ret}|{view.substr(ret)}|')  # (0, 0)
    
    return

    ### Outside legal range.
    view = sc.create_new_view(sublime.active_window(), 'ABCDEFGHIJ')
    pt = 10000
    reg = sublime.Region(pt, pt + 1)

    ret = view.rowcol(pt)
    sc.log_debug(f'>2> {ret}')  # (0, 10)
    ret = view.text_point(pt, pt)
    sc.log_debug(f'>2> {ret}')  # 10
    ret = view.insert(edit, pt, 'booga')
    sc.log_debug(f'>2> {ret}')  # 0
    ret = view.replace(edit, reg, 'xyzzy')
    sc.log_debug(f'>2> {ret}')  # None
    ret = view.split_by_newlines(reg)
    sc.log_debug(f'>2> {ret}')  # [Region(10, 10)]
    ret = view.find('pattern', pt)
    sc.log_debug(f'>2> {ret}')  # (-1, -1)
    ret = view.substr(pt)
    sc.log_debug(f'>2> |{len(ret)}|{ret[0]}|{ret}|')  # |1|2023-06-24 09:06:19.561 DBG sbot_dev.py:175 >2> (10000, 10000)||
    ret = view.word(pt)
    sc.log_debug(f'>2> {ret}|{view.substr(ret)}|')  # nada - see previous
    ret = view.line(pt)
    sc.log_debug(f'>2> {ret}|{view.substr(ret)}|')  # (9990, 10000)||
    ret = view.full_line(pt)
    sc.log_debug(f'>2> {ret}|{view.substr(ret)}|')  # (9990, 10000)||


#-----------------------------------------------------------------------------------
def dump_stack(cat):
    ''' Diagnostics. '''
    depth = 0
    try:
        while True:
            frame = sys._getframe(depth)
            fn = os.path.basename(frame.f_code.co_filename)
            func = frame.f_code.co_name

            # smsg = f'{cat}{depth} __name__:{frame.f_globals["__name__"]} FILE:{fn}  LINE:{frame.f_lineno}  FUNCTION:{frame.f_code.co_name}'
            smsg = f'{cat}{depth} FU:{func} FILE:{fn} LINE:{frame.f_lineno}  '
            print(smsg)
            depth += 1
    except:
        # End of stack.
        return


#-----------------------------------------------------------------------------------
def dump_attrs(obj):
    ''' Diagnostics. '''
    for attr in dir(obj):
        print(f'{attr} = {getattr(obj, attr)}')
