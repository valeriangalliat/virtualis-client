from . import Request
from .card_aware import CardAwareRequest


class DeleteCardRequest(CardAwareRequest):
    ACTION = 'CancelCPN'
    RESPONSE = lambda *args: True

    def __init__(self, card):
        self.virtual_card = card
        super().__init__(card.parent)

    def query(self):
        query = super().query()
        query['CPNPAN'] = self.virtual_card.pan
        return query
