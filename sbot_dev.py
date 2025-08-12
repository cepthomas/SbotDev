import sys
import os
import subprocess
import platform
import traceback
import datetime
import importlib
import bdb
import string
import re
import enum
import json
import xml
import xml.dom.minidom
import sublime
import sublime_plugin




from . import sbot_common as sc
# try:
#     from . import sbot_common as sc
#     print('>>> normal import') 
# except:
#     import sbot_common as sc
#     print('>>> unittest import')


# my_dir = os.path.dirname(__file__)
# # Add source path to sys.
# utils.ensure_import(my_dir, '..')
# # OK to import now.
# import code_format
# # # Benign reload in case of edited.
# # importlib.reload(tr)


# # Add path to sys.
# def ensure_import(*paths):
#     npath = os.path.abspath(os.path.join(*paths))
#     if npath not in sys.path:
#         # append rather than insert so can override builtin.
#         sys.path.append(npath)



# pbot_path = os.path.abspath(os.path.join('\\', 'Dev', 'Libs', 'PyBagOfTricks'))
pbot_path = R'C:\Dev\Libs\PyBagOfTricks'
if pbot_path not in sys.path:
    sys.path.append(pbot_path)

# import pbot_pdb
# import code_format


# Benign reload in case of edited.
importlib.reload(sc)

# Syntax defs.
SYNTAX_C = 'Packages/C++/C.sublime-syntax'
SYNTAX_CPP = 'Packages/C++/C++.sublime-syntax'
SYNTAX_CS = 'Packages/C#/C#.sublime-syntax'
SYNTAX_XML = 'Packages/XML/XML.sublime-syntax'
SYNTAX_LUA = 'Packages/Lua/Lua.sublime-syntax'
SYNTAX_JSON = 'Packages/JSON/JSON.sublime-syntax'


#-----------------------------------------------------------------------------------
# Write to dump file.
def _dump(txt):
    fn = os.path.join(os.path.dirname(__file__), 'out', 'dump.log')
    with open(fn, 'a') as f:
        f.write(txt + '\n')
        f.flush()

#-----------------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    sc.debug(f'plugin_loaded {__package__} with python {platform.python_version()} on {platform.platform()}')


#-----------------------------------------------------------------------------------
def plugin_unloaded():
    '''Called per plugin instance.'''
    sc.info(f'plugin_unloaded {__package__}')


#-----------------------------------------------------------------------------------
class DevEvent(sublime_plugin.EventListener):
    ''' General listener. https://www.sublimetext.com/docs/api_reference.html#sublime_plugin.EventListener '''

    def on_init(self, views):
        ''' Called once with a list of views that were loaded before the EventListener was instantiated. '''
        # First thing that happens when plugin/window created. Initialize everything.
        pass

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

    def on_exit(self):
        # Called once after the API has shut down, immediately before the plugin_host process exits
        sc.info(f'on_exit {__package__}')


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        # Blow stuff up. Force unhandled exception.
        sc.debug('Forcing unhandled exception!')
        sc.open_path('not-a-real-file')
        # i = 222 / 0


        # _dump('====== Dump a stack - most recent last')
        # for f in traceback.extract_stack():
        #     _dump(_frame_formatter(f))


        # _dump('====== Dump a traceback - most recent last')
        # try:
        #     x = 1 / 0
        # except Exception as e:
        #     for f in traceback.extract_tb(e.__traceback__):
        #         _dump(_frame_formatter(f))


        # '''
        # is_folded(region: Region) → bool
        # folded_regions() → list[sublime.Region]
        # fold(x: Region | list[sublime.Region]) → bool
        # unfold(x: Region | list[sublime.Region]) → list[sublime.Region]
        # '''
        # regions = self.view.folded_regions()
        # text = ["folded_regions"]
        # for r in regions:
        #     s = f'region:{r}'
        #     text.append(s)
        # new_view = sc.create_new_view(self.view.window(), '\n'.join(text))


