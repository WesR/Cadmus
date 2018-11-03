import discord
import json
import requests
from pyPrint import *

version = '1.0'

client = discord.Client()


'''
Notes: When printing documents, using the 'proxy_url' does not work,
You must use 'url'
'''


class globalVars:
    def __init__(self, apiKeys=dict(), defaultPrinter=str(), savedPrint=dict()):
        self.apiKeys = apiKeys
        self.defaultPrinter = defaultPrinter
        self.savedPrint = savedPrint


def loadDefaults():
    with open('defaultsAndKeys.json') as data:
        globalVars.apiKeys = json.load(data)
    globalVars.defaultPrinter = globalVars.apiKeys['default-printer']


def helpMessage():
    help = '**Commands:**\n'
    help += 'print <any length text>\n'
    help += 'print-doc <any document/image>\n'
    help += 'get printers\n'
    help += 'get default printer\n'
    help += 'get job queue\n'
    help += 'clear job queue\n'
    help += '------------------------------\n'
    help += '**Requires Permission:**\n'
    help += 'printer <printer-name> print-doc <any document/image>\n'
    help += '------------------------------\n'
    help += '**Admin Commands:**\n'
    help += 'clear printer queue <printer>\n'
    help += 'set default printer <name>\n'
    return help


def formatTextForPrinter(text):
    # We can fit 18 characters per line, so we need to break, but not break words
    words = text.split(' ')
    formatted = str()
    charcount = 0
    for w in words:
        if (charcount + len(w) <= 18):
            formatted += w
            if (charcount + len(w) == 18):
                charcount = 0
                formatted += '\n'
            else:
                charcount += len(w) + 1
                formatted += ' '
        else:
            formatted += '\n'
            formatted += w + ' '
            charcount = len(w) + 1
    return formatted


def printText(message):
    if printBytes(formatTextForPrinter(message.strip().rstrip()).encode()):
        return 'Printing!'
    else:
        print('Print text Error')
        return 'Print error'


def printFileURL(url, printer=''):
    try:
        r = requests.get(url)
        if len(printer) != 0:
            printBytes(r.content, printer)
        else:
            printBytes(r.content)
        return 'Printing!'
    except:
        print('Error Print URL')
        return 'Print error'


@client.event
async def on_ready():
    print("Online")
    await client.change_presence(game=discord.Game(name='Offical Word Holder'))


@client.event
async def on_message(message):
    if message.content.startswith('<@' + client.user.id + ">"):
        await client.send_typing(message.channel)
        command = message.content.split('<@' + client.user.id + ">")[1].strip().rstrip().lower()
        if 'help' in command:
            await client.send_message(message.channel, helpMessage())
        elif 'print-doc' in command:
            if 'printer' in command:
                if message.author.id == globalVars.apiKeys["ownerid"]:
                    try:
                        await client.send_message(message.channel, printFileURL(message.attachments[0]['url'], command.split()[command.split().index('printer') + 1]))
                    except:
                        print('Error finding custom printer')
                        await client.send_message(message.channel, 'Error finding printer')
                else:
                    globalVars.savedPrint = {
                        'queued': True,
                        'url': message.attachments[0]['url'],
                        'printer': command.split()[command.split().index('printer') + 1]
                    }
                    await client.send_message(message.channel, '<@' + globalVars.apiKeys["ownerid"] + '> can we print this?')
            else:
                await client.send_message(message.channel, printFileURL(message.attachments[0]['url']))
        elif 'get job queue' in command or 'get jobs' in command:
            await client.send_message(message.channel, 'Jobs: ' + str(getJobQueueLength()))
        elif 'get printers' in command:
            await client.send_message(message.channel, getAvailablePrinters())
        elif 'clear job queue' in command:
            await client.send_message(message.channel, 'cleared' if clearJobQueue() else 'error')
        elif 'get default printer' in command and message.author.id == globalVars.apiKeys["ownerid"]:
            await client.send_message(message.channel, getDefaultPrinter())
        elif 'clear printer queue' in command and message.author.id == globalVars.apiKeys["ownerid"]:
            await client.send_message(message.channel, 'cleared' if clearJobQueue(message.content.split('<@' + client.user.id + ">")[1].split('clear printer queue')[1].strip().rstrip()) else 'error')
        elif 'set default printer' in command and message.author.id == globalVars.apiKeys["ownerid"]:
            if setDefaultPrinter(message.content.split('<@' + client.user.id + ">")[1].split('set default printer')[1].strip().rstrip()):
                await client.send_message(message.channel, 'Printer set')
            else:
                await client.send_message(message.channel, 'Bad name')
        elif 'print' in command:
            await client.send_message(message.channel, printText(message.content.split('<@' + client.user.id + ">")[1].split('print')[1]))
        elif 'yes' in command and message.author.id == globalVars.apiKeys["ownerid"]:
            if globalVars.savedPrint['queued']:
                await client.send_message(message.channel, printFileURL(globalVars.savedPrint['url'], globalVars.savedPrint['printer']))
                globalVars.savedPrint = dict()
        else:
            await client.send_message(message.channel, '?')


def main():
    client.run(globalVars.apiKeys['discord'])


if __name__ == '__main__':
    loadDefaults()
    main()
