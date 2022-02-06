import os
import subprocess
import sublime
import sublime_plugin


#-----------------------------------------------------------------------------------
def plugin_loaded():
    # print(">>> SbotDev plugin_loaded()")
    pass


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    # print("SbotDev plugin_unloaded()")
    pass


#-----------------------------------------------------------------------------------
class SbotTestPanelCommand(sublime_plugin.WindowCommand):
    ''' Run a simple command in the project dir. '''

    def run(self):
        directions = ["north", "south", "east", "west"]

        items = []
        for l in directions:
            items.append(sublime.QuickPanelItem(l, details=["<i>details</i>", "<b>more</b>"], annotation=f"look_{l}", kind=sublime.KIND_NAVIGATION))

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

        self.window.show_quick_panel(items, self.on_done,
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
    ''' Run a simple command in the project dir. '''

    def run(self):
        # Bottom input area.
        self.window.show_input_panel(self.window.extract_variables()['folder'] + '>', "", self.on_done, None, None)

    def on_done(self, text):
        cp = subprocess.run(text, cwd=self.window.extract_variables()['folder'], universal_newlines=True, check=True, capture_output=True, shell=True)
        sout = cp.stdout
        create_new_view(self.window, sout)


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
        print(f"href:{href}")


#-----------------------------------------------------------------------------------
class SbotShowEolCommand(sublime_plugin.TextCommand):
    ''' Show line ends. '''

    def run(self, edit):
        if not self.view.get_regions("eols"):
            eols = []
            ind = 0
            while 1:
                freg = self.view.find('[\n\r]', ind)  # TODO this doesn't work as ST normalizes endings. See what hexviewer does?
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
