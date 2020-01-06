from datetime import datetime
import os.path
import simplejson
from qgis.core import QgsMessageLog
import os
import io
from os.path import expanduser

home = expanduser("~")

# This is honestly a bit of a mess and needs reworking anyway
# But, it's the base of a logging module.
def addLogEntry(message, error=False, printstr=False):
    if printstr:
        print(message)
    # Session number for unique error logs
    with open(home + '/Xmpli/Locus_tmpData.json', 'r') as rf:
        tmpData = simplejson.load(rf)
    sIdent = tmpData['sIdent']

    # Make sure that the directory exists
    if not os.path.exists(home + '/Xmpli/Logs'):
        os.makedirs(home + '/Xmpli/Logs')
    if error:
        line = '[ERROR] - [' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] - ' + message
    else:
        line = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] - ' + message
    if not os.path.isfile(home + '/Xmpli/Logs/Locus_' + sIdent + '.txt'):
        with io.open(home + '/Xmpli/Logs/Locus_' + sIdent + '.txt', 'w', encoding="utf-8") as wf:
            wf.write(line)
    else:
        line = '\n' + line
        with io.open(home + '/Xmpli/Logs/Locus_' + sIdent + '.txt', 'a', encoding="utf-8") as wf:
            wf.write(line)
        #QgsMessageLog.logMessage(message, tag="Locus", level=QgsMessageLog.INFO)


def setSessionIdentifier():
    tData = {
        'sIdent': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    }
    with open(home + '/Xmpli/Locus_tmpData.json', 'w') as wf:
        simplejson.dump(tData, wf)
