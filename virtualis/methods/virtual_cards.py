from .pagination import PaginationResponse, PaginationRequest
from ..types import date, short_date


class VirtualCard:
    pass


class VirtualCardsResponse(PaginationResponse):
    def parse(self, dict):
        super().parse(dict)
        self.cards = self.parse_loop(dict)

    def parse_item(self, dict):
        card = VirtualCard()

        card.avv = int(dict['AVV'])
        card.limit = float(dict['UCumulativeLimit'])
        card.currency = int(dict['Currency'])
        card.expiry = short_date(dict['Expiry'])
        card.start_date = short_date(dict['StartDate'])
        card.issue_date = date(dict['IssueDate'])
        card.merchant_id = dict['MerchantId']
        card.merchant_name = dict['MerchantName']
        card.num_usage = dict['NumUsage']
        card.open_to_by = dict['UOpenToBuy']
        card.pan = dict['PAN']
        card.valid_from = dict['ValidFrom']

        return card


class VirtualCardsRequest(PaginationRequest):
    ACTION = 'GetActiveAccounts'
    RESPONSE = VirtualCardsResponse

    def __init__(self, type, id):
        super().__init__()
        self.type = type
        self.id = id

    def query(self):
        query = super().query()

        query['CardType'] = str(self.type)
        query['VCardId'] = str(self.id)

        return query
