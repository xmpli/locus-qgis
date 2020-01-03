from .logging import addLogEntry
from .config import Config
import urllib3
import urllib.parse
import certifi
import json
import os

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

callPoints = {
    'category_search': 'search/{category}/{search_text}',
    'bounding_box': 'bboxsearch/',
    'reference_search': 'refsearch/',
    'point_search': 'pointsearch/',
    'list_categories': 'list_categories/',
}

class API():
    @staticmethod
    def makeCall(options, method='GET', callBody={}, debug=False):
        mode = API.buildURL(options)
        addLogEntry('Make call to: ' + mode)

        conn = http.request(method, mode, body=callBody, headers={
            'Content-Type': 'application/json; charset=UTF-8',
        })

        addLogEntry('Open Connection')
        content = conn.data.decode('UTF-8')
        addLogEntry('Received data: \n -- [BEGIN DATA] --\n' + content + '\n -- [END DATA] --')
        data = json.loads(content)
        if debug:
            print(data)
        return data

    @staticmethod
    def buildURL(options):
        endpoint = Config.getConfig()['endpoint']
        if endpoint[-1:] != '/':
            endpoint += '/'

        method = callPoints[options['method']]
        breakdown = method.split('/')

        url = [ breakdown[0] ]
        count = -1

        for sect in breakdown:
            count = count + 1
            if count == 0:
                continue

            if sect == '{category}':
                url.append(options['category'])
            elif sect == '{search_text}':
                url.append(options['search_text'])

        print(url)
        return endpoint + '/'.join(url)
