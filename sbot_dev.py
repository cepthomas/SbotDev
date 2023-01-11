import sys
import os
import subprocess
import webbrowser
import sublime
import sublime_plugin
import sublime_api # For undocumented internals.

try:
    from SbotCommon.sbot_common import slog, create_new_view
except ModuleNotFoundError as e:
    sublime.message_dialog('SbotDev plugin requires SbotCommon plugin')
    raise ImportError('SbotDev plugin requires SbotCommon plugin')


# TODO Packages?
# TODO Sublime environment updates for linux.
# TODO remove some from Default context menu? https://forum.sublimetext.com/t/altering-default-context-menu/28766/3
# TODO pdb?


# These go directly to console via _LogWriter(). Our hooks don't intercept.
#   sublime.log_commands(True/False)
#   sublime.log_input(True/False)
#   sublime.log_result_regex(True/False)
#   sublime.log_control_tree(True/False)
#   sublime.log_fps(True/False)
#   sublime_api.log_message('Called sublime_api.log_message()\n')


#-----------------------------------------------------------------------------------
def plugin_loaded():
    slog('X--X')
    # dump_stack()
    pass


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    slog('X--X')
    pass


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
class SbotCheatsheetCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.open_file('ST-commands.md')


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.WindowCommand):

    def run(self):
        slog('X--X', '== before')

        # print(os.environ)

        # dump_stack()
        # modules = dir()
        # modules = sys.modules.keys()
        

        # Force a handled exception.
        # try:
        #     i = 111 / 0
        # except Exception as e:
        #     with open(r'somewhere\sbot_trace.log', 'a') as f:
        #         import traceback
        #         traceback.print_exc(file=f)

        # Force an unhandled exception.
        i = 222 / 0

        slog('X--X', '== after')

        ### stack stuff
        # Get stackframe info. This is supposedly the fastest way. https://gist.github.com/JettJones/c236494013f22723c1822126df944b12.
        # frame = sys._getframe(0)
        # fn = os.path.basename(frame.f_code.co_filename)
        # func = frame.f_code.co_name
        # line = frame.f_lineno

        # dump_attrs(frame)
        # >>> f_back, f_builtins, f_code, f_globals, f_lasti, f_lineno, f_locals, f_trace, f_trace_lines, f_trace_opcodes, False
        # dump_attrs(frame.f_code)
        # >>> co_argcount, co_cellvars, co_code, co_consts, co_filename, co_firstlineno, co_flags, co_freevars, co_kwonlyargcount,
        #    co_lnotab, co_name, co_names, co_nlocals, co_posonlyargcount, co_stacksize, co_varnames


def start_interactive():
    winid = sublime.active_window().id()
    view = create_new_view(sublime.active_window(), '>>> howdy!')
    slog('X--X', f'{self.view}  {winid}')
    view.settings().set('interactive' , True)

class SbotInteractive(sublime_plugin.ViewEventListener):
    # def __init__(self, view):
    #     # This gets called for every view.
    #     slog('X--X', str(view))
    #     super(sublime_plugin.ViewEventListener, self).__init__(view)
    #     super().__init__(view)

    def on_selection_modified(self):
        if self.view.settings().get('interactive'):
            slog('X--X', '+++++++')
            pass

    # def on_init(self):
    # def on_load(self):
    # def on_activated(self):
    # def on_deactivated(self):
    # def on_pre_close(self):
    # def on_close(self):
    # def on_pre_save(self):
    # def on_post_save(self):
    # def on_modified(self): Called after changes have been made to the view.
    # def on_text_changed(self, changes): Called once after changes has been made to a view. changes is a list of TextChange objects.
    # def on_selection_modified(self): Called after the selection has been modified in the view.   

    ### pdb? stuff
    # import pdb
    # mydb = pdb.Pdb(stdin=sys.stdin)
    # mydb.set_trace()
    # breakpoint()
    
    # New in version 3.7: The built-in breakpoint(), when called with defaults, can be used instead of import pdb; pdb.set_trace().
    # The run* functions and set_trace() are aliases for instantiating the Pdb class and calling the method of the same name. 
    # If you want to access further features, you have to do this yourself:
    # pdb.Pdb(completekey='tab', stdin=None, stdout=None, skip=None, nosigint=False, readrc=True)
    # sys.stderr = self

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
        slog('X--X', 'abra')
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
            # kind - An optional kind tuple – defaults to sublime.KIND_AMBIGUOUS.
            # sublime.KIND_AMBIGUOUS When there source of the item is unknown – the default. Letter: none, theme class: kind_ambiguous
            # sublime.KIND_KEYWORD When the item represents a keyword. Letter: k, theme class: kind_keyword
            # sublime.KIND_TYPE When the item represents a data type, class, struct, interface, enum, trait, etc. Letter: t, theme class: kind_type
            # sublime.KIND_FUNCTION When the item represents a function, method, constructor or subroutine. Letter: f, theme class: kind_function
            # sublime.KIND_NAMESPACE When the item represents a namespace or module. Letter: a, theme class: kind_namespace
            # sublime.KIND_NAVIGATION When the item represents a definition, label or section. Letter: n, theme class: kind_navigation
            # sublime.KIND_MARKUP When the item represents a markup component, including HTML tags and CSS selectors. Letter: m, theme class: kind_markup
            # sublime.KIND_VARIABLE When the item represents a variable, member, attribute, constant or parameter. Letter: v, theme class: kind_variable
            # sublime.KIND_SNIPPET When the item contains a snippet. Letter: s, theme class: kind_snippet

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
        slog('X--X', 'cadabra')
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
        slog('====', f'Got:{text}')


