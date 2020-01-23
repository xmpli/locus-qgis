from .logging import addLogEntry
import shutil
import json
import os
from os.path import expanduser

home = expanduser("~")

config_data = {
    'endpoint': 'https://api.sh.vialocus.co.uk/',
    'api_points': {
        'address_search': 'address_search/{address}/{limit}/{offset}',
        'category_search': 'search/{category}/{search}/{limit}/{offset}',
        'bounding_box': 'bboxsearch/{bbox}/{category}/{search_text}',
        'point_search': 'pointsearch/{location}/{distance}/{category}/{search}/{limit}/{offset}',
        'reference_search': 'refsearch/{reference}/{category}/{limit}/{offset}',
        'list_categories': 'list_categories/',
    },
    'widgets': {
        'category_search': [{
                'type': 'preMade',
                'name': 'categoryGroup',
            }, {
                'type': 'text',
                'name': 'search',
                'default': '',
            }, {
                'type': 'text',
                'name': 'limit',
                'default': '100',
            }, {
                'type': 'text',
                'name': 'offset',
                'default': '0',
        }],
        'bounding_box': [{
                'type': 'preMade',
                'name': 'bboxGroup',
            }, {
                'type': 'preMade',
                'name': 'categoryGroup',
            }, {
                'type': 'text',
                'name': 'search',
                'default': '',
        }],
        'reference_search': [{
                'type': 'category',
                'typeName': 'categoryGroup',
            }, {
                'type': 'text',
                'name': 'reference',
                'default': '',
            }, {
                'type': 'text',
                'name': 'limit',
                'default': '100',
            }, {
                'type': 'text',
                'name': 'offset',
                'default': '0',
        }],
        'point_search': [{
                'type': 'preMade',
                'name': 'locationGroup',
            }, {
                'type': 'text',
                'name': 'distance',
                'default': '100',
            }, {
                'type': 'text',
                'name': 'limit',
                'default': '100',
            }, {
                'type': 'text',
                'name': 'offset',
                'default': '0',
        }],
        'address_search': [{
                'type': 'text',
                'name': 'address',
                'default': '',
            }, {
                'type': 'text',
                'name': 'limit',
                'default': '100',
            }, {
                'type': 'text',
                'name': 'offset',
                'default': '0',
        }],
    },
}

class Config():
    config = {}

    def __init__(self):
        if not os.path.exists(home + '/Xmpli'):
            os.makedirs(home + '/Xmpli')

        if not os.path.exists(home + '/Xmpli/tmp'):
            os.makedirs(home + '/Xmpli/tmp')
        else:
            shutil.rmtree(home + '/Xmpli/tmp')
            os.makedirs(home + '/Xmpli/tmp')

        if not os.path.isfile(home + '/Xmpli/Locus_config.json'):
            with open(home + '/Xmpli/Locus_config.json', 'w') as wf:
                json.dump(config_data, wf)

        with open(home + '/Xmpli/Locus_config.json', 'r') as rf:
            Config.config = json.load(rf)

    @staticmethod
    def updateConfig(new_config):
        addLogEntry('Updating Config: \n -- [BEGIN DATA] -- \n' + json.dumps(new_config) + '\n -- [END DATA] --')
        Config.config = new_config

        with open(home + '/Xmpli/Locus_config.json', 'w') as wf:
            json.dump(new_config, wf)

    @staticmethod
    def getConfig():
        addLogEntry('Returning config')
        return Config.config

    @staticmethod
    def resetConfig():
        with open(home + '/Xmpli/Locus_config.json', 'w') as wf:
            json.dump(config_data, wf)
            Config.config = config_data
