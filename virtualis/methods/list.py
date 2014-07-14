from . import Response
from abc import abstractmethod


class LazyDict:
    def __init__(self, get):
        self.get = get

    def __getitem__(self, name):
        return self.get(name)


class ListResponse(Response):
    '''Response for a protocol formatted list.'''

    def parse_loop(self, dict):
        '''Loop over a protocol response list.

        The `parse_item` method is called for each found item.
        '''

        values = []

        for i in range(1, int(dict['Total']) + 1):
            def get(name):
                return dict[name + str(i)]

            values.append(self.parse_item(LazyDict(get)))

        return values

    @abstractmethod
    def parse_item(self, get):
        '''Parses an item.

        The `get` parameter is a function that takes a name and returns
        the value for the current item.
        '''
