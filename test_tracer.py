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
def error_function():
    '''Cause exception and handling.'''
    i = 0
    return 1 / i


@traced_function
def assert_function():
    '''Assert processing.'''
    i = 10
    j = 10

    A(i == j)  # ok
    i += 1
    A(i == j)  # assert


@traced_function
def do_a_suite(alpha, number):
    '''Make a nice suite with entry/exit and return value.'''
    T('something sweet')
    ret = a_test_function(5, 9.126)

    error_function()

    assert_function()

    a_traceless_function('can you see me?')
    ret = another_test_function([33, 'tyu', 3.56], {'aaa': 111, 'bbb': 222, 'ccc': 333})
    return ret



#--------------------------  --------------------------------

def do_trace_test(trace_fn):
    '''Test starts here.'''
    start_trace(trace_fn)
    try:
        T(f'Start {do_a_suite.__name__}:{do_a_suite.__doc__}', str(datetime.datetime.now()))
        do_a_suite(number=911, alpha='abcd')  # named args
    except:
        pass
    finally:
        stop_trace()  # Always clean up resources!!


# Doc Output:
# 0000.071 do_trace_test:94 |Start do_a_suite:Make a nice suite with entry/exit and return value.| |2024-08-10 10:15:58.800860|
# 0000.142 do_a_suite:enter |number:911| |alpha:abcd|
# 0000.175 do_a_suite:74 |something sweet|
# 0000.218 a_test_function:enter |5| |9.126|
# 0000.254 TestClass.__init__:14 |making one TestClass| |number 1| |[45, 78, 23]| |5|
# 0000.299 a_test_function:46 |TestClass:number 1 tags:[45, 78, 23] arg:5|
# 0000.336 TestClass.__init__:14 |making one TestClass| |number 2| |[100, 101, 102]| |9.126|
# 0000.373 a_test_function:48 |TestClass:number 2 tags:[100, 101, 102] arg:9.126|
# 0000.415 test_class_do_something:enter |TestClass:number 1 tags:[45, 78, 23] arg:5| |5|
# 0000.438 test_class_do_something:exit |5-user-5|
# 0000.468 test_class_do_something:enter |TestClass:number 2 tags:[100, 101, 102] arg:9.126| |9.126|
# 0000.493 test_class_do_something:exit |9.126-user-9.126|
# 0000.513 a_test_function:exit |answer is cl1:5-user-5...cl2:9.126-user-9.126|
# 0000.533 error_function:enter
# 0002.2359 error_function:exception |Traceback (most recent call last):
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\SbotCommon\tracer.py", line 115, in wrapper
#     res = f(*args, **kwargs)
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\test_tracer.py", line 57, in error_function
#     return 1 / i
# ZeroDivisionError: division by zero
# |
# 0002.2412 assert_function:enter
# 0002.2957 assert_function:exception |Traceback (most recent call last):
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\SbotCommon\tracer.py", line 115, in wrapper
#     res = f(*args, **kwargs)
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\test_tracer.py", line 68, in assert_function
#     A(i == j)  # assert
#   File "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\SbotDev\SbotCommon\tracer.py", line 88, in A
#     raise AssertionError(site)
# AssertionError: wrapper:115
# |
# 0003.3029 a_traceless_function:33 |I still can do this => "can you see me?"|
# 0003.3084 another_test_function:enter |[33, 'tyu', 3.56]| |{'aaa': 111, 'bbb': 222, 'ccc': 333}|
# 0003.3111 another_test_function:exit |6|
# 0003.3132 do_a_suite:exit |6|