#-----------------------------------------------------------------------------------
class SbotGitCommand(sublime_plugin.TextCommand):

    def run(self, edit, git_cmd):
        ''' Simple git tools: diff, commit (no comment), push.
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
                details="<i>details</i><b>more</b>",
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
# class RunPdbCommand(sublime_plugin.TextCommand):
#     ''' How to hook pdb into ST. TODO1 '''

#     def run(self, edit):
#         del edit
#         TEST_OUT_PATH = os.path.join(os.path.dirname(__file__), 'out') TODOX
#         # import sys, os~
#         sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Common')) TODOX
#         # import Common

#         print('>>>>', sys.path)
#         # >>>> [
#             # 'C:\\Program Files\\Sublime Text\\Lib\\python3.8.zip',
#             # 'C:\\Program Files\\Sublime Text\\Lib\\python38',
#             # 'C:\\Program Files\\Sublime Text\\Lib\\python3',
#             # 'C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Lib\\python38',
#             # 'C:\\Program Files\\Sublime Text\\Packages',
#             # 'C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Packages'
#             # ]

#         # # Set a breakpoint here then step through and examine the code.
#         # from . import sbot_pdb; sbot_pdb.breakpoint()

#         # ret = self.function_1(911, 'abcd')
#         # print('ret:', ret)

#         # # Unhandled exception actually goes to sys.__excepthook__.
#         # # function_boom()

#         # ret = self.function_2([33, 'thanks', 3.56], {'aaa': 111, 'bbb': 222, 'ccc': 333})
#         # print('ret:', ret)


#     #----------------------------------------------------------
#     def function_1(self, a1: int, a2: str):
#         '''A simple function.'''
#         ret = f'answer is:{a1 * len(a2)}'
#         return ret

#     #----------------------------------------------------------
#     def function_2(self, a_list, a_dict):
#         '''A simple function.'''
#         return len(a_list) + len(a_dict)

#     #----------------------------------------------------------
#     def function_boom(self):
#         '''A function that causes an unhandled exception.'''
#         return 1 / 0

# { "caption": "-" },
# { "caption": "Run pdb dev", "command": "sbot_run_pdb" },
# { "caption": "Run pdb example", "command": "sbot_pdb_example" },


#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#--------------------TODO1 all this format stuff------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------
class SbotFormatJsonCommand(sublime_plugin.TextCommand):
    ''' sbot_format_json'''

    def is_visible(self):
        return self.view.settings().get('syntax') == SYNTAX_JSON
        # return True

    def run(self, edit):
        del edit
        sres = []
        err = False

        reg = sc.get_sel_regions(self.view)[0]
        s = self.view.substr(reg)
        s = format_json(s)
        sres.append(s)
        if s.startswith('Error'):
            err = True

        vnew = sc.create_new_view(self.view.window(), '\n'.join(sres))
        if not err:
            vnew.set_syntax_file(SYNTAX_JSON)


#-----------------------------------------------------------------------------------
class SbotFormatXmlCommand(sublime_plugin.TextCommand):
    ''' sbot_format_xml'''

    def is_visible(self):
        return self.view.settings().get('syntax') == SYNTAX_XML

    def run(self, edit):
        del edit
        err = False

        settings = sublime.load_settings(sc.get_settings_fn())
        reg = sc.get_sel_regions(self.view)[0]
        s = self.view.substr(reg)
        s = format_xml(s, settings.get('tab_size'))
        if s.startswith('Error'):
            err = True

        vnew = sc.create_new_view(self.view.window(), s)
        if not err:
            vnew.set_syntax_file(SYNTAX_XML)


#-----------------------------------------------------------------------------------
class SbotFormatCxCommand(sublime_plugin.TextCommand):
    ''' sbot_format_cx '''

    def is_visible(self):
        syntax = self.view.settings().get('syntax')
        return syntax in [SYNTAX_C, SYNTAX_CPP, SYNTAX_CS]

    def run(self, edit):
        del edit
        
        # Current syntax.
        syntax = str(self.view.settings().get('syntax'))
        settings = sublime.load_settings(sc.get_settings_fn())
        reg = sc.get_sel_regions(self.view)[0]
        s = self.view.substr(reg)

        sout = format_cx(s, syntax, settings.get('tab_size'))

        vnew = sc.create_new_view(self.view.window(), sout)
        vnew.set_syntax_file(syntax)




#-----------------------------------------------------------------------------------
def format_json(s):
    ''' Clean and format the string. Returns the new string. '''

    class ScanState(enum.IntFlag):
        DEFAULT = enum.auto()   # Idle
        STRING = enum.auto()    # Process a quoted string
        LCOMMENT = enum.auto()  # Processing a single line comment
        BCOMMENT = enum.auto()  # Processing a block/multiline comment
        DONE = enum.auto()      # Finito

    # tabWidth = 4
    comment_count = 0
    sreg = []
    state = ScanState.DEFAULT
    current_comment = []
    current_char = -1
    next_char = -1
    escaped = False

    # Index is in cleaned version, value is in original.
    pos_map = []

    # Iterate the string.
    try:
        slen = len(s)
        i = 0
        while i < slen:
            current_char = s[i]
            next_char = s[i + 1] if i < slen - 1 else -1

            # Remove whitespace and transform comments into legal json.
            if state == ScanState.STRING:
                sreg.append(current_char)
                pos_map.append(i)
                # Handle escaped chars.
                if current_char == '\\':
                    escaped = True
                elif current_char == '\"':
                    if not escaped:
                        state = ScanState.DEFAULT
                    escaped = False
                else:
                    escaped = False

            elif state == ScanState.LCOMMENT:
                # Handle line comments.
                if current_char == '\n':
                    # End of comment.
                    scom = ''.join(current_comment)
                    stag = f'\"//{comment_count}\":\"{scom}\",'
                    comment_count += 1
                    sreg.append(stag)
                    pos_map.append(i)
                    state = ScanState.DEFAULT
                    current_comment.clear()
                elif current_char == '\r':
                    # ignore
                    pass
                else:
                    # Maybe escape.
                    if current_char == '\"' or current_char == '\\':
                        current_comment.append('\\')
                    current_comment.append(current_char)

            elif state == ScanState.BCOMMENT:
                # Handle block comments.
                if current_char == '*' and next_char == '/':
                    # End of comment.
                    scom = ''.join(current_comment)
                    stag = f'\"//{comment_count}\":\"{scom}\",'
                    comment_count += 1
                    sreg.append(stag)
                    pos_map.append(i)
                    state = ScanState.DEFAULT
                    current_comment.clear()
                    i += 1  # Skip next char.
                elif current_char == '\n' or current_char == '\r':
                    # ignore
                    pass
                else:
                    # Maybe escape.
                    if current_char == '\"' or current_char == '\\':
                        current_comment.append('\\')
                    current_comment.append(current_char)

            elif state == ScanState.DEFAULT:
                # Check for start of a line comment.
                if current_char == '/' and next_char == '/':
                    state = ScanState.LCOMMENT
                    current_comment.clear()
                    i += 1  # Skip next char.
                # Check for start of a block comment.
                elif current_char == '/' and next_char == '*':
                    state = ScanState.BCOMMENT
                    current_comment.clear()
                    i += 1  # Skip next char.
                elif current_char == '\"':
                    sreg.append(current_char)
                    pos_map.append(i)
                    state = ScanState.STRING
                # Skip ws.
                elif current_char not in string.whitespace:
                    sreg.append(current_char)
                    pos_map.append(i)

            else:  # state == ScanState.DONE:
                pass
            i += 1  # next

        # Prep for formatting.
        ret = ''.join(sreg)

        # Remove any trailing commas.
        ret = re.sub(',}', '}', ret)
        ret = re.sub(',]', ']', ret)

        # Run it through the formatter.
        ret = json.loads(ret)
        ret = json.dumps(ret, indent=4)

    except json.JSONDecodeError as je:
        # Get some context from the original string.
        context = []
        original_pos = pos_map[je.pos]
        start_pos = max(0, original_pos - 40)
        end_pos = min(len(s) - 1, original_pos + 40)
        context.append(f'Json Error: {je.msg} pos: {original_pos}')
        context.append(s[start_pos:original_pos])
        context.append('---------here----------')
        context.append(s[original_pos:end_pos])
        ret = '\n'.join(context)

    return ret


#-----------------------------------------------------------------------------------
def format_xml(s, indent):
    ''' Clean and format the string. Returns the new string. '''

    def clean(node):
        for n in node.childNodes:
            if n.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                if n.nodeValue:
                    n.nodeValue = n.nodeValue.strip()
            elif n.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                clean(n)
    
    try:
        top = xml.dom.minidom.parseString(s)
        clean(top)  
        top.normalize()
        sindent = ' ' * int(indent)
        ret = top.toprettyxml(indent=sindent)
    except Exception as e:
        ret = f"Error: {e}"

    return ret


#-----------------------------------------------------------------------------------
def format_cx(s, syntax, indent):
    ''' Clean and format C/C++/C# string. Returns the new string. '''

    # Build the command. Uses --style=allman --indent=spaces=4 --indent-col1-comments --errors-to-stdout
    sindent = f"-s{indent}"
    p = ['astyle', '-A1', sindent, '-Y', '-X']
    if syntax == 'C#': # else default of C
        p.append('--mode=cs')

    try:
        cp = subprocess.run(p, input=s, text=True, universal_newlines=True, capture_output=True, shell=True, check=True)
        sout = cp.stdout
    except Exception:
        sout = "Format Cx failed. Is astyle installed and in your path?"

    return sout


