#!/usr/bin/python3

import concurrent.futures

from tools import vidPart
from tools import playlist
from tools import subtitle
from tools import batcher
from tools import logger

logger.debugOn()

subsDir = '/home/ben/Downloads/out/subs'
playlistDir = '/home/ben/Downloads/out/playlist'
clipsDirBase = '/home/ben/Downloads/out/clips2'

playlistIds = ['PL8F9A69893481FB47',
'PLJ_TJFLc25JTxhK8VHJXHAG7QMiUd-JXd',
'PLJ_TJFLc25JSmtBkyIYqgD5KabbU57yzY',
'PLJ_TJFLc25JQaIKha3sduCHUXkFcNMMDS',
'PLJ_TJFLc25JSeHaHvnLsVJjpPGbFsylAE',
'PLJ_TJFLc25JTwinvdLo4PP2rTFfTd9Uhz',
'PLJ_TJFLc25JR3VZ7Xe-cmt4k3bMKBZ5Tm',
'PL8F9A69893481FB47',
'PL34C1F26D03F5F9B8',
'PL5919C8DE6F720A2D',
'FLrTNhL_yO3tPTdQ5XgmmWjA',
'PL2CCF5FDA9CEEBDB8']
searchPhrases = ['superman', 'ironman', 'aquaman', 'hulk', 'wonderwoman', 'ghost busters',
 'batman', 'spiderman', 'extended universe', 'dc comics', 'batman', 'cinematic universe']

def processJob(clipsDir, videoIds, searchPhrase):
    matchArray = batcher.findMatchesAll(subsDir, videoIds, searchPhrase)
    for match in matchArray:
        match['start'] -= 0.25
        match['duration'] += 0.5
    batcher.downloadAll(clipsDir, matchArray)

videoIds = batcher.convertPlaylists2VideoIds(playlistDir, playlistIds)
videoIds = list(set(videoIds))

for searchPhrase in searchPhrases:
    clipsDir = clipsDirBase + "_" + searchPhrase.replace(' ', '-')
    processJob(clipsDir, videoIds, searchPhrase)
