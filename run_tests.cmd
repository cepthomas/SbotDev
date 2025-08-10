
:: General test runner for all sbot stuff.


cls

echo off

pushd ..\SbotDev\tests
python -m unittest test_common
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
