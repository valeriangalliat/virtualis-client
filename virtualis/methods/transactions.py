from .pagination import PaginationResponse, PaginationRequest
from ..types import date, short_date, Money
from functools import partial


class Transaction:
    pass


class TransactionsResponse(PaginationResponse):
    def parse(self, dict):
        super().parse(dict)
        self.transactions = self.parse_loop(dict)

    def parse_item(self, dict):
        transaction = Transaction()

        transaction.avv = dict['AVV']
        transaction.auth_code = dict['AuthCode']
        transaction.cumulative_limit = Money(dict['CumulativeLimit'])
        transaction.currency = int(dict['Currency'])
        transaction.expiry = short_date(dict['ExpiryDate'])
        transaction.issue_date = date(dict['IssueDate'])
        transaction.merchant_city = dict['MerchantCity']
        transaction.merchant_country = dict['MerchantCountry']
        transaction.merchant_name = dict['MerchantName']
        transaction.micro_ref_number = dict['MicroRefNumber']
        transaction.num_usage = int(dict['NumUsage'])
        transaction.pan = dict['PAN']
        transaction.amount = Money(dict['TransactionAmount'])
        transaction.date = date(dict['TransactionDate'])
        transaction.limit = Money(dict['TransactionLimit'])
        transaction.valid_from = date(dict['ValidFrom'])
        transaction.valid_to = date(dict['ValidTo'])

        return transaction


class TransactionsRequest(PaginationRequest):
    ACTION = 'GetPastTransactions'
    RESPONSE = TransactionsResponse

    def __init__(self, card):
        super().__init__()
        self.card = card

    def query(self):
        query = super().query()

        query['CardType'] = str(self.card.type)
        query['VCardId'] = str(self.card.id)

        return query
