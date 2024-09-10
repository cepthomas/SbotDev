
:: Run unit tests from the command line.
:: Requires env ST_PKGS set to ...\Sublime Text\Packages.

cls
echo off

set PYTHONPATH=%ST_PKGS%
set TESTER_PATH=%~dp0

pushd %TESTER_PATH%

:: Two options for running tests:
:: 1) Direct execution of all tests in a suite.
python test_table.py
rem test_tester.py test_format.py test_highlight.py test_logger.py test_notr.py

:: 2) Run tests explicitly specified in a script. Like:
::runner = unittest.TextTestRunner()
::runner.verbosity = 2
::runner.run(test_tester.TestStEmul('test_module'))

popd

pause
