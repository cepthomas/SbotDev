import sys
import os
import subprocess
import platform
import sublime
import sublime_plugin
from . import sbot_common_src as sc


#-----------------------------------------------------------------------------------
def plugin_loaded():
    # print(dir(sbot))
    sc.slog(sc.CAT_DBG, f'Starting up with python {platform.python_version()} on {platform.platform()}')


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    # sc.slog(sc.CAT_DBG, 'sbot_dev plugin_unloaded()')
    pass


#-----------------------------------------------------------------------------------
class SbotAllEvent(sublime_plugin.EventListener):
    ''' General listener. '''

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

    def on_hover_done(self, sel):
        print(f'>>> on_hover_done:{sel}')

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
            text.append(f'>>>> returncode:{cp.returncode}')
        if len(cp.stdout) > 0:
            text.append('>>>> stdout')
            text.append(f'{cp.stdout}')
        if len(cp.stderr) > 0:
            text.append('>>>> stderr')
            text.append(f'{cp.stderr}')
        new_view = sc.create_new_view(self.view.window(), '\n'.join(text))
        if is_diff:
            new_view.assign_syntax('Packages/Diff/Diff.sublime-syntax')

    def is_visible(self):
        return True
        # return self.view.settings().get('syntax') == 'Packages/Markdown/Markdown.sublime-syntax'


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # do_api(edit)

        do_folding(self.view)

        return

        # Force a handled exception.
        sc.slog(sc.CAT_DBG, 'Forcing handled exception!')
        sc.start_file('not-a-real-file')

        # Force an unhandled exception.
        sc.slog(sc.CAT_DBG, 'Forcing unhandled exception!')
        i = 222 / 0

        ### stack stuff
        # Get stackframe info. This is supposedly the fastest way. https://gist.github.com/JettJones/c236494013f22723c1822126df944b12.
        frame = sys._getframe(0)
        fn = os.path.basename(frame.f_code.co_filename)
        func = frame.f_code.co_name
        line = frame.f_lineno

        dump_attrs(frame)
        # >>> f_back, f_builtins, f_code, f_globals, f_lasti, f_lineno, f_locals, f_trace, f_trace_lines, f_trace_opcodes, False
        dump_attrs(frame.f_code)
        # >>> co_argcount, co_cellvars, co_code, co_consts, co_filename, co_firstlineno, co_flags, co_freevars, co_kwonlyargcount,
        #    co_lnotab, co_name, co_names, co_nlocals, co_posonlyargcount, co_stacksize, co_varnames


