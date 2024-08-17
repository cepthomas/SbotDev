# A remote pdb tailored for specifically debugging sublime text plugins with its non-standard
# embedded python.
# It's mostly hacked from https://github.com/ionelmc/python-remote-pdb with some bits of rpdb.py and pdbx.py.
# Started 8/15/2024.


import errno
import os
import re
import socket
import sys
from pdb import Pdb
from .SbotCommon import logger as log

# print(f'>>> (re)load {__name__}')

DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 4444  # or 0?

USE_ANSI_COLOR = True

COLOR_GRAY   = '\033[90m'
COLOR_RED    = '\033[91m'
COLOR_BLUE   = '\033[94m'
COLOR_YELLOW = '\033[33m'
COLOR_GREEN  = '\033[92m'
COLOR_RESET  = '\033[0m'



#-----------------------------------------------------------------------------------
class FileWrapper(object):
    '''Make socket look like a file. Also handles encoding and line endings.'''
    def __init__(self, conn):
        self.conn = conn
        fh = conn.makefile('rw')
        # Return a file object associated with the socket.
        # https://docs.python.org/3.8/library/socket.html
        self.stream = fh
        self.read = fh.read
        self.readline = fh.readline
        self.readlines = fh.readlines
        self.close = fh.close
        self.flush = fh.flush
        self.fileno = fh.fileno
        self._nl_rex=re.compile('\r?\n')  # Convert all to windows style.
        if hasattr(fh, 'encoding'):
            self._send = lambda data: conn.sendall(data.encode(fh.encoding))
        else:
            self._send = conn.sendall

    def __iter__(self):
        return self.stream.__iter__()

    @property
    def encoding(self):
        return self.stream.encoding

    def write(self, line):
        '''Write line to client. Fix any line endings.'''
        line = self._nl_rex.sub('\r\n', line)

        # Colorize?
        if USE_ANSI_COLOR:
            if '->' in line:
                line = f'{COLOR_YELLOW}{line}{COLOR_RESET}'
            elif '>>' in line:
                line = f'{COLOR_GREEN}{line}{COLOR_RESET}'
            elif '***' in line:
                line = f'{COLOR_RED}{line}{COLOR_RESET}'
            elif 'Error:' in line:
                line = f'{COLOR_RED}{line}{COLOR_RESET}'
            elif '>' in line:
                line = f'{COLOR_BLUE}{line}{COLOR_RESET}'
        self._send(line)

    def writelines(self, lines):
        '''Write all to client.'''
        for line in lines:
            self.write(line)


#-----------------------------------------------------------------------------------
class StPdb(Pdb):
    '''Run pdb behind a blocking telnet server.'''
    active_instance = None

    def __init__(self, host, port):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        listen_socket.bind((host, port))
        log.info(f'StPdb session open at {listen_socket.getsockname()}, waiting for connection.')
        listen_socket.listen(1)
        conn, address = listen_socket.accept()
        log.info(f'StPdb accepted connection from {repr(address)}.')
        self.handle = FileWrapper(conn)
        Pdb.__init__(self, completekey='tab', stdin=self.handle, stdout=self.handle)
        StPdb.active_instance = self

    def __restore(self):
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

    # do_q = do_exit = do_quit  # TODO what?


#-----------------------------------------------------------------------------------
def set_trace(host=DEFAULT_ADDR, port=DEFAULT_PORT):
    '''Opens a remote PDB using import stpdb; stpdb.set_trace() syntax.'''
    rdb = StPdb(host=host, port=port)
    rdb.set_trace(frame=sys._getframe().f_back)