#-----------------------------------------------------------------------------------
def test_format(): 

    my_dir = os.path.dirname(__file__)

    def assertEqual(s1, s2):
        pass

    def fail(s1):
        pass

    #------------------------------------------------------------
    # def test_format_json(self):

    fn = os.path.join(my_dir, 'messy.json')
    with open(f'{fn}', 'r') as fp:
        # The happy path.
        s = fp.read()
        res = format_json(s)
        assertEqual(res[:50], '{\n    "MarkPitch": {\n        "Original": 0,\n      ')

        # Make it a bad file.
        s = s.replace('\"Original\"', '')
        res = format_json(s)
        assertEqual(res[:50], "Json Error: Expecting property name enclosed in do")


    #------------------------------------------------------------
    # def test_format_xml(self):

    fn = os.path.join(my_dir, 'messy.xml')
    with open(f'{fn}', 'r') as fp:
        # The happy path.
        s = fp.read()
        res = format_xml(s, 4)
        if 'Error:' in res:
            fail(res)
        else:
            assertEqual(res[100:150], 'nType="Anti-IgG (PEG)" TestSpec="08 ABSCR4 IgG" Du')

        # Make it a bad file.
        s = s.replace('ColumnType=', '')
        res = format_xml(s, 4)
        assertEqual(res, "Error: not well-formed (invalid token): line 6, column 4")


    #------------------------------------------------------------
    # def test_format_c(self):

    fn = os.path.join(my_dir, 'messy.c')
    with open(f'{fn}', 'r') as fp:
        # The happy path.
        s = fp.read()
        res = format_cx(s, 'C', 4)
        assertEqual(res[450:475], '[1] = (val >> 8) & 0xFF;\n')


    #------------------------------------------------------------
    # def test_format_cs(self):

    fn = os.path.join(my_dir, 'messy.cs')
    with open(f'{fn}', 'r') as fp:
        # The happy path.
        s = fp.read()

        res = format_cx(s, 'C#', 4)
        assertEqual(res[700:738], '\n    public Dumper(TextWriter writer)\n')


