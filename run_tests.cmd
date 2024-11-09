

cls

echo off

del "C:\Users\cepth\AppData\Roaming\Sublime Text\Packages\User\_Test\trace.txt"

rem def setUp(self):
rem     sc.init('_Test')
rem def tearDown(self):
rem     pass

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

pushd ..\SbotResiduum\tests
python -m unittest test_residuum
popd

pushd ..\Notr\tests
python -m unittest test_notr test_table
popd

pushd ..\SbotFormat\tests
python -m unittest test_format
popd

pushd ..\SbotHighlight\tests
python -m unittest test_highlight
popd

pushd ..\SbotRender\tests
python -m unittest test_render
popd

pushd ..\SbotSignet\tests
python -m unittest test_signet
popd
