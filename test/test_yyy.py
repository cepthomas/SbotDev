import sys
import os
import time
import traceback
import functools
import platform
import datetime
import inspect

# Just for import experiments.

# The trace file.
_just_a_var = 200


print(f'>>> loaded {__name__}')


#---------------------------------------------------------------------------
def plugin_loaded():
    '''Called per plugin instance.'''
    global _just_a_var
    _just_a_var += 1
    print(f'>>> plugin_loaded(): {__name__}')


#---------------------------------------------------------------------------
def do_test_func_yyy(msg):
    '''Test.'''
    global _just_a_var
    _just_a_var += 1
    print(f'>>> do_test_func_yyy({msg}):{_just_a_var}')

