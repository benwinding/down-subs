import concurrent.futures

from tools import subtitle
from tools import vidPart
from tools import logger
from tools import playlist

def downloadSubtitles(subsDir, videoIds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(subtitle.downloadSubs, subsDir, videoId): videoId for videoId in videoIds}
        for future in concurrent.futures.as_completed(futures):
            subPath = future.result()

def convertPlaylists2VideoIds(playlistDir, playlistIds):
    allVideoIds = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(playlist.convert2VideoIds, playlistDir, playlistId): playlistId for playlistId in playlistIds}
        for future in concurrent.futures.as_completed(futures):
            videoIds = future.result()
            allVideoIds += videoIds

    return allVideoIds

def downloadAll(partsDir, matches):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(vidPart.downloadPart, partsDir, match['videoId'], match['start'], match['duration']): match for match in matches}
        for future in concurrent.futures.as_completed(futures):
            partPath = future.result()
            logger.Print("Finished: " + partPath)

def findMatchesAll(subsDir, videoIds, searchPhrase):
    allMatches = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(subtitle.getMatches, subsDir, videoId, searchPhrase): videoId for videoId in videoIds}
        for future in concurrent.futures.as_completed(futures):
            phraseMatches = future.result()
            if not isinstance(phraseMatches, list):
                continue
            if len(phraseMatches) > 0:
                allMatches += phraseMatches

    return allMatches
