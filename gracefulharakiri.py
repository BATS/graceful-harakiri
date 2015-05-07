import linecache
import os
import signal

from nose.plugins import Plugin

class GracefulHarakiri(Plugin):
    name = 'gracefulharakiri'

    def _print_tb(self, frame):
        """Print a stack trace, starting with the passed frame and going upwards."""
        tb_output = []
        while frame is not None:
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            name = frame.f_code.co_name
            frame_output = '  File "%s", line %d, in %s' % (
                filename, lineno, name)
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, frame.f_globals)
            if line:
                frame_output += '\n    ' + line.strip()
            tb_output.append(frame_output)
            frame = frame.f_back

        tb_output.reverse()
        print 'Traceback (most recent call last):'
        print '\n'.join(tb_output)

    def _SIGTERM_handler(self, _, frame):
            """Handler for SIGTERM: print the stack and send a SIGINT signal."""
            self._print_tb(frame)
            os.kill(os.getpid(), signal.SIGINT)

    def begin(self):
        signal.signal(signal.SIGTERM, self._SIGTERM_handler)