'''
# SbotFormat doc


Sublime Text plugin to do simple formatting of common source code files. Doesn't replace the existing file,
shows the content in a new view.

- Prettify json, turns C/C++ style comments into valid json elements, and removes trailing commas.
- Prettify xml.
- Prettify C family (C/C++/C#) files using [AStyle](https://astyle.sourceforge.net/) (which must be installed and in your path). Note: I started with the python astyle module but didn't care for it.
- Prettify lua - uses main code from [LuaFormat](https://github.com/floydawong/LuaFormat) (MIT license). Gets a bit confused sometimes.

**NOTE:** LSP works much better for json and lua and should be preferred. Keeping this code here for now.

Built for ST4 on Windows. Linux and OSX should be ok but are minimally tested - PRs welcome.


## Commands and Menus

| Command                  | Description                   | Args             |
| :--------                | :-------                      | :--------        |
| sbot_format_json         | Format json content           |                  |
| sbot_format_xml          | Format xml content            |                  |
| sbot_format_cx_src       | Format C/C++/C# content       |                  |
| sbot_format_lua          | Format lua content            |                  |


There is no default `Context.sublime-menu` file in this plugin.
Add the commands you like to your own `User\Context.sublime-menu` file. Typical entries are:
``` json
{ "caption": "Format",
    "children":
    [
        { "caption": "Format C/C++/C#", "command": "sbot_format_cx_src" },
        { "caption": "Format json", "command": "sbot_format_json" },
        { "caption": "Format xml", "command": "sbot_format_xml" },
        { "caption": "Format lua", "command": "sbot_format_lua" },
    ]
}
```

## Settings

| Setting            | Description         | Options                                     |
| :--------          | :-------            | :------                                     |
| tab_size           | Spaces per tab      | Currently applies to all file types         |
'''
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------
def _frame_formatter(frame, stkpos=-1):
    if stkpos >= 0:
        # extra info please
        s = f'stkpos:{stkpos} file:{frame.filename} func:{frame.name} lineno:{frame.lineno} line:{frame.line}'
    else:
        s = f'file:{frame.filename} func:{frame.name} lineno:{frame.lineno} line:{frame.line}'
    # Other frame.f_code attributes:
    # co_filename, co_firstlineno, co_argcount, co_name, co_varnames, co_consts, co_names
    # co_cellvars, co_freevars, co_kwonlyargcount, co_posonlyargcount, co_nlocals, co_stacksize
    return s


