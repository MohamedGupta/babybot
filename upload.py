import os, pickle, re, random
#import urllib, urllib2
import requests
from bs4 import BeautifulSoup
from slackbot.bot import respond_to
from slackbot.utils import download_file, create_tmp_file
_dir = os.path.dirname(os.path.realpath(__file__))


@respond_to(r'youtube (.*)', re.IGNORECASE)
def youtube_search(message, search):
    search_parts = search.split()
    option = search_parts[0]
    if unicode(option, 'utf-8').isnumeric() or option in ('top'):
        url = "https://www.youtube.com/results?search_query=" + ' '.join(search_parts[1:])
    else:
        url = "https://www.youtube.com/results?search_query=" + search
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    vids = soup.findAll(attrs={'class':'yt-lockup-tile'})

    if option == 'top':
        reply = 'top result '
        vid = vids[0]
    else:
        try:
            vid = vids[int(option)]
            reply = option + 'th result '
        except:
            vid = random.choice(vids)
            reply = 'random result '
    message.reply(reply + 'https://www.youtube.com/watch?v=' + vid.attrs['data-context-item-id'])


@respond_to(r'give (.*) (\d+) (.*)', re.IGNORECASE)
def give_bucks(message, owner, count, unit):
    count = int(count)
    if os.path.isfile(_dir + 'ledger.p'):
        ledger = pickle.load(open(_dir + 'ledger.p', 'r'))
        if owner not in ledger:
            #ledger.append(owner)
            ledger[owner] = {unit: 0}
        elif unit not in ledger[owner]:
                ledger[owner][unit] = 0
    else:
        ledger = dict()
        ledger[owner] = {unit: 0}

    ledger[owner][unit] = ledger[owner][unit] + count
    pickle.dump(ledger, open(_dir + 'ledger.p', 'w'))
    message.reply('giving {0} {1} to {2}'.format(count, unit, owner))
    message.reply('{0} now has {1} {2}'.format(owner, ledger[owner][unit], unit))

@respond_to(r'dock (.*) (\d+) (.*)', re.IGNORECASE)
def dock_bucks(message, owner, count, unit):
    count = int(count)
    if os.path.isfile(_dir + 'ledger.p'):
        ledger = pickle.load(open(_dir + 'ledger.p', 'r'))
        if owner not in ledger:
            #ledger.append(owner)
            ledger[owner] = {unit: 0}
        elif unit not in ledger[owner]:
                ledger[owner][unit] = 0
    else:
        ledger = dict()
        ledger[owner] = {unit: 0}

    ledger[owner][unit] = ledger[owner][unit] - count
    pickle.dump(ledger, open(_dir + 'ledger.p', 'w'))
    message.reply('docking {0} {1} {2}'.format(owner, count, unit))
    message.reply('{0} now has {1} {2}'.format(owner, ledger[owner][unit], unit))

"""
@respond_to(r'upload \<?(.*)\>?')
def upload(message, url):
    url = url.lstrip('<').rstrip('>')
    fname = os.path.basename(url)
    message.reply('uploading {}'.format(fname))
    if url.startswith('http'):
        with create_tmp_file() as tmpf:
            download_file(url, tmpf)
            message.channel.upload_file(fname, tmpf, 'downloaded from {}'.format(url))
    elif url.startswith('/'):
        message.channel.upload_file(fname, url)
"""
