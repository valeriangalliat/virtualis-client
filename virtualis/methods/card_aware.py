from . import Request


class CardAwareRequest(Request):
    def __init__(self, card):
        self.card = card

    def query(self):
        return {
            'CardType': self.card.type,
            'VCardId': self.card.id,
        }
