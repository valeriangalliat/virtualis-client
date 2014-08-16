from abc import abstractmethod


class Request:
    ACTION = None
    RESPONSE = None

    @abstractmethod
    def query(self):
        pass


class Response:
    def __init__(self, dict):
        self.parse(dict)

    @abstractmethod
    def parse(self, dict):
        pass


from .cards import CardsRequest, CardsResponse
from .virtual_cards import VirtualCardsRequest, VirtualCardsResponse
from .create_card import CreateCardRequest, CreateCardResponse
from .delete_card import DeleteCardRequest
from .transactions import TransactionsRequest, TransactionsResponse
