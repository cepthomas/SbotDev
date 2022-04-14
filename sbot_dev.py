import sys
import os
import subprocess
import sublime
import sublime_plugin

try:
    from SbotCommon.sbot_common import trace_function, trace_method, get_store_fn
except ModuleNotFoundError as e:
    sublime.message_dialog('SbotDev plugin requires SbotCommon plugin')


# TODO Sublime environment updates for linux. Packages?


# TODO generic/common?
#   - Decorator for tracing function entry.


# TODO more debugging tools for plugins:
#   - extension to logger print?
# print(f'*** {fn}')
# log_commands(flag) - Controls command logging. If enabled, all commands run from key bindings and the menu will be logged to the console.    
# log_input(flag) - Controls input logging. If enabled, all key presses will be logged to the console.  
# log_result_regex(flag) - Controls result regex logging. This is useful for debugging regular expressions used in build systems.  
# log_control_tree(flag) - When enabled, clicking with Ctrl+Alt will log the control tree under the mouse to the console.  4064
# log_fps(flag) - When enabled, logs the number of frames per second being rendered for the user interface


# You can only import modules from the Python Standard Library and use the ones provided by Sublime Text.
# If you want to import a third-party module, e.g. memoized, you need to include it as a dependency.
# So you find the module source, copy it and publish via PackageControl.
# Then add it to your project using dependencies.json file.



# class LintAndPanel(sublime_plugin.WindowCommand):
#     def run(self):
#         self.window.run_command("sublime_linter_lint")
#         self.window.run_command("sublime_linter_panel_toggle")


# Then in your keybindings you can now set something for the new lint_and_panel (the camel case class translates to cool_hacker_case here) like so:
# { "keys": ["super+p"], "command": "lint_and_panel" },


# You should be able to put a startup.py in your Packages/User directory with contents like:
# import sublime
# import sublime_plugin
# class ShowPanel(sublime_plugin.EventListener):
#     def on_activated_async(self, view):
#         view.window().run_command("show_panel", {"panel": "output.SublimeLinter"})
# You probably have to fiddle with what events to use though, this example isn’t that nice. Anyway, hope that gets you started in the right direction.

# create_output_panel(name, <unlisted>)   View    
# Returns the view associated with the named output panel, creating it if required. The output panel can be shown by running the show_panel window command, with the panel argument set to the name with an "output." prefix.
# The optional unlisted parameter is a boolean to control if the output panel should be listed in the panel switcher.

# find_output_panel(name) View or None    Returns the view associated with the named output panel, or None if the output panel does not exist.    

# destroy_output_panel(name)  None    Destroys the named output panel, hiding it if currently open.   

# active_panel()  str or None    Returns the name of the currently open panel, or None if no panel is open. Will return built-in panel names (e.g. "console", "find", etc) in addition to output panels. 

# panels()    [str]   Returns a list of the names of all panels that have not been marked as unlisted. Includes certain built-in panels in addition to output panels.

# TODO remove some from Default context menu?


# print(f'>>>>{test_func(6)}')

# print(f'*** {trace_method}')


#-----------------------------------------------------------------------------------
@trace_function
def plugin_loaded():
    # print(">>> SbotDev plugin_loaded()")
    pass


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    # print("SbotDev plugin_unloaded()")
    pass


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.WindowCommand):
    @trace_method
    def run(self):
        modules = dir()
        modules = sys.modules#.keys()
        # 'SbotFormat.sbot_format', 'SbotHighlight', 'SbotHighlight.sbot_highlight', 'SbotLogger', 'SbotLogger.sbot_logger',
        # 'SbotRender', 'SbotRender.sbot_render', 'SbotScope', 'SbotScope.sbot_scope', 'SbotSidebar', 'SbotSidebar.sbot_sidebar',
        # 'SbotSignet', 'SbotSignet.sbot_signet', '_bootlocale', 'SbotDev.sbot_dev'

        print(f'modules:{modules}')


#-----------------------------------------------------------------------------------
class SbotTestPanelCommand(sublime_plugin.WindowCommand):
    ''' blabla. '''

    def run(self):
        directions = ["north", "south", "east", "west"]

        items = []
        for dir in directions:
            items.append(sublime.QuickPanelItem(dir, details=["<i>details</i>", "<b>more</b>"], annotation=f"look_{dir}", kind=sublime.KIND_NAVIGATION))

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

            # sublime.MONOSPACE_FONT - use a monospace font
            # sublime.KEEP_OPEN_ON_FOCUS_LOST - keep the quick panel open if the window loses input focus
            # sublime.WANT_EVENT - pass a second parameter to on_done, an event Dict

        self.window.show_quick_panel(items,
                                     self.on_done,
                                     flags=sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT | sublime.MONOSPACE_FONT,
                                     selected_index=2,
                                     on_highlight=self.on_highlight,
                                     placeholder="place-xxx")

    def on_done(self, *args, **kwargs):
        print(f"SEL:{args[0]}")
        # print(f"on_done args:{args} kwargs:{kwargs}")

    def on_highlight(self, *args, **kwargs):
        print(f"HLT:{args[0]}")
        # print(f"on_highlight args:{args} kwargs:{kwargs}")


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
        image = os.path.join(sublime.packages_path(), "SbotDev", "felix.jpg") #TODO get from common.
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
        print(f"href:{href}")


#-----------------------------------------------------------------------------------
class SbotShowEolCommand(sublime_plugin.TextCommand):
    ''' Show line ends. '''

    def run(self, edit):
        if not self.view.get_regions("eols"):
            eols = []
            ind = 0
            while 1:
                freg = self.view.find('[\n\r]', ind)  # this doesn't work as ST normalizes endings. See what hexviewer does?
                if freg is not None and not freg.empty():  # second condition is not documented!!
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



# #-----------------------------------------------------------------------------------
# class SbotGeneralEvent(sublime_plugin.EventListener):
#     ''' Listener for window events of interest. '''

#     def on_selection_modified(self, view):
#         ''' Show the abs position in the status bar. '''
#         pos = view.sel()[0].begin()
#         view.set_status("position", f'Pos {pos}')


#-----------------------------------------------------------------------------------
class SbotSplitViewCommand(sublime_plugin.WindowCommand):
    ''' Toggles between split file views.'''

    def run(self):
        window = self.window

        if len(window.layout()['rows']) > 2:
            # Remove split.
            window.run_command("focus_group", {"group": 1})
            window.run_command("close_file")
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})
        else:
            # Add split.
            sel_row, _ = window.active_view().rowcol(window.active_view().sel()[0].a)  # current sel
            window.run_command("set_layout", {"cols": [0.0, 1.0], "rows": [0.0, 0.5, 1.0], "cells": [[0, 0, 1, 1], [0, 1, 1, 2]]})
            window.run_command("focus_group", {"group": 0})
            window.run_command("clone_file")
            window.run_command("move_to_group", {"group": 1})
            window.active_view().run_command("goto_line", {"line": sel_row})

