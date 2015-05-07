import gracefulharakiri
import inspect
import os
import re
import signal
import sys
from cStringIO import StringIO
from signal import SIGTERM, SIGINT
from unittest import TestCase
try:
    from unittest import Mock
except ImportError:
    from mock import Mock



class TestGracefulHarakiri(TestCase):
    """Tests for the GracefulHarakiri plugin for nosetests"""

    def setUp(self):
        self.sut = gracefulharakiri.GracefulHarakiri()

    def test_begin_binds_SIGTERM_handler(self):
        """Verify that begin() associates a handler to SIGTERM"""
        def _callable(): pass
        signal.signal(SIGTERM, _callable)

        self.sut.begin()
        self.assertNotEqual(_callable, signal.getsignal(SIGTERM))

    def test_begin_does_not_bind_handlers_to_other_signals(self):
        """Verify that begin() does not associates a handler to signals
        other than SIGTERM"""
        signals = ['signal.' + s for s in dir(signal)
                   if s.startswith('SIG')
                   and s.isalpha()
                   and s != 'SIGTERM']
        handlers = [signal.getsignal(eval(s)) for s in signals]
        signals_and_handlers = dict(zip(signals, handlers))

        self.sut.begin()

        for s,h in signals_and_handlers.items():
            self.assertEqual(h, signal.getsignal(eval(s)))

    def test_handler_sends_SIGINT(self):
        """Verify that the handler sends signal SIGINT"""
        _stdout = sys.stdout
        sys.stdout = StringIO()
        mock = Mock()
        signal.signal(SIGINT, mock)
        self.sut.begin()

        os.kill(os.getpid(), SIGTERM)
        sys.stdout = _stdout

        mock.assert_called_once_with(SIGINT, inspect.currentframe())

    def test_current_frame_information_are_printed(self):
        """Verify that the details of the current stack (file name, line
        number, function name) are printed to the stdout"""
        _stdout = sys.stdout
        sys.stdout = StringIO()
        def _callable(*args): pass
        signal.signal(SIGINT, _callable)
        self.sut.begin()
        frame = inspect.currentframe()

        os.kill(os.getpid(), SIGTERM)
        output = sys.stdout.getvalue()
        sys.stdout = _stdout

        # Avoid specifying the line, it'll make the test too brittle
        details = 'File "%s", line [0-9]+, in %s' % (
            frame.f_code.co_filename,
            frame.f_code.co_name,
        )

        self.assertTrue(re.search(details, output))