#-----------------------------------------------------------------------------------
class SbotTestPhantomsCommand(sublime_plugin.TextCommand):
    # def __init__(self, view):
    #     self.phantom_set = sublime.PhantomSet(self.view, "my_key")

    def __init__(self, view):
        super(SbotTestPhantomsCommand, self).__init__(view)
        self.view = view
        self.phantom_set = sublime.PhantomSet(self.view, "my_key")
        self.count = 0

    def run(self, edit):
        # image = f"C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Packages\\SublimeBagOfTricks\\test\\files\\mark64.bmp"
        image = os.path.join(sublime.packages_path(), "SbotDev", "felix.jpg")
        img_html = '<img src="file://' + image + '" width="16" height="16">'

        # Old way works too:
        # self.view.erase_phantoms("test")
        # self.view.erase_phantoms ("test")
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

#-----------------------------------------------------------------------------------
# class SbotAllEvent(sublime_plugin.EventListener):
#     ''' For tracing EventListener event sequence. '''

#     def on_init(self, views):
#         ''' First thing that happens when plugin/window created. Views are valid.
#         Note that this also happens if this module is reloaded - like when editing this file. '''
#         slog('X--X', f'{views}')

#     def on_load_project(self, window):
#         ''' This gets called for new windows but not for the first one. '''
#         slog('X--X')

#     def on_pre_close_project(self, window):
#         ''' Save to file when closing window/project. Seems to be called twice. '''
#         slog('X--X')

#     def on_load(self, view):
#         ''' Load a file. '''
#         slog('X--X')

#     def on_deactivated(self, view):
#         # Window is still valid here.
#         slog('X--X')

#     def on_pre_close(self, view):
#         ''' This happens after on_pre_close_project(). '''
#         slog('X--X')

#     def on_close(self, view):
#         slog('X--X')

#     def on_pre_save(self, view):
#         slog('X--X')

#     def on_post_save(self, view):
#         slog('X--X')

#     def on_pre_close_window(self, window):
#         slog('X--X')

#     def on_new_window(self, window):
#         ''' Another window/instance has been created. Project has not been opened yet though. '''
#         slog('X--X')


#-------------------------------- Graveyard ---------------------------------------------------
# class SbotShowEolCommand(sublime_plugin.TextCommand):
#     ''' Show line ends. '''

#     def run(self, edit):
#         if not self.view.get_regions("eols"):
#             eols = []
#             ind = 0
#             while 1:
#                 freg = self.view.find('[\n\r]', ind)  # this doesn't work as ST normalizes endings. See what hexviewer does?
#                 if freg is not None and not freg.empty():  # second condition is not documented.
#                     eols.append(freg)
#                     ind = freg.end() + 1
#                 else:
#                     break
#             if eols:
#                 settings = sublime.load_settings("xxx.sublime-settings")
#                 self.view.add_regions("eols", eols, settings.get('eol_scope'))
#         else:
#             self.view.erase_regions("eols")


#-------------------------------- Graveyard ---------------------------------------------------
# class SbotSidebarOpenFileCommand(sublime_plugin.WindowCommand):
#     ''' Simple file opener using default application, like you double clicked it.
#
#     def run(self, paths):
#         if len(paths) > 0:
#             if platform.system() == 'Windows':
#                 os.startfile(paths[0])
#             elif platform.system() == 'Linux':
#                 subprocess.run(('xdg-open', paths[0]))
#
#     def is_visible(self, paths):
#         vis = (platform.system() == 'Windows' or platform.system() == 'Linux') and len(paths) > 0
#         return vis
