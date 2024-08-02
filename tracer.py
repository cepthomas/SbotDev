
import sys
import os
import subprocess
import platform
import time
import sublime
import sublime_plugin
from . import sbot_common as sc

from . import remote_pdb

DEV_SETTINGS_FILE = "SbotDev.sublime-settings"



class _context(object):
    ''' One scoped context. '''

    def __init__(self, arg=None):  # args?
        self._arg = arg
        self._trace(f'ENTER')  # <module>

    def __call__(self, arg=None):  # args?
        self._trace(f'CALL({arg})')
        pass

    def __del__(self):
        # func or file, line
        self._trace(f'EXIT')

    def _trace(self, msg):
        elapsed = time.perf_counter_ns() - _start_count
        msec = elapsed // 1000000
        usec = elapsed // 1000
        frame = sys._getframe(2)
        # fn = os.path.basename(frame.f_code.co_filename)  # string
        # mod_name = frame.f_globals['__name__']  # SbotDev.sbot_dev

        # print(dir(frame.f_code))

        if 'self' in frame.f_locals:
            class_name = frame.f_locals['self'].__class__.__name__
            func = f'{class_name}.{frame.f_code.co_name}'
        else:
            func = frame.f_code.co_name

        s = f'{msec:04}.{usec:03} {func}({frame.f_lineno}) {msg}\n'

        # Write the record.
        # t1 = time.perf_counter_ns()
        _ftrace.write(s)
        # t2 = time.perf_counter_ns()
        # sys.stdout.write(s)
        # sys.stdout.flush()
        # t3 = time.perf_counter_ns()
        # print(f'{(t2-t1)/1000000}  {(t3-t2)/1000000}')



#---------------------------------------------------------------------------
#-------------------------- test code --------------------------------------
#---------------------------------------------------------------------------

class a_test_class(object):

    def __init__(self, arg):
        self._arg = arg
        C = _context(arg)

    def do_something(self, arg2):
        C = _context()
        res = f'{self._arg}-glom-{arg2}'
        C()
        return res

 
def a_test_function(a1: int, a2: float):
    C = _context(222)
    C('test1')
    cl1 = a_test_class(a1)
    cl2 = a_test_class(a2)
    C()
    return f'answer is cl1:{cl1.do_something(a1)}...cl2:{cl2.do_something(a2)}'


def a_suite():
    C = _context(111)
    C('ct1')
    res = a_test_function(5, 9.126)
    print(res)


#---------------------------------------------------------------------------
#-------------------------- gogogo! ----------------------------------------
#---------------------------------------------------------------------------

# TODO1 linux too?
_start_count = time.perf_counter_ns()

# Open file now. Doing it on every write is too expensive.
with open(sc.get_store_fn('trace.txt'), "a") as _ftrace:
    a_suite()



# print('====frame====')
# for attr in dir(frame):
#     print(f'{attr} = {getattr(frame, attr)}')

# ====frame====
# f_back = <frame at 0x0000025A5C291380, file 'C:\\Users\\cepth\\AppData\\Roaming\\Sublime Text\\Packages\\SbotDev\\tracer.py', line 126, code <module>>
# f_code = <code object a_test_function at 0x0000025A5CEFCD40, file "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\tracer.py", line 102>
# f_lasti = 28
# f_lineno = 107
# f_locals = {'a1': 5, 'a2': 9.126,
#    'C': <SbotDev.tracer._context object at 0x0000025A5C3F2D60>,
#    'cl1': <SbotDev.tracer.a_test_class object at 0x0000025A5C3F37F0>}
# f_trace = None
# f_trace_lines = True
# f_trace_opcodes = False



# print('====frame.f_code====')
# for attr in dir(frame.f_code):
#     print(f'{attr} = {getattr(frame.f_code, attr)}')

# ====frame.f_code====
# co_argcount = 2
# co_cellvars = ()
# co_code = b't\x00d\x01\x83\x01}\x02|\x02d\x02\x83\x01\x01\x00t\x01|\x00\x83\x01}\x03t\x01|\x01\x83\x01}\x04|\x02\x83\x00\x01\x00d\x03|\x03\xa0\x02|\x00\xa1\x01\x9b\x00d\x04|\x04\xa0\x02|\x01\xa1\x01\x9b\x00\x9d\x04S\x00'
# co_consts = (None, 222, 'test1', 'answer is cl1:', '...cl2:')
# co_filename = C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\tracer.py
# co_firstlineno = 102
# co_flags = 67
# co_freevars = ()
# co_kwonlyargcount = 0
# co_lnotab = b'\x00\x01\x08\x01\x08\x02\x08\x01\x08\x02\x06\x02'
# co_name = a_test_function
# co_names = ('_context', 'a_test_class', 'do_something')
# co_nlocals = 5
# co_posonlyargcount = 0
# co_stacksize = 6
# co_varnames = ('a1', 'a2', 'C', 'cl1', 'cl2')
