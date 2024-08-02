import sys
import os
import subprocess
import platform
import sublime
import sublime_plugin
from . import sbot_common as sc


class SomeClass(object):
    # https://www.pythonlikeyoumeanit.com/Module4_OOP/Special_Methods.html
    # https://docs.python.org/3/reference/datamodel.html#special-method-names

    # def __new__(cls, arg1):
    #     # Called to create a new instance of class cls. __new__() is a static method (special-cased so you need not
    #     # declare it as such) that takes the class of which an instance was requested as its first argument.
    #     # The remaining arguments are those passed to the object constructor expression (the call to the class).
    #     # The return value of __new__() should be the new object instance (usually an instance of cls).
    #     print(f'new')

    def __init__(self, arg1):
        # Called after the instance has been created (by __new__()), but before it is returned to the caller.
        # If a base class has an __init__() method, the derived class’s __init__() method, if any, must explicitly
        # call it to ensure proper initialization of the base class part of the instance; for example: super().__init__([args...]).

        # Get caller info.
        frame = sys._getframe(1)
        fn = os.path.basename(frame.f_code.co_filename)
        line = frame.f_lineno
        func = {frame.f_code.co_name}
        # f'mod_name = {frame.f_globals["__name__"]}'
        # f'class_name = {frame.f_locals["self"].__class__.__name__}'
        self.function = func
        print(f'enter {self.function}')

    def __call__(self, a1, a2):
        # Called when the instance is “called” as a function;
        # if this method is defined, x(arg1, arg2, ...) roughly translates to type(x).__call__(x, arg1, ...).
        print(f'call({a1},{a2})')

    def __del__(self):
        # Called when the instance is about to be destroyed. This is also called a finalizer or (improperly) a destructor.
        # If a base class has a __del__() method, the derived class’s __del__() method, if any, must explicitly call
        # it to ensure proper deletion of the base class part of the instance.
        #  Due to the precarious circumstances under which __del__() methods are invoked, exceptions that occur during
        # their execution are ignored, and a warning is printed to sys.stderr instead. 
        print(f'exit {self.function}')

    def __repr__(self):
        # Called by the repr() built-in function to compute the “official” string representation of an object.
        # If at all possible, this should look like a valid Python expression that could be used to recreate an object
        # with the same value (given an appropriate environment).
        # repr(x) invokes x.__repr__(), this is also invoked when an object is returned by a console
        return 'aaaaa'

    def __str__(self):
        # Returns string representation of an object.
        # This method differs from object.__repr__() in that there is no expectation that __str__() return a valid
        # Python expression: a more convenient or concise representation can be used.
        return 'bbbbb'

    def __format__(self, format_spec):
        return 'ccccc'

    def __hash__(self):
        return 999

    # Also Mathematical/Comparison Operators, Container-Like Class
    # def __getitem__(self, key):
    # def __pow__(self, other):
    # def __getattr__(self, name) etc
    # def __len__(self)
    # def __contains__(self, item)

