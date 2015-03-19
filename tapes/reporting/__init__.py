from __future__ import print_function

import abc
import tapes


class Reporter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry):
        self.registry = registry if registry is not None else tapes._global_registry

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass
