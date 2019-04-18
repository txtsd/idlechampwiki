import requests
import urllib
from pprint import pprint


class ICAccount:
    API_URL = "https://idlechampions.gamepedia.com/api.php"
    PARAMS_0 = {
        'format': 'json',
        'formatversion': '2',
        'maxlag': '5',
    }
    PARAMS_1 = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json',
        'formatversion': '2',
        'maxlag': '5',
    }
    PARAMS_2 = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'csrf',
        'format': 'json',
        'formatversion': '2',
        'maxlag': '5',
    }

    def __init__(self):
        self.un = 'Txtsd8313@IC_Parse_Uploader'
        self.pw = 'vlsl03nb0qqmubt0g4pik48je0bubi0k'
        self.result = None
        self.S = requests.Session()
        self.S.headers = {'User-Agent': 'IC_Parse_Uploader'}

    def get(self, param={}):
        _param = param
        _param.update(ICAccount.PARAMS_0)
        R = self.S.get(ICAccount.API_URL, params=_param)
        return R

    def post(self, data={}, param={}, head={}):
        _param = param
        _param.update(ICAccount.PARAMS_0)
        _param = urllib.parse.urlencode(_param)
        _data = data

        _R = self.S.get(url=ICAccount.API_URL, params=ICAccount.PARAMS_2)
        DATA = _R.json()
        LOGIN_TOKEN = DATA['query']['tokens']['csrftoken']

        _data.update({'token': LOGIN_TOKEN})
        # _head = head
        # _head.update({'Content-Type': 'application/x-www-form-urlencoded'})
        R = self.S.post(ICAccount.API_URL, params=_param, data=_data)
        return R

    def login(self):
        # Retrieve login token first
        R = self.S.get(url=ICAccount.API_URL, params=ICAccount.PARAMS_1)
        DATA = R.json()

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
        # print(LOGIN_TOKEN)

        # Send a post request to login. Using the main account for login is not
        # supported. Obtain credentials via Special:BotPasswords
        # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
        PARAMS = {
            'action': 'login',
            'lgname': self.un,
            'lgpassword': self.pw,
            'lgtoken': LOGIN_TOKEN,
            'format': 'json',
            'formatversion': '2',
            'maxlag': '5',
        }

        R = self.S.post(ICAccount.API_URL, data=PARAMS)
        DATA = R.json()
        if R.status_code == 200:
            print('Logged in!')
        # print(DATA)


if __name__ == '__main__':
    instance = ICAccount()
    instance.login()
