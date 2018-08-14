from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import json
import re
import os 

from tools import helpers

def getId(href):
    matchObj = re.search( r'(\?v=)([\w\d-]*)', href, re.M|re.I)
    match = matchObj.group(2)
    return match

def convert2VideoIds(playlistsDir, playlistId):
    # Caching
    helpers.make_path(playlistsDir)
    playlistFile = playlistId + ".txt"
    playlistPath = os.path.join(playlistsDir, playlistFile)
    if os.path.exists(playlistPath):
        with open(playlistPath, 'r') as plFile:
            allLines = plFile.readlines()
            allIds = {line.rstrip() for line in allLines}
            return allIds

    host = 'https://www.youtube.com'
    url = '{0}/playlist?list={1}'.format(host, playlistId)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    linksAll = soup.find_all('a','pl-video-title-link')
    # Get more links if there's a load more button
    if len(linksAll) > 99:
        loadMoreHref = soup.find('button', 'load-more-button')['data-uix-load-more-href']
        url2 = host + loadMoreHref
        # print(url2)
        contentHtml = json.load(urlopen(url2))['content_html']
        soup2 = BeautifulSoup(contentHtml, 'html.parser')
        links2 = soup2.find_all('a','pl-video-title-link')
        linksAll = linksAll + links2

    allHrefs = {link['href'].encode('utf-8') for link in linksAll}
    allIds = {getId(str(href)) for href in allHrefs}
    with open(playlistPath, 'w') as plFile:
        for item in allIds:
            plFile.write("%s\n" % item)
    return allIds

# print(convert2VideoIds("PL34C1F26D03F5F9B8"))