import sys
import os
import subprocess
import sublime
import sublime_plugin
import sublime_api

try:
    from SbotCommon.sbot_common import log_message
except ModuleNotFoundError as e:
    raise ImportError('SbotDev plugin requires SbotCommon plugin')


# TODO Sublime environment updates for linux. Packages?

# TODO remove some from Default context menu?

# TODO pdb?

# These go directly to console via _LogWriter(). Our hooks don't intercept. Must be loaded before our stuff.
#   sublime.log_commands(True/False)
#   sublime.log_input(True/False)
#   sublime.log_result_regex(True/False)
#   sublime.log_control_tree(True/False)
#   sublime.log_fps(True/False)
#   sublime_api.log_message('Called sublime_api.log_message()\n')
#   initial plugin loading messages: reloading ...  Package Control: ...


#-----------------------------------------------------------------------------------
def plugin_loaded():

    log_message('DEV', 'howdy')
    # dump_stack()


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    log_message('DEV')


#-----------------------------------------------------------------------------------
def dump_stack(cat):
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
class SbotDebugCommand(sublime_plugin.WindowCommand):

    def run(self):
        log_message('DEV', 'doody')
        # dump_stack()
        # modules = dir()
        # modules = sys.modules.keys()
        i = 999 / 0


#-----------------------------------------------------------------------------------
class SbotDebugEvent(sublime_plugin.EventListener):
    ''' Listener for view specific events of interest. '''


    def on_init(self, views):
        ''' First thing that happens when plugin/window created. Views are valid.
        Note that this also happens if this module is reloaded - like when editing this file. '''
        log_message('DEV', f'{views}')

    def on_load_project(self, window):
        ''' This gets called for new windows but not for the first one. '''
        log_message('DEV')

    def on_pre_close_project(self, window):
        ''' Save to file when closing window/project. Seems to be called twice. '''
        log_message('DEV')

    def on_load(self, view):
        ''' Load a file. '''
        log_message('DEV')

    def on_deactivated(self, view):
        # Window is still valid here.
        log_message('DEV')

    def on_pre_close(self, view):
        ''' This happens after on_pre_close_project(). '''
        log_message('DEV')

    def on_close(self, view):
        log_message('DEV')

    def on_pre_save(self, view):
        log_message('DEV')

    def on_post_save(self, view):
        log_message('DEV')

    def on_pre_close_window(self, window):
        log_message('DEV')

    def on_new_window(self, window):
        ''' Another window/instance has been created. Project has not been opened yet though. '''
        log_message('DEV')


#-----------------------------------------------------------------------------------
class SbotTestPanelCommand(sublime_plugin.WindowCommand):
    ''' blabla. '''

    # Panel iterate stuff.
    # create_output_panel(name, <unlisted>) Returns the view associated with the named output panel, creating it if required.
    #   The output panel can be shown by running the show_panel window command, with the panel argument set to the name with an "output." prefix.
    #   The optional unlisted parameter is a boolean to control if the output panel should be listed in the panel switcher.
    # find_output_panel(name) Returns the view associated with the named output panel, or None if the output panel does not exist.    
    # destroy_output_panel(name)  Destroys the named output panel, hiding it if currently open.   
    # active_panel()  Returns the name of the currently open panel, or None if no panel is open. Will return built-in panel names (e.g. "console", "find", etc) in addition to output panels. 
    # panels() Returns a list of the names of all panels that have not been marked as unlisted. Includes certain built-in panels in addition to output panels.

    # You should be able to put a startup.py in your Packages/User directory with contents like:
    # import sublime
    # import sublime_plugin
    # class ShowPanel(sublime_plugin.EventListener):
    #     def on_activated_async(self, view):
    #         view.window().run_command("show_panel", {"panel": "output.SublimeLinter"})
    # You probably have to fiddle with what events to use though, this example isn’t that nice.


    def run(self):
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

        self.window.show_quick_panel(items,
                                     self.on_done,
                                     flags=sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT,
                                     selected_index=2,
                                     on_highlight=self.on_highlight,
                                     placeholder="place-xxx")

    def on_done(self, *args, **kwargs):
        sel = args[0]

    def on_highlight(self, *args, **kwargs):
        hlt = args[0]


#-----------------------------------------------------------------------------------
class SbotTestPanelInputCommand(sublime_plugin.WindowCommand):
    ''' blabla. '''

    def run(self):
        # Bottom input area.
        self.window.show_input_panel(self.window.extract_variables()['folder'] + '>', "", self.on_done, None, None)

    def on_done(self, text):
        cp = subprocess.run(text, cwd=self.window.extract_variables()['folder'], universal_newlines=True, check=True, capture_output=True, shell=True)
        sout = cp.stdout
        # create_new_view(self.window, sout)


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

        # sublime.LAYOUT_INLINE: Display in between the region and the point following.
        # sublime.LAYOUT_BELOW: Display in space below the current line, left-aligned with the region.
        # sublime.LAYOUT_BLOCK: Display in space below the current line, left-aligned with the beginning of the line.

    def nav(self, href):
        # on_navigate is an optional callback that should accept a single string parameter,
        # that is the href attribute of the link clicked.
        pass


#-----------------------------------------------------------------------------------
class SbotShowEolCommand(sublime_plugin.TextCommand):
    ''' Show line ends. '''

    def run(self, edit):
        if not self.view.get_regions("eols"):
            eols = []
            ind = 0
            while 1:
                freg = self.view.find('[\n\r]', ind)  # this doesn't work as ST normalizes endings. See what hexviewer does?
                if freg is not None and not freg.empty():  # second condition is not documented.
                    eols.append(freg)
                    ind = freg.end() + 1
                else:
                    break
            if eols:
                settings = sublime.load_settings("SbotSignet.sublime-settings")
                self.view.add_regions("eols", eols, settings.get('eol_scope'))
        else:
            self.view.erase_regions("eols")


# #-----------------------------------------------------------------------------------
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



# #-----------------------------------------------------------------------------------
# class SbotCmdLineCommand(sublime_plugin.WindowCommand):
#     ''' Run a simple command in the project dir. '''

#     def run(self):
#         # Bottom input area.
#         self.window.show_input_panel(self.window.extract_variables()['folder'] + '>', "", self.on_done, None, None)

#     def on_done(self, text):
#         cp = subprocess.run(text, cwd=self.window.extract_variables()['folder'], universal_newlines=True, capture_output=True, shell=True)
#         sout = cp.stdout
#         vnew = self.window.new_file()
#         vnew.set_scratch(True)
#         vnew.run_command('append', {'characters': sout})  # insert has some odd behavior - indentation


