import datetime


def choice(true, false):
    '''Create a choice type between a false or true value.'''

    def parse(value):
        value = value.lower()

        if value == true:
            return True

        if value == false:
            return False

        message = 'Unknown value format, expected \'{0}\' or \'{1}\'.'
        message = messageformat(true, false)
        raise ValueError(message)

    return parse


truefalse = choice('true', 'false')
yesno = choice('y', 'n')


def split_date(value):
    return map(int, value.split('/'))


def date(value):
    '''Convert a protocol date to `datetime.date`.'''
    day, month, year = split_date(value)
    return datetime.date(year, month, day)


def short_date(value):
    '''Convert a protocol short date to `datetime.date`.'''
    month, year = split_date(value)
    return datetime.date(2000 + year, month, 1)


class Money:
    def __init__(self, value):
        '''Parse a money protocol value. '''
        self.currency = value[0]
        self.amount = float(value[1:])

    def __str__(self):
        return self.currency + str(self.amount)
