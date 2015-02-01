from __future__ import print_function
from datetime import timedelta
from time import sleep

import fudge
from fudge.inspector import arg

from tapes.reporting.console import ThreadedConsoleReporter
from tests.base import StatsTest


class ConsoleReportingTestCase(StatsTest):
    def test_threaded_console_reporter_prints_stats_with_intervals(self):
        # TODO: this is somewhat hacky and it doesn't actually fail. Short of actually introducing a pipe in the other
        # direction (printer_thread -> parent) I see no way of testing this properly at the moment though
        try:
            import __builtin__
            fudge.patch_object(
                __builtin__, 'print',
                fudge.Fake('py2:print')
                .expects_call()
                .with_args(arg.contains('test_threaded_console_reporter_prints_stats_with_intervals'))
            )
        except ImportError:
            import builtins
            fudge.patch_object(
                builtins, 'print',
                fudge.Fake('py3:print')
                .expects_call()
                .with_args(arg.contains('test_threaded_console_reporter_prints_stats_with_intervals'))
            )

        counter = self.registry.counter(
            'ConsoleReportingTestCase.test_threaded_console_reporter_prints_stats_with_intervals'
        )

        counter.increment(42)

        reporter = ThreadedConsoleReporter(self.registry, timedelta(milliseconds=100))
        reporter.start()
        sleep(0.2)
        reporter.stop()
