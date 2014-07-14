from . import Response, Request


class CreateCardResponse(Response):
    def parse(self, dict):
        self.avv = dict['AVV']
        self.expiry = int(dict['ExpiryMonth']), int(dict['ExpiryYear'])
        self.pan = int(dict['PAN'])


class CreateCardRequest(Request):
    ACTION = 'GetCPN'
    RESPONSE = CreateCardResponse

    def __init__(self, type, id, limit, valid_for):
        self.type = type
        self.id = id
        self.limit = limit
        self.valid_for = valid_for

    def query(self):
        return {
            'TransLimit': '',
            'CumulativeLimit': str(self.limit),
            'ValidFor': str(self.valid_for),
            'CPNType': 'SP',
            'CardType': str(self.type),
            'VCardId': str(self.id),
        }
