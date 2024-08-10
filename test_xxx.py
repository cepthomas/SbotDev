import sys
import os
import time
import traceback
import functools
import platform
import datetime
import inspect

# Just for import experiments.

# The trace file.
_just_a_var = None

print(f'XXX loaded test_xxx.py  {str(datetime.datetime.now())}')


#---------------------------------------------------------------------------
def plugin_loaded():
    ''' Called once per plugin instance. Each module/file can have its own. '''
    print(f'XXX plugin_loaded(): {__name__}')


#---------------------------------------------------------------------------
def do_something(msg):#trace_fn, clean_file=True):
    global _just_a_var

    print(f'XXX do_something({msg})---{_just_a_var}')

