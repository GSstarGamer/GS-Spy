import json
import re
import requests

def webhookurl(url:str):
    pattern = r'^https://discord\.com/api/webhooks/\d+/[A-Za-z0-9_-]+$'

    if re.match(pattern, url):
        res = requests.get(url)
        if res.status_code == 200:
            return url
        else:
            raise TypeError('Not a valid webhook URL (request)')
    else:
        raise TypeError('Not a valid webhook URL (re)')


class config():
    def __init__(self) -> None:
        with open('config.json', 'r') as f:
            data = json.load(f)

        self.prefix = str(data['prefix'])
        self.webhookURL = webhookurl(data['webhookURL'])
        self.enabled = bool(data['enabled'])
        self.targets = [int(i) for i in data['targets']]
