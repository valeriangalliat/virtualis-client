from .pagination import PaginationResponse, PaginationRequest
from ..types import date, short_date, Money
from functools import partial


class VirtualCard:
    pass


class VirtualCardsResponse(PaginationResponse):
    def __init__(self, parent_card, dict):
        self.parent = parent_card
        super().__init__(dict)

    def parse(self, dict):
        super().parse(dict)
        self.cards = self.parse_loop(dict)

    def parse_item(self, dict):
        card = VirtualCard()

        card.parent = self.parent
        card.avv = dict['AVV']
        card.limit = Money(dict['CumulativeLimit'])
        card.currency = int(dict['Currency'])
        card.expiry = short_date(dict['Expiry'])
        card.start_date = short_date(dict['StartDate'])
        card.issue_date = date(dict['IssueDate'])
        card.merchant_id = dict['MerchantId']
        card.merchant_name = dict['MerchantName']
        card.num_usage = int(dict['NumUsage'])
        card.open_to_by = Money(dict['OpenToBuy'])
        card.pan = dict['PAN']
        card.valid_from = date(dict['ValidFrom'])

        return card


class VirtualCardsRequest(PaginationRequest):
    ACTION = 'GetActiveAccounts'

    def __init__(self, card):
        super().__init__()
        self.card = card

        # Contextual response
        self.RESPONSE = partial(VirtualCardsResponse, self.card)

    def query(self):
        query = super().query()

        query['CardType'] = str(self.card.type)
        query['VCardId'] = str(self.card.id)

        return query
