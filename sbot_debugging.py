import sys
import os
import subprocess
import platform
import traceback
import bdb
import datetime
import string
import re
import importlib
import socket
import sublime
import sublime_plugin
from . import sbot_common as sc


#-----------------------------------------------------------------------------------
# Setup for running pbot_pdb in this file
# This way:
#  - Copy pbot_pdb.py to this dir and edit to taste.
#    from . import pbot_pdb
# That way:
#  - Clone PyBagOfTricks and add its path to sys.path.
pbot_path = R'C:\Dev\Libs\PyBagOfTricks'
if pbot_path not in sys.path: sys.path.append(pbot_path)
import pbot_pdb


#-----------------------------------------------------------------------------------
class SbotDebugCommand(sublime_plugin.TextCommand):
    ''' '''
    def function2(self, arg):
        x = 111
        y = 22
        return arg + x + y

    def function1(self, arg):
        # Set a breakpoint in here then step through and examine the code.
        sc.info('function1 set breakpoint')

        log_fn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'out', 'spbot.log'))
        try: os.remove(log_fn)
        except: pass

        pbot_pdb.breakpoint(59120, log_fn=log_fn, use_color=True) # turn off color for unit test

        sc.info('function1 done breakpoint')

        res = self.function2(len(arg))
        return res

    def boom(self):
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

    def run(self, edit):
        sc.info('go() enter')

        # Benign reload in case of edited.
        # importlib.reload(pbot_pdb)

        # Run some test code.
        self.function1('ABCD')
        sc.info('go() exit')


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

    # Crude shutdown detection to avoid false positives.
    if len(sublime.windows()) > 0:
        msg = f'Unhandled exception {type.__name__}: {value}'
        sc.error(msg, tb)

    # Otherwise revert to original hook.
    sys.__excepthook__(type, value, tb)


#-----------------------------------------------------------------------------------
# Write to dump file.
def _dump(txt):
    fn = os.path.join(os.path.dirname(__file__), 'out', 'dump.log')
    with open(fn, 'a') as f:
        f.write(txt + '\n')
        f.flush()


#----------------------- Finish initialization -------------------------------------

# Connect the last chance hook.
sys.excepthook = excepthook
