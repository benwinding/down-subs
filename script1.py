#!/usr/bin/python3

from tools import vidPart
from tools import subtitle
from tools import logger

import concurrent.futures
import urllib.request
import shutil

subsDir = '/home/ben/Downloads/out/subs'
clipsDir = '/home/ben/Downloads/out/clips'
vidId = '0iID-OpwZ4E'
searchPhrase = 'i think'

logger.debugOn()

print("Searching: " + searchPhrase)
matchObj = subtitle.getMatches(subsDir, vidId, searchPhrase)
matchArray = matchObj['matches']
print(matchArray)
for match in matchArray:
    secStart = match['start']
    secDuration = match['duration']
    vidPart.downloadPart(clipsDir, vidId, secStart-0.25, secDuration+0.5)