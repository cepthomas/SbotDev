import sys
import datetime
import importlib

from .stpdb import StPdb
from .SbotCommon import tracer as tr
# Some optional shorthand.
trfunc = tr.trfunc
A = tr.A
T = tr.T
Y = tr.Y

print(f'>>> (re)load {__name__}')

importlib.reload(tr)
# importlib.reload(stpdb)

@trfunc
def test_one_arguments():
    result = Y("hello 1")
    Y("hello 2")


#-------------------------- tracer test code --------------------------------------

class TestClass(object):
    ''' Dummy for testing class function tracing.'''

    # Note: don't use @trfunc on constructor.
    def __init__(self, name, tags, arg):
        '''Construct.'''
        T('making one TestClass', name, tags, arg)
        self._name = name
        self._tags = tags
        self._arg = arg

    @trfunc
    def do_something(self, arg):
        '''Entry/exit is traced with args and return value.'''
        res = f'{self._arg}-user-{arg}'
        return res

    @trfunc
    def do_class_assert(self, arg):
        '''Entry/exit is traced with args and return value.'''
        # StPdb().set_trace()
        A(1 == 2)

    @trfunc
    def do_class_exception(self, arg):
        '''Entry/exit is traced with args and return value.'''
        # StPdb().set_trace()
        x = 1 / 0

    def __str__(self):
        '''Required for readable trace.'''
        s = f'TestClass:{self._name} tags:{self._tags} arg:{self._arg}'
        return s

def a_traceless_function(s):
    '''Entry/exit is not traced but explicit traces are ok.'''
    T(f'I still can do this => "{s}"')

@trfunc
def another_test_function(a_list, a_dict):
    '''Entry/exit is traced with args and return value.'''
    return len(a_list) + len(a_dict)

@trfunc
def a_test_function(a1: int, a2: float):
    '''Entry/exit is traced with args and return value.'''
    cl1 = TestClass('number 1', [45, 78, 23], a1)
    cl2 = TestClass('number 2', [100, 101, 102], a2)
    T(cl1)
    T(cl2)
    ret = f'answer is cl1:{cl1.do_something(a1)}...cl2:{cl2.do_something(a2)}'

    ret = f'{cl1.do_class_assert(a1)}'

    ret = f'{cl1.do_class_exception(a2)}'
    return ret

@trfunc
def test_exception_function():
    '''Cause exception and handling.'''
    i = 0
    return 1 / i

@trfunc
def test_assert_function():
    '''Assert processing.'''
    i = 10
    j = 10

    A(i == j)  # ok - no trace
    i += 1
    A(i == j)  # assert

@trfunc
def do_a_suite(alpha, number):
    '''Make a nice suite with entry/exit and return value.'''
    T('something sweet')

    # StPdb().set_trace()

    ret = a_test_function(5, 9.126)

    test_exception_function()

    test_assert_function()

    a_traceless_function('can you see me?')
    ret = another_test_function([33, 'tyu', 3.56], {'aaa': 111, 'bbb': 222, 'ccc': 333})
    return ret


#----------------------------------------------------------
def do_trace_test(trace_fn):
    '''Test starts here.'''

    tr.start(trace_fn, clean_file=True, stop_on_exception=True, sep=('(', ')'))

    T(f'Start {do_a_suite.__name__}:{do_a_suite.__doc__}', str(datetime.datetime.now()))
    do_a_suite(number=911, alpha='abcd')  # named args
    tr.stop()  # Always clean up resources!!


# Output looks like this - stop on error is false:
# 0000.021 do_trace_test:136 (Start do_a_suite:Make a nice suite with entry/exit and return value.) (2024-08-15 12:42:28.108274)
# 0000.045 do_a_suite:enter (number:911) (alpha:abcd)
# 0000.054 do_a_suite:112 (something sweet)
# 0000.073 a_test_function:enter (5) (9.126)
# 0000.085 TestClass.__init__:40 (making one TestClass) (number 1) ([45, 78, 23]) (5)
# 0000.098 TestClass.__init__:40 (making one TestClass) (number 2) ([100, 101, 102]) (9.126)
# 0000.109 a_test_function:84 (TestClass:number 1 tags:[45, 78, 23] arg:5)
# 0000.118 a_test_function:85 (TestClass:number 2 tags:[100, 101, 102] arg:9.126)
# 0000.130 TestClass.do_something:enter (TestClass:number 1 tags:[45, 78, 23] arg:5) (5)
# 0000.136 TestClass.do_something:exit (5-user-5)
# 0000.145 TestClass.do_something:enter (TestClass:number 2 tags:[100, 101, 102] arg:9.126) (9.126)
# 0000.151 TestClass.do_something:exit (9.126-user-9.126)
# 0000.159 TestClass.do_class_assert:enter (TestClass:number 1 tags:[45, 78, 23] arg:5) (5)
# 0000.169 TestClass.do_class_assert:56:assert
# 0000.180 TestClass.do_class_exception:enter (TestClass:number 1 tags:[45, 78, 23] arg:5) (9.126)
# 0000.654 do_class_exception:63 (exception: division by zero)
# 0000.665 a_test_function:exit (None)
# 0000.671 test_exception_function:enter
# 0000.780 test_exception_function:97 (exception: division by zero)
# 0000.789 test_assert_function:enter
# 0000.798 test_assert_function:107:assert
# 0000.805 a_traceless_function:72 (I still can do this => "can you see me?")
# 0000.817 another_test_function:enter ([33, 'tyu', 3.56]) ({'aaa': 111, 'bbb': 222, 'ccc': 333})
# 0000.824 another_test_function:exit (6)
# 0000.828 do_a_suite:exit (6)
