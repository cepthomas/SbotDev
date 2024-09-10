

:: Run unit tests from the command line.
rem Script drive+path: %~dp0  path only: %~p0
rem Current exec dir: %CD%

cls
echo off

set ST_PKGS="%APPDATA%\Sublime Text\Packages"

set PYTHONPATH=%PYTHONPATH%;%~dp0\test_files;%~dp0\st_sim;%ST_PKGS%\SbotFormat;


rem set TESTER_PATH=%~dp0
rem pushd %TESTER_PATH%

:: Execute from the parent dir ST_PKGS.
pushd ..

rem pwd

:: Two options for running tests:
:: 1) Direct execution of all tests in a suite.
python SbotDev\test_sbot.py
rem sbot_testing.py test_table.py

:: 2) Run tests explicitly specified in a script. Like:
::runner = unittest.TextTestRunner()
::runner.verbosity = 2
::runner.run(test_tester.TestStEmul('test_module'))

popd
