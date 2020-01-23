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

        try:
            method = Config.getConfig()['api_points'][options['method']]
        except:
            Config.resetConfig()
            method = Config.getConfig()['api_points'][options['method']]

        breakdown = method.split('/')

        url = [ breakdown[0] ]
        count = -1

        for sect in breakdown:
            count = count + 1
            if count == 0:
                continue

            if sect == '{category}':
                url.append(options['category'])
            elif sect == '{search}':
                if len(options['search']) > 0:
                    url.append(options['search'])
                else:
                    url.append(' ')
            elif sect == '{address}':
                if len(options['address']) > 0:
                    url.append(options['address'])
                else:
                    url.append(' ')
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
            elif sect == '{limit}':
                if len(options['limit']) > 0:
                    try:
                        # Ensure that the distance is a float value
                        limit = int(options['limit'])
                        url.append(str(limit))
                    except:
                        QMessageBox.information(None, 'Data Error', 'Limit must be a whole number.\n\nPlease update the limit and try again')
                        return False
                else:
                    url.append('100')
            elif sect == '{offset}':
                if len(options['offset']) > 0:
                    try:
                        # Ensure that the distance is a float value
                        offset = int(options['offset'])
                        url.append(str(offset))
                    except:
                        QMessageBox.information(None, 'Data Error', 'Offset must be a whole number.\n\nPlease update the offset and try again')
                        return False
                else:
                    url.append('0')

        return endpoint + '/'.join(url)
