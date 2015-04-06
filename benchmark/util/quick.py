from __future__ import print_function
import timeit
import sys
import os

sys.path.insert(0, os.path.abspath('..'))

iterations = 200000

print('tapes ', timeit.timeit(
    'with timer.time(): pass'.format(iterations),
    setup='import tapes; timer = tapes.timer("thing")',
    number=iterations))


print('scales ', timeit.timeit(
    'with latency.time(): pass'.format(iterations),
    setup='''
from greplin import scales;
STATS = scales.collection("/web", scales.PmfStat("latency"))
latency = STATS.latency
    ''',
    number=iterations))
