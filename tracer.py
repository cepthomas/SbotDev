import sys
import os
import subprocess
import platform
import functools
import time
import datetime
import sublime
import inspect
import traceback
import sublime_plugin
from . import sbot_common as sc
# from . import remote_pdb


#---------------------------------------------------------------------------
def _dump_me(stkpos=1):  # caller
    buff = []
    frame = sys._getframe(stkpos)
    co = frame.f_code
    buff.append(f'>>>>>> co_filename:{co.co_filename}')
    buff.append(f'frame.f_locals:{frame.f_locals}')
    buff.append(f'frame.f_lineno:{frame.f_lineno}')
    buff.append(f'co_firstlineno:{co.co_firstlineno}')
    buff.append(f'co_argcount:{co.co_argcount}')
    buff.append(f'co_consts:{co.co_consts}')
    buff.append(f'co_name:{co.co_name}')
    buff.append(f'co_names:{co.co_names}')
    buff.append(f'co_varnames:{co.co_varnames}')
    # co_argcount = 2
    # co_cellvars = ()
    # co_freevars = ()
    # co_kwonlyargcount = 0
    # co_posonlyargcount = 0
    # co_nlocals = 5
    # co_stacksize = 6

    # fn = os.path.basename(frame.f_code.co_filename)  # string
    # mod_name = frame.f_globals['__name__']  # SbotDev.sbot_dev

    return '\n'.join(buff)


#-------------------------- trace code --------------------------------------

#---------------------------------------------------------------------------
def _trace(msg, stkpos=None):
    '''Do one trace record. if stkpos not None determine the function/line info too.'''
    elapsed = time.perf_counter_ns() - _start_count
    msec = elapsed // 1000000
    usec = elapsed // 1000

    # for i in [1,2,3,4,5]:
    #     frame = sys._getframe(i)
    #     print(f'+{i}+ {frame.f_code.co_name} {frame.f_lineno}')

    if stkpos is not None:
        frame = sys._getframe(stkpos)
        if 'self' in frame.f_locals:
            class_name = frame.f_locals['self'].__class__.__name__
            func = f'{class_name}.{frame.f_code.co_name}'
        else:
            func = frame.f_code.co_name  # could be '<module>'
        s = f'{msec:04}.{usec:03} {func}({frame.f_lineno}) {msg}\n'
    else:
        s = f'{msec:04}.{usec:03} {msg}\n'

    # Write the record.
    _ftrace.write(s)


_start_count = 0
#---------------------------------------------------------------------------
def init_trace():
    _start_count = time.perf_counter_ns()  # TODO support linux


#---------------------------------------------------------------------------
def T(msg):
    '''Trace function for user sprinkling through code.'''
    _trace(msg, 2)
    # print(f'TRACE:{msg}')


#---------------------------------------------------------------------------
def traced_function(f):
    '''Decorator to support function entry/exit tracing.'''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        parts = [f'{f.__name__}(enter)']
        if len(args) > 0:
            parts.append(f'args:{args}')
        if len(kwargs) > 0:
            parts.append(f'kwargs:{kwargs}')
        _trace(' '.join(parts))

        stat = 0
        res = None
        try:
            res = f(*args, **kwargs)
        except Exception as e:
            # _trace(str(e))
            _trace(traceback.format_exc())
            stat = 1

        _trace(f'{f.__name__}(exit) stat:{stat} res:{res} type:{type(res)}')
        return (stat, res)
    return wrapper


#-------------------------- test code --------------------------------------

class a_test_class(object):
    def __init__(self, arg):
        T(f'making a class:{arg}')
        self._arg = arg

    @traced_function
    def test_class_do_something(self, arg2):
        res = f'{self._arg}-glom-{arg2}'
        return res


def a_traceless_function(s):
    T(f'I got this:{s}')


@traced_function
def a_test_function(a1: int, a2: float):
    cl1 = a_test_class(a1)
    cl2 = a_test_class(a2)
    T(f'function:{a1 + a2}')
    ret = f'answer is cl1:{cl1.test_class_do_something(a1)}...cl2:{cl2.test_class_do_something(a2)}'
    return ret


@traced_function
def do_a_suite():
    '''Do a test suite.'''
    T('something sweet')
    ret = a_test_function(5, 9.126)
    # error_function(0)
    a_traceless_function('help!')
    return ret


@traced_function
def error_function(denom):
    return 1 / denom


#-------------------------- test start here --------------------------------

# Open file now. Doing it on every write is too expensive. TODO1 clean like logger
with open(sc.get_store_fn('sbot.trc'), "a") as _ftrace:
    init_trace()
    time_str = f'{str(datetime.datetime.now())}'[0:-3]
    T(f'>>>>>>>> Start test {time_str}')
    do_a_suite()
    T(do_a_suite.__name__)
    T(do_a_suite.__doc__)
