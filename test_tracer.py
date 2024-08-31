import sys
import os
import datetime
import importlib
from . import tracer as tr

# Benign reload in case of edited.
importlib.reload(tr)


# Some optional shorthand.
trfunc = tr.trfunc
A = tr.A
T = tr.T


#-------------------------- tracer test code --------------------------------------

class TestClass(object):
    ''' Dummy for testing class function tracing.'''

    # Note: don't use @trfunc on constructor!
    def __init__(self, name, tags, arg):
        '''Construction.'''
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
        A(1 == 2)

    @trfunc
    def do_class_exception(self, arg):
        '''Entry/exit is traced with args and return value.'''
        x = 1 / 0

    def __str__(self):
        '''Required for readable trace.'''
        s = f'TestClass:{self._name} tags:{self._tags} arg:{self._arg}'
        return s

def no_trfunc_function(s):
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

    ret = a_test_function(5, 9.126)

    test_exception_function()

    test_assert_function()

    no_trfunc_function('can you see me?')
    ret = another_test_function([33, 'tyu', 3.56], {'aaa': 111, 'bbb': 222, 'ccc': 333})
    return ret

def do_trace_test():
    '''Test starts here.'''
    trace_fn = os.path.join(os.path.dirname(__file__), '_tracer.log')
    tr.start(trace_fn, clean_file=True, stop_on_exception=True, sep=('(', ')'))

    T(f'Start {do_a_suite.__name__}:{do_a_suite.__doc__}', str(datetime.datetime.now()))
    do_a_suite(number=911, alpha='abcd')  # named args
    tr.stop()  # Always clean up resources!!

# Uncomment this to run.
# do_trace_test()


# Output looks like this - stop on error is false:
# 0000.016 do_trace_test:118 (Start do_a_suite:Make a nice suite with entry/exit and return value.) (2024-08-19 10:20:02.624956)
# 0000.035 do_a_suite:enter (number:911) (alpha:abcd)
# 0000.044 do_a_suite:98 (something sweet)
# 0000.056 a_test_function:enter (5) (9.126)
# 0000.065 TestClass.__init__:28 (making one TestClass) (number 1) ([45, 78, 23]) (5)
# 0000.078 TestClass.__init__:28 (making one TestClass) (number 2) ([100, 101, 102]) (9.126)
# 0000.087 a_test_function:70 (TestClass:number 1 tags:[45, 78, 23] arg:5)
# 0000.095 a_test_function:71 (TestClass:number 2 tags:[100, 101, 102] arg:9.126)
# 0000.106 TestClass.do_something:enter (TestClass:number 1 tags:[45, 78, 23] arg:5) (5)
# 0000.111 TestClass.do_something:exit (5-user-5)
# 0000.119 TestClass.do_something:enter (TestClass:number 2 tags:[100, 101, 102] arg:9.126) (9.126)
# 0000.125 TestClass.do_something:exit (9.126-user-9.126)
# 0000.132 TestClass.do_class_assert:enter (TestClass:number 1 tags:[45, 78, 23] arg:5) (5)
# 0000.141 TestClass.do_class_assert:43:assert
# 0000.151 TestClass.do_class_exception:enter (TestClass:number 1 tags:[45, 78, 23] arg:5) (9.126)
# 0000.612 do_class_exception:49 (exception: division by zero)
# 0000.622 a_test_function:exit (None)
# 0000.629 test_exception_function:enter
# 0000.717 test_exception_function:83 (exception: division by zero)
# 0000.728 test_assert_function:enter
# 0000.739 test_assert_function:93:assert
# 0000.745 no_trfunc_function:58 (I still can do this => "can you see me?")
# 0000.757 another_test_function:enter ([33, 'tyu', 3.56]) ({'aaa': 111, 'bbb': 222, 'ccc': 333})
# 0000.763 another_test_function:exit (6)
# 0000.767 do_a_suite:exit (6)
