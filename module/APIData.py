from abc import ABC, abstractmethod


class APIData(ABC):
    """
    Model API
    """

    name = None
    url = None
    method = None
    data = None
    headers = None
    expected_time = None

    @abstractmethod
    def setName(self, name):
        pass

    @abstractmethod
    def setUrl(self, url):
        pass

    @abstractmethod
    def setMethod(self, method):
        pass

    @abstractmethod
    def setHeaders(self, headers):
        pass

    @abstractmethod
    def setData(self, data):
        pass

    @abstractmethod
    def setExpectedTime(self, time):
        pass
