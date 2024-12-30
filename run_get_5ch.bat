@echo off

call .env\Scripts\activate

:: 稼働中
:: set URL=https://itest.5ch.net/hayabusa9/test/read.cgi/mnewsplus/1723666514

:: DAT落ち
:: set URL=https://itest.5ch.net/egg/test/read.cgi/android/1588589650
:: set URL=https://itest.5ch.net/eagle/test/read.cgi/livejupiter/1661614745
:: set URL=https://itest.5ch.net/nova/test/read.cgi/livegalileo/1712803906/
:: set URL=https://itest.5ch.net/nova/test/read.cgi/livegalileo/1712983961
set URL=https://itest.5ch.net/mi/test/read.cgi/news4vip/1643274178/
:: set URL=https://itest.5ch.net/eagle/test/read.cgi/livejupiter/1663411463/

:: 0: 稼働中, 1: DAT落ち
set MODE=1

call python get_5ch.py %URL% -m %MODE%