import abc


class Stat(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_values(self):
        raise NotImplementedError()
