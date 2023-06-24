import sys
import os
import subprocess
import platform
import inspect
import sublime
import sublime_plugin
import sublime_api
from . import sbot_common_src as sc


#-----------------------------------------------------------------------------------
def plugin_loaded():
    # print(dir(sbot))
    sc.slog(sc.CAT_DBG, f'>>>>>>>>>> Starting up: python {platform.python_version()} on {platform.platform()}')
    # dump_stack()

#-----------------------------------------------------------------------------------
def plugin_unloaded():
    sc.slog(sc.CAT_DBG, 'plugin_unloaded')

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

#-----------------------------------------------------------------------------------
def start_interactive():
    winid = sublime.active_window().id()
    view = sc.create_new_view(sublime.active_window(), '>>> howdy!')
    # slog(sc.CAT_DBG, f'{self.view}  {winid}')
    view.settings().set('interactive' , True)


#-----------------------------------------------------------------------------------
class SbotAllEvent(sublime_plugin.EventListener):
    ''' For tracing EventListener event sequence. '''

    # It appears that ViewEventListener exhibits some uexpected behavior. Safest to stay away from it I think.
    # https://stackoverflow.com/a/50226141

    def on_selection_modified(self, view):
        if view.settings().get('interactive'):
            # sc.slog(sc.CAT_DBG, '+++++++')
            pass

    def on_query_completions(self, view, prefix, locations): # TODO suppress too many offerings.
        return ([], sublime.INHIBIT_WORD_COMPLETIONS)

        # on_query_completions(view: View, prefix: str, locations: List[Point]) 
        #            -> Union[None, List[CompletionValue], Tuple[List[CompletionValue], AutoCompleteFlags], CompletionList]
        # Called whenever completions are to be presented to the user.
        # prefix - The text already typed by the user.
        # locations - The list of points being completed. Since this method is called for all completions no matter the syntax,
        #    self.view.match_selector(point, relevant_scope) should be called to determine if the point is relevant.
        # Returns - A list of completions in one of the valid formats or None if no completions are provided.

        # INHIBIT_WORD_COMPLETIONS = 8
        # Prevent Sublime Text from showing completions based on the contents of the view.
        # INHIBIT_EXPLICIT_COMPLETIONS = 16
        # Prevent Sublime Text from showing completions based on .sublime-completions files.
        # DYNAMIC_COMPLETIONS = 32
        # If completions should be re-queried as the user types.
        # INHIBIT_REORDER = 128
        # Prevent Sublime Text from changing the completion order.


    def on_hover(self, view, point, hover_zone):
        # point - The closest point in the view to the mouse location. The mouse may not actually be located adjacent based on the value of hover_zone.
        # hover_zone:
        # TEXT = 1 The mouse is hovered over the text.
        # GUTTER = 2 The mouse is hovered over the gutter.
        # MARGIN = 3 The mouse is hovered in the white space to the right of a line.        
        items = ['ietm1', 'item2', 'item3', 'item4']
        # view.show_popup_menu(items, self.on_done)

        # show_popup_menu(items: list[str], on_done: Callable[[int], None], flags=0)
        #   Show a popup menu at the caret, for selecting an item in a list.
        # show_popup(content: str, flags=PopupFlags.NONE, location: Point=-1, max_width: DIP=320,
        #   max_height: DIP=240, on_navigate:=None, on_hide:=None)
        #   Show a popup displaying HTML content.

    def on_done(self, sel):
        print(f'>>> {sel}')


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):

    def run(self, edit):

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
        sc.slog(sc.CAT_DBG, f'>0> {ret}') #(1, 3)
        ret = view.text_point(2, 4)
        sc.slog(sc.CAT_DBG, f'>0> {ret}') #17
        ret = view.find('78', 5)
        sc.slog(sc.CAT_DBG, f'>0> {ret}') #(9, 11)
        ret = view.substr(11)
        sc.slog(sc.CAT_DBG, f'>0> |{len(ret)}|{ret[0]}|{ret}|') #|1|9|9|
        ret = view.word(13)
        sc.slog(sc.CAT_DBG, f'>0> {ret}|{view.substr(ret)}|') #(13, 17)|UUUU|
        ret = view.line(3)
        sc.slog(sc.CAT_DBG, f'>0> {ret}|{view.substr(ret)}|') #(0, 8)|012 3456|
        ret = view.full_line(12)
        sc.slog(sc.CAT_DBG, f'>0> {ret}|{view.substr(ret)}|') #(9, 13)|789

        ### Empty buffer.
        view = sc.create_new_view(sublime.active_window(), '')
        pt = 0
        reg = sublime.Region(pt, pt)

        ret = view.rowcol(pt)
        sc.slog(sc.CAT_DBG, f'>1> {ret}') #(0, 0)
        ret = view.text_point(pt, pt)
        sc.slog(sc.CAT_DBG, f'>1> {ret}') #0
        ret = view.split_by_newlines(reg)
        sc.slog(sc.CAT_DBG, f'>1> {ret}') #[Region(0, 0)] ???
        ret = view.find('pattern', pt)
        sc.slog(sc.CAT_DBG, f'>1> {ret}') #(-1, -1)
        ret = view.substr(pt)
        sc.slog(sc.CAT_DBG, f'>1> |{len(ret)}|{ret[0]}|{ret}|') #|1|2023-06-24 09:13:37.992 DBG sbot_dev.py:144 >1> (0, 0)||
        ret = view.word(pt)
        sc.slog(sc.CAT_DBG, f'>1> {ret}|{view.substr(ret)}|') #nada - see previous
        ret = view.line(pt)
        sc.slog(sc.CAT_DBG, f'>1> {ret}|{view.substr(ret)}|') #(0, 0)
        ret = view.full_line(pt)
        sc.slog(sc.CAT_DBG, f'>1> {ret}|{view.substr(ret)}|') #(0, 0)
        # return

        ### Outside legal range.
        view = sc.create_new_view(sublime.active_window(), 'ABCDEFGHIJ')
        pt = 10000
        reg = sublime.Region(pt, pt + 1)

        ret = view.rowcol(pt)
        sc.slog(sc.CAT_DBG, f'>2> {ret}') #(0, 10)
        ret = view.text_point(pt, pt)
        sc.slog(sc.CAT_DBG, f'>2> {ret}') #10
        ret = view.insert(edit, pt, 'booga')
        sc.slog(sc.CAT_DBG, f'>2> {ret}') #0
        ret = view.replace(edit, reg, 'xyzzy')
        sc.slog(sc.CAT_DBG, f'>2> {ret}') #None
        ret = view.split_by_newlines(reg)
        sc.slog(sc.CAT_DBG, f'>2> {ret}') #[Region(10, 10)]
        ret = view.find('pattern', pt)
        sc.slog(sc.CAT_DBG, f'>2> {ret}') #(-1, -1)
        ret = view.substr(pt)
        sc.slog(sc.CAT_DBG, f'>2> |{len(ret)}|{ret[0]}|{ret}|') #|1|2023-06-24 09:06:19.561 DBG sbot_dev.py:175 >2> (10000, 10000)||
        ret = view.word(pt)
        sc.slog(sc.CAT_DBG, f'>2> {ret}|{view.substr(ret)}|') #nada - see previous
        ret = view.line(pt)
        sc.slog(sc.CAT_DBG, f'>2> {ret}|{view.substr(ret)}|') #(9990, 10000)||
        ret = view.full_line(pt)
        sc.slog(sc.CAT_DBG, f'>2> {ret}|{view.substr(ret)}|') #(9990, 10000)||
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
    # Panel iterate stuff.
    # create_output_panel(name, <unlisted>) Returns the view associated with the named output panel, creating it if required.
    #   The output panel can be shown by running the show_panel window command, with the panel argument set to the name with an "output." prefix.
    #   The optional unlisted parameter is a boolean to control if the output panel should be listed in the panel switcher.
    # find_output_panel(name) Returns the view associated with the named output panel, or None if the output panel does not exist.    
    # destroy_output_panel(name)  Destroys the named output panel, hiding it if currently open.   
    # active_panel()  Returns the name of the currently open panel, or None if no panel is open. Will return built-in panel names (e.g. "console", "find", etc) in addition to output panels. 
    # panels() Returns a list of the names of all panels that have not been marked as unlisted. Includes certain built-in panels in addition to output panels.

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
    ''' blabla. '''

    def run(self):
        # slog(sc.CAT_DBG, 'cadabra')
        # Bottom input area.
        self.window.show_input_panel(self.window.extract_variables()['folder'] + '>', "", self.on_done, None, None)

        # show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
        # Shows the input panel, to collect a line of input from the user. on_done and on_change, if not None, should both
        # be functions that expect a single string argument. on_cancel should be a function that expects no arguments. 
        # The view used for the input widget is returned.

    def on_done(self, text):
        # cp = subprocess.run(text, cwd=self.window.extract_variables()['folder'], universal_newlines=True, check=True, capture_output=True, shell=True)
        # sout = cp.stdout
        # create_new_view(self.window, sout)
        # slog(sc.CAT_DBG, f'Got:{text}')
        pass


