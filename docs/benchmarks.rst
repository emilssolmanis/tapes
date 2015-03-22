==========
Benchmarks
==========

The benchmarking scripts are in the source code and have ``tox`` environments defined for Python 2.7, 3.4 and PyPy.
All you need to do to run them yourself is check out the code and run::

    tox -e benchmark-py27,benchmark-py34,benchmark-pypy

The results shown here are from an old-ish i5 laptop and are by no means 100% conclusive. With that said...

Just the timer
==============

This just runs some timer metric calls via Python's ``timeit``. The times are

======= =============== ===============
         Tapes           Scales
======= =============== ===============
Py 2.7   3.0038728714    12.1747989655
Py 3.4   3.3859353300    15.8657573729
PyPy     0.4108750820    11.163599968


Flask
=====

Python 2.7
----------
.. image:: images/benchmarks/py27/flask_single_box.png
    :align: center

Python 3.4
----------
.. image:: images/benchmarks/py34/flask_single_box.png
    :align: center

PyPy 2.4
--------
.. image:: images/benchmarks/pypy/flask_single_box.png
    :align: center

Tornado, single process
=======================

Python 2.7
----------
.. image:: images/benchmarks/py27/tornado_single_box.png
    :align: center

Python 3.4
----------
.. image:: images/benchmarks/py34/tornado_single_box.png
    :align: center

PyPy 2.4
----------
.. image:: images/benchmarks/pypy/tornado_single_box.png
    :align: center


Tornado, forked processes
=========================

Python 2.7
----------
.. image:: images/benchmarks/py27/tornado_multi_box.png
    :align: center

Python 3.4
----------
.. image:: images/benchmarks/py34/tornado_multi_box.png
    :align: center

PyPy 2.4
--------
.. image:: images/benchmarks/pypy/tornado_multi_box.png
    :align: center

