import sys
import datetime
from .SbotCommon.tracer import *


#-------------------------- tracer test code --------------------------------------

class TestClass(object):
    ''' Dummy for testing class function tracing.'''

    # TODO don't do this here: @traced_function
    def __init__(self, name, tags, arg):
        '''Construct.'''
        T('making one TestClass', name, tags, arg)
        self._name = name
        self._tags = tags
        self._arg = arg

    @traced_function
    def do_something(self, arg):
        '''Entry/exit is traced with args and return value.'''
        res = f'{self._arg}-user-{arg}'
        return res

    @traced_function
    def do_class_assert(self, arg):
        '''Entry/exit is traced with args and return value.'''
        A(1 == 2)

    @traced_function
    def do_class_exception(self, arg):
        '''Entry/exit is traced with args and return value.'''
        x = 1 / 0

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
    cl2 = TestClass('number 2', [100, 101, 102], a2)
    T(cl1)
    T(cl2)
    ret = f'answer is cl1:{cl1.do_something(a1)}...cl2:{cl2.do_something(a2)}'
    # This blows up.
    ret = f'{cl1.do_class_assert(a1)}'
    ret = f'{cl1.do_class_exception(a2)}'
    return ret

@traced_function
def test_exception_function():
    '''Cause exception and handling.'''
    i = 0
    return 1 / i

@traced_function
def test_assert_function():
    '''Assert processing.'''
    i = 10
    j = 10

    A(i == j)  # ok - no trace
    i += 1
    A(i == j)  # assert

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

# Output looks like this:
# 0000.071 do_trace_test:97 |Start do_a_suite:Make a nice suite with entry/exit and return value.| |2024-08-11 17:56:39.064581|
# 0000.157 do_a_suite:enter |number:911| |alpha:abcd|
# 0000.200 do_a_suite:81 |something sweet|
# 0000.293 a_test_function:enter |5| |9.126|
# 0000.379 TestClass.__init__:14 |making one TestClass| |number 1| |[45, 78, 23]| |5|
# 0000.479 TestClass.__init__:14 |making one TestClass| |number 2| |[100, 101, 102]| |9.126|
# 0000.538 a_test_function:54 |TestClass:number 1 tags:[45, 78, 23] arg:5|
# 0000.601 a_test_function:55 |TestClass:number 2 tags:[100, 101, 102] arg:9.126|
# 0000.738 TestClass.do_something:enter |TestClass:number 1 tags:[45, 78, 23] arg:5| |5|
# 0000.776 TestClass.do_something:exit |5-user-5|
# 0000.838 TestClass.do_something:enter |TestClass:number 2 tags:[100, 101, 102] arg:9.126| |9.126|
# 0000.914 TestClass.do_something:exit |9.126-user-9.126|
# 0000.977 TestClass.do_class_assert:enter |TestClass:number 1 tags:[45, 78, 23] arg:5| |5|
# 0001.1087 TestClass.do_class_assert:28:assert
# 0001.1325 TestClass.do_class_exception:enter |TestClass:number 1 tags:[45, 78, 23] arg:5| |9.126|
# 0003.3679 do_class_exception:33 |exception: division by zero|
# 0003.3740 a_test_function:exit |None|
# 0003.3775 test_exception_function:enter
# 0004.4238 test_exception_function:66 |exception: division by zero|
# 0004.4290 test_assert_function:enter
# 0004.4336 test_assert_function:76:assert
# 0004.4370 a_traceless_function:42 |I still can do this => "can you see me?"|
# 0004.4432 another_test_function:enter |[33, 'tyu', 3.56]| |{'aaa': 111, 'bbb': 222, 'ccc': 333}|
# 0004.4462 another_test_function:exit |6|
# 0004.4487 do_a_suite:exit |6|
