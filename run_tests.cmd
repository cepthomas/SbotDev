
cls

echo off
TODO1 fix this
del "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\User\_Test\trace.txt"

rem :: Run unit tests from the command line. MY_PATH=%~dp0
rem set PYTHONPATH=%~dp0test_files;%~dp0st_sim;
rem :: Execute from the parent dir ST_PKGS="%APPDATA%\Sublime Text\Packages".
rem pushd ..
rem :: Execute all tests in a suite.  test_sbot.py  test_table.py  test_tracer.py
rem python SbotDev\test_sbot.py
rem :: Restore
rem popd

pushd ..\SbotDev\tests
python -m unittest test_common test_tracer
popd

rem pushd ..\SbotResiduum\tests
rem python -m unittest test_residuum
rem popd

pushd ..\Notr\tests
python -m unittest test_notr test_table
popd

pushd ..\SbotFormat\tests
python -m unittest test_format
popd

rem pushd ..\SbotHighlight\tests
rem python -m unittest test_highlight
rem popd

rem pushd ..\SbotRender\tests
rem python -m unittest test_render
rem popd

rem pushd ..\SbotSignet\tests
rem python -m unittest test_signet
rem popd