#-----------------------------------------------------------------------------------
class SbotTestPhantomsCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super(SbotTestPhantomsCommand, self).__init__(view)
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, "my_key")
        self.count = 0

    def run(self, edit):
        image = os.path.join(sublime.packages_path(), "SbotDev", "felix.jpg")
        img_html = '<img src="file://' + image + '" width="16" height="16">'

        # Old way works too:
        # self.view.erase_phantoms("test")
        # self.view.erase_phantoms ("test")
        # for sel in self.view.sel():
        #     self.view.add_phantom ("test", sel, img_html, sublime.LAYOUT_BLOCK)


        # view = sc.create_new_view(sublime.active_window(), '>>> howdy!')
        # pt = 10000
        # reg = sublime.Region(pt, pt + 1)
        # ret = view.insert(edit, pt, 'booga') #0
        # sc.slog(sc.CAT_DBG, f'>>> {ret}')
        # ret = view.replace(edit, reg, 'booga') #None
        # sc.slog(sc.CAT_DBG, f'>>> {ret}')



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

        # Let's do some other visuals.
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
        # on_navigate is an optional callback that should accept a single string parameter,
        # that is the href attribute of the link clicked.
        pass


#-----------------------------------------------------------------------------------
class SbotCmdLineCommand(sublime_plugin.WindowCommand):
    ''' Run a simple command in the project dir. '''

    def run(self):
        # Bottom input area.
        self.window.show_input_panel(self.window.extract_variables()['folder'] + '>', "", self.on_done, None, None)

    def on_done(self, text):
        cp = subprocess.run(text, cwd=self.window.extract_variables()['folder'], universal_newlines=True, capture_output=True, shell=True)
        sout = cp.stdout
        vnew = self.window.new_file()
        vnew.set_scratch(True)
        vnew.run_command('append', {'characters': sout})  # insert has some odd behavior - indentation
