import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Stat(object):

    @abc.abstractmethod
    def get_values(self):
        raise NotImplementedError()
