import sys
import datetime
from .SbotCommon.tracer import *


#-------------------------- tracer test code --------------------------------------

class TestClass(object):
    ''' Dummy for testing class function tracing.'''

    def __init__(self, name, tags, arg):
        '''Construct.'''
        T('making one TestClass', name, tags, arg)
        self._name = name
        self._tags = tags
        self._arg = arg

    @traced_function
    def test_class_do_something(self, arg2):
        '''Entry/exit is traced with args and return value.'''
        res = f'{self._arg}-user-{arg2}'
        return res

    def __str__(self):
        '''Required for readable trace.'''
        s = f'TestClass:{self._name} tags:{self._tags} arg:{self._arg}'
        return s


def a_traceless_function(s):
    '''Entry/exit is not traced but explicit traces are ok.'''
    T(f'I still can do this => "{s}"')


@traced_function
def another_test_function(a_list, a_dict):
    '''Entry/exit is traced with args and return value.'''
    return len(a_list) + len(a_dict)


@traced_function
def a_test_function(a1: int, a2: float):
    '''Entry/exit is traced with args and return value.'''
    cl1 = TestClass('number 1', [45, 78, 23], a1)
    T(cl1)
    cl2 = TestClass('number 2', [100, 101, 102], a2)
    T(cl2)
    ret = f'answer is cl1:{cl1.test_class_do_something(a1)}...cl2:{cl2.test_class_do_something(a2)}'
    return ret


@traced_function
def test_exception_function():
    '''Cause exception and handling.'''
    i = 0
    return 1 / i
# 0000.533 test_exception_function:enter
# 0002.2359 test_exception_function:exception |Traceback (most recent call last):
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\SbotCommon\tracer.py", line 115, in wrapper
#     res = f(*args, **kwargs)
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\test_tracer.py", line 57, in test_exception_function
#     return 1 / i
# ZeroDivisionError: division by zero
# |


@traced_function
def test_assert_function():
    '''Assert processing.'''
    i = 10
    j = 10

    A(i == j)  # ok - no trace
    i += 1
    A(i == j)  # assert

# stkpos = 3
# 0000.936 test_assert_function:enter
# 0001.1087 test_assert_function:exception |Traceback (most recent call last):
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\SbotCommon\tracer.py", line 123, in wrapper
#     res = f(*args, **kwargs)
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\test_tracer.py", line 75, in test_assert_function
#     A(i == j)  # assert
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\SbotCommon\tracer.py", line 96, in A
#     raise AssertionError(site)
# AssertionError: test_assert_function:75
# |


@traced_function
def do_a_suite(alpha, number):
    '''Make a nice suite with entry/exit and return value.'''
    T('something sweet')
    ret = a_test_function(5, 9.126)

    test_exception_function()

    test_assert_function()

    a_traceless_function('can you see me?')
    ret = another_test_function([33, 'tyu', 3.56], {'aaa': 111, 'bbb': 222, 'ccc': 333})
    return ret


#----------------------------------------------------------

def do_trace_test(trace_fn):
    '''Test starts here.'''
    start_trace(trace_fn)

    T(f'Start {do_a_suite.__name__}:{do_a_suite.__doc__}', str(datetime.datetime.now()))
    do_a_suite(number=911, alpha='abcd')  # named args
    stop_trace()  # Always clean up resources!!

    # try:
    #     T(f'Start {do_a_suite.__name__}:{do_a_suite.__doc__}', str(datetime.datetime.now()))
    #     do_a_suite(number=911, alpha='abcd')  # named args
    # except:
    #     pass
    # finally:
    #     stop_trace()  # Always clean up resources!!


# Output looks like this:
# 
