# My hacked version of https://github.com/ionelmc/python-remote-pdb. Started 8/15/2024.

# TODO1 move to SbotCommon?

# TODO1 add colors like debugger.lua? see stpdb.py
# l(ist): An arrow (>) indicates the current frame, which determines the context of most commands.
# 134                     # stpdb.StPdb()  # shorter
# 135  ->                 StPdb().set_trace()
# 136                 except Exception as e:
# Exception line is '>>'.                                |
# 
# w(here): Print a stack trace, with the most recent frame at the bottom. An arrow (>) indicates the current frame,
#    which determines the context of most commands.
#    -> is the code line
#   c:\program files\sublime text\lib\python38\sublime_plugin.py(1687)run_()
# -> return self.run(edit, **args)
#   c:\users\cepth\appdata\roaming\sublime text\packages\sbotdev\sbot_dev.py(137)run()
# -> StPdb().set_trace()
#   c:\users\cepth\appdata\roaming\sublime text\packages\sbotdev\stpdb.py(123)set_trace()
# -> print('$$$ 80')
# > c:\program files\sublime text\lib\python38\sublime.py(31)write()
# -> def write(self, s):
# 
# errors like:
# *** SyntaxError: invalid syntax
# print('Error:', self.orig, 'does not exist')
# print(f"ImportError: {e}")
# self.message('%s = *** undefined ***' % (name,))
# 
# others:
# self.message('[EOF]')

from __future__ import print_function

import errno
import os
import re
import socket
import sys
from pdb import Pdb
from .SbotCommon import logger as log

# TODO1 way to disable all without commenting out? StPdb().set_trace()  with PRODUCTION?

print(f'>>> (re)load {__name__}')

# TODO1 get these from config?
DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 4444  # or 0?


# From rpdb:
# class FileObjectWrapper(object):
#     def __init__(self, fileobject, stdio):
#         self._obj = fileobject
#         self._io = stdio

#     def __getattr__(self, attr):
#         if hasattr(self._obj, attr):
#             attr = getattr(self._obj, attr)
#         elif hasattr(self._io, attr):
#             attr = getattr(self._io, attr)
#         else:
#             raise AttributeError('Attribute %s is not found' % attr)
#         return attr


class FileWrapper(object):
    '''Make socket look like a file. Also handles encoding and both kinds of line endings.'''
    def __init__(self, conn):
        self.conn = conn
        fh = conn.makefile('rw')
        # https://docs.python.org/3.8/library/socket.html
        self.stream = fh
        self.read = fh.read
        self.readline = fh.readline
        self.readlines = fh.readlines
        self.close = fh.close
        self.flush = fh.flush
        self.fileno = fh.fileno
        if hasattr(fh, 'encoding'):
            self._send = lambda data: conn.sendall(data.encode(fh.encoding))
        else:
            self._send = conn.sendall

    def __iter__(self):
        return self.stream.__iter__()

    @property
    def encoding(self):
        return self.stream.encoding

    def write(self, data, nl_rex=re.compile('\r?\n')):
        data = nl_rex.sub('\r\n', data)
        self._send(data)

    def writelines(self, lines, nl_rex=re.compile('\r?\n')):
        for line in lines:
            self.write(line, nl_rex)


class StPdb(Pdb):
    '''Run pdb behind a blocking telnet server.'''
    active_instance = None

    def __init__(self):  #, host, port, patch_stdstreams=False):
        host = DEFAULT_ADDR
        port = DEFAULT_PORT

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        listen_socket.bind((host, port))
        log.info(f'StPdb session open at {listen_socket.getsockname()}, waiting for connection.')
        listen_socket.listen(1)
        conn, address = listen_socket.accept()
        log.info(f'StPdb accepted connection from {repr(address)}.')
        self.handle = FileWrapper(conn)
        Pdb.__init__(self, completekey='tab', stdin=self.handle, stdout=self.handle)
        # self.backup = []
        # if patch_stdstreams:
        #     for name in ('stderr', 'stdout', '__stderr__', '__stdout__', 'stdin', '__stdin__'):
        #         self.backup.append((name, getattr(sys, name)))
        #         setattr(sys, name, self.handle)
        StPdb.active_instance = self

    def __restore(self):
        # if self.backup:
        #     log.info('Restoring streams: {self.backup}.')
        # for name, fh in self.backup:
        #     setattr(sys, name, fh)
        self.handle.close()
        StPdb.active_instance = None

    def set_trace(self, frame=None):
        if frame is None:
            frame = sys._getframe().f_back
        try:
            Pdb.set_trace(self, frame)
        except IOError as exc:
            if exc.errno != errno.ECONNRESET:
                raise

    def do_quit(self, arg):
        self.__restore()
        return Pdb.do_quit(self, arg)

    do_q = do_exit = do_quit  # TODO?


# To use some specific host/port:
#     from remote_pdb import StPdb
#     StPdb('127.0.0.1', 4444).set_trace()
# NOPE To open a remote PDB on first available port:
#     from remote_pdb import set_trace
#     set_trace() # you'll see the port number in the logs
# NOPE To connect just run ``telnet 127.0.0.1 4444``.
# 
# TODO1? When you are finished debugging, either exit the debugger, or press ctrl+] ctrl+d.
# 
# def set_trace(host=None, port=None):  #, patch_stdstreams=False):
#     '''Opens a remote PDB on first available port.'''
#     if host is None:
#         host = os.environ.get('REMOTE_PDB_HOST', '127.0.0.1')
#     if port is None:
#         port = int(os.environ.get('REMOTE_PDB_PORT', '0'))
#     rdb = StPdb(host=host, port=port)  #, patch_stdstreams=patch_stdstreams)
#     rdb.set_trace(frame=sys._getframe().f_back)


# From rpdb:
# def set_trace(addr=DEFAULT_ADDR, port=DEFAULT_PORT, frame=None):
#     """Wrapper function to keep the same import x; x.set_trace() interface.
#     We catch all the possible exceptions from pdb and cleanup.
#     """
#     try:
#         debugger = Rpdb(addr=addr, port=port)
#     except socket.error:
#         if OCCUPIED.is_claimed(port, sys.stdout):
#             # rpdb is already on this port - good enough, let it go on:
#             sys.stdout.write("(Recurrent rpdb invocation ignored)\n")
#             return
#         else:
#             # Port occupied by something else.
#             raise
#     try:
#         debugger.set_trace(frame or sys._getframe().f_back)
#     except Exception:
#         traceback.print_exc()
