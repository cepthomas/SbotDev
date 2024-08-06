import sys
from .sbot_common_master import *  # noqa: F403
from .sbot_trace import *  # noqa: F403


#-------------------------- trace test code --------------------------------------

class a_test_class(object):
    def __init__(self, arg):
        T(f'making one a_test_class:{arg}')
        #>>> T('making one a_test_class, arg')
        self._arg = arg

    @traced_function
    def test_class_do_something(self, arg2):
        res = f'{self._arg}-glom-{arg2}'  #OK user formatted string
        return res


def a_traceless_function(s):
    T(f'I got this:{s}')
    #>>> T('I got this!', s)


@traced_function
def a_test_function(a1: int, a2: float):
    cl1 = a_test_class(a1)
    cl2 = a_test_class(a2)
    ret = f'answer is cl1:{cl1.test_class_do_something(a1)}...cl2:{cl2.test_class_do_something(a2)}'
    return ret


@traced_function
def do_a_suite(pre, it):
    '''Do a test suite.'''
    T('something sweet')
    ret = a_test_function(5, 9.126)
    # error_function(0)
    a_traceless_function('can you see me?')
    return ret


@traced_function
def error_function(denom):
    return 1 / denom


#-------------------------- test start here --------------------------------

def do_it():
    start_trace('dev')

    time_str = f'{str(datetime.datetime.now())}'[0:-3]
    T(f'!!! Start test {time_str}')
    # T('!!! Start test, time_str')
    do_a_suite(pre='abcd', it=911)
    T(do_a_suite.__name__)
    T(do_a_suite.__doc__)

    stop_trace()
    
do_it()


# 2024-08-05 15:14:09.644 INF notr.py:512 Opened project file C:\Users\cepth\OneDrive\OneDriveDocuments\notes\main.nproj

# Output:
# 0000.054 do_it:54 !!! Start test 2024-08-06 10:07:24.074


# 0000.182 do_a_suite:enter kwarg pre:abcd kwarg it:911


# 0000.211 do_a_suite:36 something sweet


# 0000.269 a_test_function:enter arg0:5 arg1:9.126


# 0000.296 a_test_class.__init__:10 making one a_test_class:5


# 0000.330 a_test_class.__init__:10 making one a_test_class:9.126


# 0000.378 test_class_do_something:enter arg0:<SbotDev.trace_test.a_test_class object at 0x000002D2BAB3DC10> arg1:5


# 0000.409 test_class_do_something:exit stat:0 res:5-glom-5 type:<class 'str'>


# 0000.448 test_class_do_something:enter arg0:<SbotDev.trace_test.a_test_class object at 0x000002D2BAB3DA90> arg1:9.126
# 0000.511 test_class_do_something:exit stat:0 res:9.126-glom-9.126 type:<class 'str'>
# 0000.543 a_test_function:exit stat:0 res:answer is cl1:(0, '5-glom-5')...cl2:(0, '9.126-glom-9.126') type:<class 'str'>
# 0000.571 a_traceless_function:21 I got this:can you see me?
# 0000.604 do_a_suite:exit stat:0 res:(0, "answer is cl1:(0, '5-glom-5')...cl2:(0, '9.126-glom-9.126')") type:<class 'tuple'>
# 0000.625 do_it:56 do_a_suite
# 0000.645 do_it:57 Do a test suite.
