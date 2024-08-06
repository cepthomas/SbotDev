import sys
import os
import time
import traceback
import functools
import platform
# import datetime
import inspect
# import pathlib
# import shutil
# import subprocess
# import sublime

from .sbot_common_master import *  # noqa: F403


''' TODO add:
-----
ic(foo(123))
Prints
ic| foo(123): 456


-----
d = {'key': {1: 'one'}}
ic(d['key'][1])

class klass():
    attr = 'yep'
ic(klass.attr)
Prints
ic| d['key'][1]: 'one'
ic| klass.attr: 'yep'

------
def foo():
    ic()
    first()

    if expression:
        ic()
        second()
    else:
        ic()
        third()
Prints
ic| example.py:4 in foo()
ic| example.py:11 in foo()


------
ic(1)
ic.disable()
ic(2)
ic.enable()
ic(3)


------
temperature = -1
y.assert_(temperature > 0)
This will raise an AttributeError.
But
y.enabled = False
temperature = -1
y.assert_(temperature > 0)
will not.
'''


#-----------------------------------------------------------------------------------
#---------------------------- Private fields ---------------------------------------
#-----------------------------------------------------------------------------------

# The trace file.
_ftrace = None

# For elapsed time stamps.
_trace_start_time = 0

#-----------------------------------------------------------------------------------
#---------------------------- Public trace functions -------------------------------
#-----------------------------------------------------------------------------------

#---------------------------------------------------------------------------
def start_trace(name, clean_file=True):
    '''Enables tracing and optionally clean file (default is True).'''
    global _ftrace
    global _trace_start_time

    stop_trace()  # just in case

    trace_fn = get_store_fn(f'trace_{name}.log')

    if clean_file:
        with open(trace_fn, 'w'):
            pass

    # Open file now. Doing it on every write is too expensive.
    _ftrace = open(trace_fn, 'a')
    _trace_start_time = _get_ns()


#---------------------------------------------------------------------------
def stop_trace(): #TODO1 make sure this gets called!
    '''Stop tracing.'''
    global _ftrace

    if _ftrace is not None:
        _ftrace.flush()
        _ftrace.close()
        _ftrace = None


#---------------------------------------------------------------------------
def T(msg):
    '''Trace function for user code.'''
    if _ftrace is not None:
        _trace(msg, stkpos=2)


#---------------------------------------------------------------------------
def traced_function(f):
    '''Decorator to support function entry/exit tracing.'''
    # Check for enabled.
    if _ftrace is None:
        return f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        parts = []
        parts.append(f'{f.__name__}:enter')

        if len(args) > 0:
            for i in range(len(args)):
                parts.append(f'arg{i}:{args[i]}') # TODO nice to have name?
        if len(kwargs) > 0:
            print(kwargs)
            for k,v in kwargs.items():
                parts.append(f'kwarg {k}:{v}')

        s = ' '.join(parts)
        _trace(s)

        stat = 0
        res = None
        try:
            res = f(*args, **kwargs)
        except Exception as e:
            # _trace(e)
            _trace(traceback.format_exc())
            stat = 1

        _trace(f'{f.__name__}:exit stat:{stat} res:{res} type:{type(res)}')
        return (stat, res)
    return wrapper


#-----------------------------------------------------------------------------------
#---------------------------- Private functions ------------------------------------
#-----------------------------------------------------------------------------------


#---------------------------------------------------------------------------
def _trace(*msgs, **opts):  #stkpos=None):
    '''Do one trace record. if stkpos not None determine the function/line info too.'''
    elapsed = _get_ns() - _trace_start_time
    msec = elapsed // 1000000
    usec = elapsed // 1000

    parts = []
    parts.append(f'{msec:04}.{usec:03}')

    if stkpos is not None:
        frame = sys._getframe(stkpos)
        if 'self' in frame.f_locals:
            class_name = frame.f_locals['self'].__class__.__name__
            func = f'{class_name}.{frame.f_code.co_name}'
        else:
            func = frame.f_code.co_name  # could be '<module>'
        parts.append(f'{func}:{frame.f_lineno}')
    # else:
    #     parts = f'{msec:04}.{usec:03} {msg}\n'

    for m in msgs:
        parts.append(f'{m}')

    parts.append('\n')
    s = ' '.join(parts)
    print(s)

    # Write the record. TODO1 if file is locked by other process notify user that trace is one module only.
    _ftrace.write(s)


#---------------------------------------------------------------------------
def _get_ns():
    '''Get current nanosecond.'''
    if platform.system() == 'Darwin':
        log_error('Sorry, we don\'t do Macs')
    elif platform.system() == 'Windows':
        return time.perf_counter_ns()
    else:  # linux variants
        return time.clock_gettime_ns(time.CLOCK_MONOTONIC)
