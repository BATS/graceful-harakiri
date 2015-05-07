# GracefulHarakiri
Plugin for nosetests that intercepts SIGTERM signals, converts them to SIGINT
and prints the stacktrace.


Motivation
==========

Jenkins kills the builds that exceed a specific amount of time, by sending them
a SIGTERM signal.

If nosetests receives a SIGTERM signal, it stops abruptly and does not
display any information where it left off. This information would be valuable
in debugging the test that got stuck.


Enter GracefulHarakiri, a plugin that intercepts the SIGTERM signal and
converts it to a SIGINT signal, thus making nosetests exit gracefully.
The plugin also outputs the current stack frame (and all previous ones), much
like Python does when displaying a Traceback object.


Setup and usage
===============

To install it you can use easy_install:

      $ sudo easy_install gracefulharakiri


The usage is also pretty simple: just specify `--with-gracefulharakiri` on the
command line.


Example
=======

Suppose you run the following test, in `test_dummy.py`:

      import time
      def test_nothing():
            time.sleep(120)

If you run it without this plugin and kill it via a SIGTERM, you would see:

      $ nosetests -sv test_dummy.py
      2015-04-27 11:27:17 : test_dummy.test_nothing ... Terminated

If you enabled the GracefulHarakiri plugin:

      $ nosetests -sv --with-gracefulharakiri test_dummy.py
      2015-04-27 11:29:44 : test_dummy.test_nothing ... Traceback (most recent call last):
        File "/usr/local/bin/nosetests", line 8, in <module>
      [... trimmed output ...]
        File "/usr/local/lib64/python2.6/site-packages/nose-1.3.4-py2.6.egg/nose/case.py", line 197, in runTest
            self.test(*self.arg)                                                                              
        File "/home/user/test_dummy.py", line 4, in test_nothing             
            time.sleep(120)
