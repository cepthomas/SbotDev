echo off

:: Run unit tests from the command line. MY_PATH=%~dp0
set PYTHONPATH=%~dp0test_files;%~dp0st_sim;
:: Execute from the parent dir ST_PKGS="%APPDATA%\Sublime Text\Packages".
pushd ..
:: Execute all tests in a suite.  test_sbot.py  test_table.py  test_tracer.py
python SbotDev\test_sbot.py
:: Restore
popd
