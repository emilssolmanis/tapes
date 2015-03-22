Tapes |version|
===============

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   api
   benchmarks

This is a native Python metrics library implementation. It currently supports Python 2.7, 3.4 and PyPy, but most other
versions should probably work.

Compared to `other libraries <https://github.com/Cue/scales>`_, tapes
 - doesn't use a separate thread to decay the moving average's weights
 - doesn't use "clever tricks" with stack frames, which means it also doesn't break in weird
   ways (e.g., when used within a method decorated with ``@staticmethod``)
 - has clean code, that passes ``flake8`` validation
 - is also performance-oriented

You can check the :doc:`benchmarks` yourself!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