#-----------------------------------------------------------------------------------
class SbotTestPanelCommand(sublime_plugin.WindowCommand):

    def run(self):
        # sc.slog(sc.CAT_DBG, 'abra')
        directions = ["north", "south", "east", "west"]

        items = []
        for dir in directions:
            items.append(sublime.QuickPanelItem(
                trigger=dir,
                details=["<i>details</i>", "<b>more</b>"],
                annotation=f"look_{dir}",
                kind=sublime.KIND_NAVIGATION))
            # trigger - A unicode string of the text to match against the user's input.
            # details - An optional unicode string, or list of unicode strings, containing limited inline HTML. Displayed below the trigger.
            # annotation - An optional unicode string of a hint to draw to the right-hand side of the row.
            # kind - An optional kind tuple – defaults to sublime.KIND_AMBIGUOUS. Otherwise KIND_KEYWORD, etc.

        self.window.show_quick_panel(items, self.on_done, flags=sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT,
                                     selected_index=2, on_highlight=self.on_highlight, placeholder="place-xxx")

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
        sc.slog(sc.CAT_DBG, f'Got:{text}')


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
    sc.slog(sc.CAT_DBG, f'>0> {ret}')  # (1, 3)
    ret = view.text_point(2, 4)
    sc.slog(sc.CAT_DBG, f'>0> {ret}')  # 17
    ret = view.find('78', 5)
    sc.slog(sc.CAT_DBG, f'>0> {ret}')  # (9, 11)
    ret = view.substr(11)
    sc.slog(sc.CAT_DBG, f'>0> |{len(ret)}|{ret[0]}|{ret}|')  # |1|9|9|
    ret = view.word(13)
    sc.slog(sc.CAT_DBG, f'>0> {ret}|{view.substr(ret)}|')  # (13, 17)|UUUU|
    ret = view.line(3)
    sc.slog(sc.CAT_DBG, f'>0> {ret}|{view.substr(ret)}|')  # (0, 8)|012 3456|
    ret = view.full_line(12)
    sc.slog(sc.CAT_DBG, f'>0> {ret}|{view.substr(ret)}|')  # (9, 13)|789

    ### Empty buffer.
    view = sc.create_new_view(sublime.active_window(), '')
    pt = 0
    reg = sublime.Region(pt, pt)

    ret = view.rowcol(pt)
    sc.slog(sc.CAT_DBG, f'>1> {ret}')  # (0, 0)
    ret = view.text_point(pt, pt)
    sc.slog(sc.CAT_DBG, f'>1> {ret}')  # 0
    ret = view.split_by_newlines(reg)
    sc.slog(sc.CAT_DBG, f'>1> {ret}')  # [Region(0, 0)] ???
    ret = view.find('pattern', pt)
    sc.slog(sc.CAT_DBG, f'>1> {ret}')  # (-1, -1)
    ret = view.substr(pt)
    sc.slog(sc.CAT_DBG, f'>1> |{len(ret)}|{ret[0]}|{ret}|')  # |1|2023-06-24 09:13:37.992 DBG sbot_dev.py:144 >1> (0, 0)||
    ret = view.word(pt)
    sc.slog(sc.CAT_DBG, f'>1> {ret}|{view.substr(ret)}|')  # nada - see previous
    ret = view.line(pt)
    sc.slog(sc.CAT_DBG, f'>1> {ret}|{view.substr(ret)}|')  # (0, 0)
    ret = view.full_line(pt)
    sc.slog(sc.CAT_DBG, f'>1> {ret}|{view.substr(ret)}|')  # (0, 0)
    
    return

    ### Outside legal range.
    view = sc.create_new_view(sublime.active_window(), 'ABCDEFGHIJ')
    pt = 10000
    reg = sublime.Region(pt, pt + 1)

    ret = view.rowcol(pt)
    sc.slog(sc.CAT_DBG, f'>2> {ret}')  # (0, 10)
    ret = view.text_point(pt, pt)
    sc.slog(sc.CAT_DBG, f'>2> {ret}')  # 10
    ret = view.insert(edit, pt, 'booga')
    sc.slog(sc.CAT_DBG, f'>2> {ret}')  # 0
    ret = view.replace(edit, reg, 'xyzzy')
    sc.slog(sc.CAT_DBG, f'>2> {ret}')  # None
    ret = view.split_by_newlines(reg)
    sc.slog(sc.CAT_DBG, f'>2> {ret}')  # [Region(10, 10)]
    ret = view.find('pattern', pt)
    sc.slog(sc.CAT_DBG, f'>2> {ret}')  # (-1, -1)
    ret = view.substr(pt)
    sc.slog(sc.CAT_DBG, f'>2> |{len(ret)}|{ret[0]}|{ret}|')  # |1|2023-06-24 09:06:19.561 DBG sbot_dev.py:175 >2> (10000, 10000)||
    ret = view.word(pt)
    sc.slog(sc.CAT_DBG, f'>2> {ret}|{view.substr(ret)}|')  # nada - see previous
    ret = view.line(pt)
    sc.slog(sc.CAT_DBG, f'>2> {ret}|{view.substr(ret)}|')  # (9990, 10000)||
    ret = view.full_line(pt)
    sc.slog(sc.CAT_DBG, f'>2> {ret}|{view.substr(ret)}|')  # (9990, 10000)||


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
