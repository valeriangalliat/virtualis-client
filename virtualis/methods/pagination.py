from . import Request
from .list import ListResponse


class PaginationResponse(ListResponse):
    def parse(self, dict):
        self.count = int(dict['RecordCount'])


class PaginationRequest(Request):
    def __init__(self):
        '''Set pagination default values.

        The page number starts from 1, and the limit is the number of
        items per page.
        '''

        self.page = 1
        self.limit = 10

    def paginate(self, page, limit):
        self.page = page
        self.limit = limit

    def query(self):
        '''Gets the pagination query dictionary.'''

        return {
            'Start': (self.page - 1) * self.limit,
            'Next': self.limit,
        }
