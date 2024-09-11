echo off

:: Run unit tests from the command line. MY_PATH=%~dp0
rem set ST_PKGS="%APPDATA%\Sublime Text\Packages"
set PYTHONPATH=%~dp0test_files;%~dp0st_sim;

rem python test_sbot.py
rem exit

:: Execute from the parent dir ST_PKGS.
pushd ..
:: Execute all tests in a suite.
python SbotDev\test_sbot.py
:: Restore
popd
