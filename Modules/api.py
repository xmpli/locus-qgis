from PyQt5.QtWidgets import QMessageBox
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
    'bounding_box': 'bboxsearch/{bbox}/{category}/{search_text}',
    'reference_search': 'refsearch/{reference}/{category}',
    'point_search': 'pointsearch/{location}/{distance}',
    'list_categories': 'list_categories/',
}

class API():
    @staticmethod
    def makeCall(options, method='GET', callBody={}, debug=False):
        mode = API.buildURL(options)
        if not mode:
            addLogEntry('Failed to create URL')
            return False
        addLogEntry('Make call to: ' + mode)

        try:
            conn = http.request(method, mode, body=callBody, headers={
                'Content-Type': 'application/json; charset=UTF-8',
            })
        except:
            addLogEntry("Endpoint failed to connect")
            QMessageBox.critical(None, 'Connection Error', 'Unable to connect to the API endpoint, check your connection or the URL in settings and try again')
            return False

        addLogEntry('Open Connection')
        content = conn.data.decode('UTF-8', 'backslashreplace')
        addLogEntry('Received data: \n -- [BEGIN DATA] --\n' + content + '\n -- [END DATA] --')

        try:
            data = json.loads(content)
            if debug:
                print(data)
            return data
        except:
            addLogEntry("Endpoint failed to return correct data")
            QMessageBox.critical(None, 'Endpoint Error', 'The endpoint gave incorrect data, check the settings to ensure that the URL is correct')
            return False

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
                if len(options['search_text']) > 0:
                    url.append(options['search_text'])
            elif sect == '{distance}':
                if len(options['distance']) > 0:
                    try:
                        # Ensure that the distance is a float value
                        distance = float(options['distance'])
                        url.append(str(distance))
                    except:
                        QMessageBox.information(None, 'Data Error', 'Distance must be a decimal number.\n\nPlease update the distance and try again')
                        return False
            elif sect == '{reference}':
                if len(options['reference']) > 0:
                    url.append(options['reference'])
            elif sect == '{location}':
                part = options['crs'] + ';POINT(' + str(options['location']['x']) + ' ' + str(options['location']['y']) + ')'
                url.append(part)
            elif sect == '{bbox}':
                maxPart = str(options['bbox'][2]) + ' ' + str(options['bbox'][3])
                minPart = str(options['bbox'][0]) + ' ' + str(options['bbox'][1])
                url.append(maxPart + ',' + minPart)

        return endpoint + '/'.join(url)
