import re
import ssl
import urllib.parse
import urllib.request

from abc import abstractmethod

class RequestError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '{0}: {1}'.format(self.code, self.message)


class Request():
    ACTION = None
    RESPONSE = None

    @abstractmethod
    def query(self):
        pass


class Response():
    def __init__(self, dict):
        self.parse(dict)

    @abstractmethod
    def parse(self, dict):
        pass


class ListResponse(Response):
    def parse_loop(self, dict):
        values = []

        for i in range(1, int(dict['Total']) + 1):
            def get(name):
                return dict[name + str(i)]

            values.append(self.parse_item(get))

        return values

    @abstractmethod
    def parse_item(self, get):
        pass


class Card():
    pass


def yesno(value):
    value = value.lower()

    if value == 'y':
        return True
    elif value == 'n':
        return False
    else:
        raise ValueError('Unknown yes or no value \'{0}\'.'.format(value))


class GetActiveCardsResponse(ListResponse):
    def parse(self, dict):
        self.cards = self.parse_loop(dict)

    def parse_item(self, get):
        card = Card()

        card.ad_frequency = int(get('AdFrequency'))
        card.cpn_service = bool(get('CPN_Service'))
        card.type = int(get('CardType'))
        card.id = int(get('VCardId'))
        card.holder_name = get('CardholderName')
        card.default = yesno(get('DefaultCard'))
        card.nick = get('Nickname')
        card.pan = int(get('PAN'))
        card.vbv_service = bool(get('VBV_Service'))

        return card


class GetActiveCardsRequest(Request):
    ACTION = 'GetActiveCards'
    RESPONSE = GetActiveCardsResponse

    def query(self):
        return {
            'CardType': '',
            'VCardId': '',
            'codeEFS': '21',
            'codeSi': '001',
        }


class GetCardInfoResponse(Response):
    def parse(self, dict):
        self.avv = dict['AVV']
        self.expiry = int(dict['ExpiryMonth']), int(dict['ExpiryYear'])
        self.pan = int(dict['PAN'])


class GetCardInfoRequest(Request):
    ACTION = 'GetCPN'
    RESPONSE = GetCardInfoResponse

    def __init__(self, type, id):
        self.type = type
        self.id = id

    def query(self):
        return {
            'TransLimit': '',
            'CumulativeLimit': '15',
            'ValidFor': '1',
            'CPNType': 'SP',
            'CardType': str(self.type),
            'VCardId': str(self.id),
        }


class Client:
    SCHEME = 'https'
    HOST = 'www.service-virtualis.com'
    PATH = '/cvd/WebServlet'
    URL = SCHEME + '://' + HOST + PATH
    ENCODING = 'latin_1'

    def __init__(self, user, pass_, cafile=None, capath=None):
        self.user = user
        self.pass_ = pass_
        self.cafile = cafile
        self.capath = capath

        self.session_id = None

        #import http.client
        #http.client.HTTPConnection.debuglevel = 1

        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(self.cafile)

        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(),
            urllib.request.HTTPSHandler(context=context))

    def send(self, req):
        query = req.query()
        query['Request'] = req.ACTION

        if self.session_id is None:
            query['noPersonne'] = self.user
            query['motDePasse'] = self.pass_

        res = self.send_raw(query)

        print()
        print()
        print(res)

        if res['Action'] == 'Error':
            raise RequestError(res['Code'], res['ErrMsg'])

        if 'SessionId' in res:
            self.session_id = res['SessionId']

        return req.RESPONSE(res)

    def send_raw(self, query):
        query['Version'] = '3.0'
        query['IssuerId'] = '1'
        query['Locale'] = 'en'
        query['Trigger'] = 'trigger'
        query['IE'] = 'false'
        query['StartTime'] = '0'

        data = urllib.parse.urlencode(query).encode(self.ENCODING)
        request = urllib.request.Request(self.URL)

        res = self.opener.open(request, data)
        res = res.read().decode(self.ENCODING)
        res = re.sub(r'&+', r'&', res)

        if res[-1] == '&':
            res = res[0:-1]

        res = urllib.parse.parse_qs(res, True, True)
        res = {k: v[0] for k, v in res.items()}

        return res
