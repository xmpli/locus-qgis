from .logging import addLogEntry
import shutil
import json
import os

# Store local data in %user%/AppData/Roaming
home = os.getenv('APPDATA')
if not isinstance(home, str):
    home = '..'

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
            config_data = {
                'endpoint': 'https://api.sh.vialocus.co.uk/',
            }
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
