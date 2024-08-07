import sys
import os
import traceback
import platform
import collections
import datetime
import pathlib
import shutil
import subprocess
import sublime


#-----------------------------------------------------------------------------------
#---------------------------- Public defs ------------------------------------------
#-----------------------------------------------------------------------------------

# Log defs.
LL_ERROR = 0
LL_WARN = 1
LL_INFO = 2
LL_DEBUG = 3


#-----------------------------------------------------------------------------------
#---------------------------- Private fields ---------------------------------------
#-----------------------------------------------------------------------------------

# Internal flag.
_temp_view_id = None

# Log defs.
_LOG_FILE_NAME = 'sbot.log'
_level_to_name = {LL_ERROR: 'ERR', LL_WARN: 'WRN', LL_INFO: 'INF', LL_DEBUG: 'DBG'}
_name_to_level = {v: k for k, v in _level_to_name.items()}
_log_level = LL_INFO
_tell_level = LL_INFO
_log_fn = None


#-----------------------------------------------------------------------------------
#---------------------------- Public logger functions ------------------------------
#-----------------------------------------------------------------------------------

def log_error(message):
    '''Convenience function.'''
    _write_log(LL_ERROR, message)

def log_warn(message):
    '''Convenience function.'''
    _write_log(LL_WARN, message)

def log_info(message):
    '''Convenience function.'''
    _write_log(LL_INFO, message)

def log_debug(message):
    '''Convenience function.'''
    _write_log(LL_DEBUG, message)

def set_log_level(level):
    '''Set current log level.'''
    global _log_level
    _log_level = _convert_log_level(level)

def set_tell_level(level):
    '''Set level to send to stdout.'''
    global _tell_level
    _tell_level = _convert_log_level(level)


#-----------------------------------------------------------------------------------
#---------------------------- Private functions ------------------------------------
#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
def _convert_log_level(level):
    '''Convert arg (str or int) into a valid log level.'''
    new_level = -1
    if type(level) is int:
        new_level = level
    elif type(level) is str:
        if level in _name_to_level:
            new_level = _name_to_level[level]
    if new_level not in _level_to_name:
        raise ValueError(f'Invalid log level: {level}')
    return new_level


#-----------------------------------------------------------------------------------
def _write_log(level, message):
    '''Format a standard message with caller info and log it.'''
    # Gates. Sometimes get stray empty lines.
    if len(message) == 0:
        return
    if len(message) == 1 and message[0] == '\n':
        return
    if level > _log_level:
        return

    # Get caller info.
    frame = sys._getframe(2)
    fn = os.path.basename(frame.f_code.co_filename)
    line = frame.f_lineno
    # f'func = {frame.f_code.co_name}'
    # f'mod_name = {frame.f_globals["__name__"]}'
    # f'class_name = {frame.f_locals["self"].__class__.__name__}'

    slvl = _level_to_name[level] if level in _level_to_name else '???'
    time_str = f'{str(datetime.datetime.now())}'[0:-3]

    # Write the record.
    # I don't think file access needs to be synchronized. ST docs say that API runs on one thread. But?
    with open(_log_fn, 'a') as log:
        out_line = f'{time_str} {slvl} {fn}:{line} {message}'
        log.write(out_line + '\n')
        log.flush()

    # Write to console also?
    if level <= _tell_level:
        out_line = f'>>> {slvl} {fn}:{line} {message}'
        sys.stdout.write(out_line + '\n')
        sys.stdout.flush()

#-----------------------------------------------------------------------------------
#----------------------- Finish initialization -------------------------------------
#-----------------------------------------------------------------------------------

_log_fn = get_store_fn(_LOG_FILE_NAME)

# Maybe roll over log now.
if os.path.exists(_log_fn) and os.path.getsize(_log_fn) > 50000:
    bup = _log_fn.replace('.', '_old.')
    shutil.copyfile(_log_fn, bup)
    # Clear current log file.
    with open(_log_fn, 'w'):
        pass
