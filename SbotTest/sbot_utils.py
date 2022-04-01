import subprocess
import sublime
import sublime_plugin


#-----------------------------------------------------------------------------------
def plugin_loaded():
    pass


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    pass


#-----------------------------------------------------------------------------------
class SbotEvent(sublime_plugin.EventListener):
    ''' Listener for window specific events of interest. '''

    def on_selection_modified(self, view):
        ''' Show the abs position in the status bar. '''
        pos = view.sel()[0].begin()
        view.set_status("position", f'Pos {pos}')

    def on_load_project(self, window):
        ''' Doesn't fire on startup (last) project load. '''
        print(f"on_load_project() {window.project_file_name()}")

    def on_exit(self):
        ''' Called once after the API has shut down, immediately before the plugin_host process exits. '''
        print("on_exit()")

    def on_pre_close_window(self, window):
        ''' Seems to work. '''
        print("on_pre_close_window()")


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
