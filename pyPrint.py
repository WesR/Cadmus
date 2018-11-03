import cups
import json
from cadmus import globalVars, loadDefaults

loadDefaults()
conn = cups.Connection()

'''
This file is for talking to the cups driver
'''


def getDefaultPrinter():
    return globalVars.defaultPrinter


def setDefaultPrinter(name):
    for printer in conn.getPrinters():
        if str(name) == str(printer):
            globalVars.defaultPrinter = str(printer)
            return True
    return False


def getAvailablePrinters():
    printers = 'Printers:\n'
    for printer in conn.getPrinters():
        printers += printer + '\n'
    return printers


def getJobQueueLength():
    return len(conn.getJobs())


def clearJobQueue(printer=globalVars.defaultPrinter):
    try:
        conn.cancelAllJobs(printer)
        return True
    except:
        print('Error Clearing Jobs')
        return False


def printBytes(b, printer=globalVars.defaultPrinter):
    try:
        scratchFile = open("./scratch", "wb")
        scratchFile.write(b)
        scratchFile.close()
        conn.printFile(printer, './scratch', 'python print', {})
        return True
    except:
        print('Error Printing Bytes')
        return False