#-----------------------------------------------------------------------------------
def _dump_stack(stkpos=1):
    # Default is caller frame -> 1.

    buff = []

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

    # Get most recent frame => traceback.extract_tb(tb)[:-1], traceback.extract_stack()[:-1]

    for frame in traceback.extract_stack():
        buff.append(f'{_frame_formatter(frame)}')

    return buff


#-----------------------------------------------------------------------------------
def excepthook(type, value, tb):
    '''
    Process unhandled exceptions. This catches for all current plugins and is mainly
    used for debugging the sbot pantheon. Logs the full stack and pops up a message box
    with summary.
    '''

    # This happens with hard shutdown of SbotPdb: BrokenPipeError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError.
    if issubclass(type, bdb.BdbQuit) or issubclass(type, ConnectionError):
        return

    # Sometimes gets these on shutdown:
    # FileNotFoundError '...Log\plugin_host-3.8-on_exit.log'
    # if issubclass(type, FileNotFoundError) and 'plugin_host-3.8-on_exit.log' in str(value):
    #     return

    # LSP is sometimes impolite when closing.
    # 2024-10-03 13:03:31.177 ERR sbot_dev.py:384 Unhandled exception TypeError: 'NoneType' object is not iterable
    # if type is TypeError and 'object is not iterable' in str(value):
    #     return

    # Crude shutdown detection.
    if len(sublime.windows()) > 0:
        msg = f'Unhandled exception {type.__name__}: {value}\nSee the log or ST console'
        sc.error(msg, tb)

    # Otherwise revert to original hook.
    sys.__excepthook__(type, value, tb)


#-----------------------------------------------------------------------------------
#----------------------- Finish initialization -------------------------------------
#-----------------------------------------------------------------------------------

# Connect the last chance hook.
sys.excepthook = excepthook


