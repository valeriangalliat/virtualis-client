from . import Response, Request
from .card_aware import CardAwareRequest


class CreateCardResponse(Response):
    def parse(self, dict):
        self.avv = dict['AVV']
        self.expiry = int(dict['ExpiryMonth']), int(dict['ExpiryYear'])
        self.pan = int(dict['PAN'])


class CreateCardRequest(CardAwareRequest):
    ACTION = 'GetCPN'
    RESPONSE = CreateCardResponse

    def __init__(self, card, limit, valid_for):
        super().__init__(card)
        self.limit = limit
        self.valid_for = valid_for

    def query(self):
        return {
            'TransLimit': '',
            'CumulativeLimit': str(self.limit),
            'ValidFor': str(self.valid_for),
            'CPNType': 'SP',
            'CardType': str(self.card.type),
            'VCardId': str(self.card.id),
        }
