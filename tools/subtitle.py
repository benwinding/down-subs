#!/usr/bin/env python3
import os
import subprocess
import string
import json
import re
import math
from tools import helpers
from tools import logger

def getMatches(subDir, videoId, phrase):
    subPath = downloadSubs(subDir, videoId)
    matches = getMatchesFromFile(videoId, subPath, phrase)
    return matches

def downloadSubs(outdir, videoId):
    lang = "en"
    templateName = "%(id)s.%(ext)s"
    templatePath = os.path.join(outdir, templateName)

    outFileName = "{0}.{1}.vtt".format(videoId, lang)
    outPath = os.path.join(outdir, outFileName)
    if os.path.exists(outPath):
        return outPath

    logger.Print("Downloading: " + videoId)
    keyVals = {
        "lang": lang,
        "templatePath": templatePath,
        "videoId": videoId,
    }

    # -loglevel quiet \ throws an error
    t = string.Template("""youtube-dl --sub-lang ${lang} \
    --write-auto-sub \
    --skip-download \
    --output "${templatePath}" \
    ${videoId}
    """)
    command = t.substitute(keyVals)
    test = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = test.communicate()[0]
    return outPath

def getMatchesFromFile(videoId, subPath, phrase):
    if not os.path.exists(subPath):
        return "Could not find file: " + subPath
    logger.Print(subPath + ", searching: " + phrase)

    with open(subPath, 'r') as subFile:
        lines = subFile.readlines()

    # Build match dictionary
    timeSaidDict = {}
    for i in range(len(lines)):
        line = lines[i]
        matchGroups = re.findall(r'([\s\w\.\,\-\']*)(<[\w\.\/]*>)*(<([\d\:\.]*)>)', line, re.M|re.I)
        for match in matchGroups:
            time = match[3]
            said = match[0]
            timeSaidDict[time] = said

        if len(matchGroups) > 0:
            reverseGroup = re.findall(r'(<([\d\:\.]*)>)(<[\w\.\/]*>)*([\s\w\.\,\-\']*)', line, re.M|re.I)
            time = reverseGroup[-1][1]+"99"
            said = reverseGroup[-1][3]
            timeSaidDict[time] = said

    matchTimes = []
    if " " in phrase:
        phraseArray = phrase.split(" ")
    else:
        phraseArray = [phrase]
    matchedIndex = 0
    matchedMax = len(phraseArray) - 1
    tentativeMatch = []
    # Try and match array
    for index, key in enumerate(timeSaidDict):
        currentPhrasePart = phraseArray[matchedIndex].rstrip().lstrip().lower()
        currentVideoPart = timeSaidDict[key].rstrip().lstrip().lower()
        if currentPhrasePart not in currentVideoPart:
            # print("NO MATCH... currentPhrasePart: " + currentPhrasePart + ", currentVideoPart: " + currentVideoPart)
            matchedIndex = 0
            tentativeMatch = []
            continue
        # print("MATCH!!... currentPhrasePart: " + currentPhrasePart + ", currentVideoPart: " + currentVideoPart)
        tentativeMatch.append(key)
        matchedIndex += 1
        if matchedIndex > matchedMax:
            hmsStart = tentativeMatch[0]
            hmsFinish = tentativeMatch[-1]
            secondsStart = helpers.hms2seconds(hmsStart)
            secondsFinish = helpers.hms2seconds(hmsFinish)
            if secondsFinish == secondsStart:
                secondsFinish += 1
            matchBracket = {
                'start': secondsStart,
                'finish': secondsFinish,
                'duration': secondsFinish - secondsStart,
                'videoId': videoId
            }
            matchTimes.append(matchBracket)
            matchedIndex = 0
            tentativeMatch = []

    return matchTimes
