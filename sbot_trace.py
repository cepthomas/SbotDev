import sys
import os
import time
import traceback
import functools
import platform
import inspect

from .sbot_common_master import *  # noqa: F403


''' TODO1 add:
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

    print(f'_ftrace 2 {_ftrace}')


#---------------------------------------------------------------------------
def stop_trace(): #TODO1 make sure this always gets called!
    '''Stop tracing.'''
    global _ftrace

    if _ftrace is not None:
        _ftrace.flush()
        _ftrace.close()
        _ftrace = None


#---------------------------------------------------------------------------
def T(*msgs):
    '''Trace function for user code.'''
    if _ftrace is not None:
        # Dig out func and line.
        frame = sys._getframe(1)
        if 'self' in frame.f_locals:
            class_name = frame.f_locals['self'].__class__.__name__
            func = f'{class_name}.{frame.f_code.co_name}'
        else:
            func = frame.f_code.co_name  # could be '<module>'

        msgl = []
        for m in msgs:
            msgl.append(m)

        _trace(func, frame.f_lineno, msgl)


#---------------------------------------------------------------------------
def traced_function(f):
    '''Decorator to support function entry/exit tracing.'''

    # Check for enabled.
if _ftrace is None:
    print(f'_ftrace 1 {_ftrace}')
    return f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        msgs = []
        if len(args) > 0:
            for i in range(len(args)):
                msgs.append(f'arg{i}:{args[i]}') # TODO nice to have name but difficult?
        if len(kwargs) > 0:
            for k,v in kwargs.items():
                msgs.append(f'{k}:{v}')

        # s = ' '.join(msgs)
        _trace(f.__name__, 'enter', msgs)

        # Execute the wrapped function.
        res = None
        ret = []
        try:
            res = f(*args, **kwargs)
            ret.append(f'res:{res}')
        except Exception as e:
            # _trace(e)
            _trace(f.__name__, 'exception', [e, traceback.format_exc()])

        _trace(f.__name__, 'exit', ret)
        return res
    return wrapper


#-----------------------------------------------------------------------------------
#---------------------------- Private functions ------------------------------------
#-----------------------------------------------------------------------------------


#---------------------------------------------------------------------------
def _trace(func, line, msgs):
    '''Do one trace record.'''
    elapsed = _get_ns() - _trace_start_time
    msec = elapsed // 1000000
    usec = elapsed // 1000

    parts = []
    parts.append(f'{msec:04}.{usec:03}')
    parts.append(f'{func}:{line}')

    for m in msgs:
        parts.append(f'[{m}]')

    parts.append('\n')
    s = ' '.join(parts)

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
