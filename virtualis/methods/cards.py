from . import Request
from .list import ListResponse
from ..types import yesno


class Card:
    pass


class CardsResponse(ListResponse):
    def parse(self, dict):
        self.cards = self.parse_loop(dict)

    def parse_item(self, dict):
        card = Card()

        card.ad_frequency = int(dict['AdFrequency'])
        card.cpn_service = bool(dict['CPN_Service'])
        card.type = int(dict['CardType'])
        card.id = int(dict['VCardId'])
        card.holder_name = dict['CardholderName']
        card.default = yesno(dict['DefaultCard'])
        card.nick = dict['Nickname']
        card.pan = dict['PAN']
        card.vbv_service = bool(dict['VBV_Service'])

        return card


class CardsRequest(Request):
    ACTION = 'GetActiveCards'
    RESPONSE = CardsResponse

    def query(self):
        return {
            'CardType': '',
            'VCardId': '',
            'codeEFS': '21',
            'codeSi': '001',
        }
