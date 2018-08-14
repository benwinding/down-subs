import os
import subprocess
import string
import json
from tools import helpers
from tools import logger

def downloadBase(outdir, videoId, secStart, secDuration):
    helpers.make_path(outdir)
    logger.Print("downloading: {0}, {1}-{2}".format(videoId, secStart, secDuration))
    outFile = "{0}-{1}-{2}.mp4".format(videoId, str(secStart), str(secDuration))
    outPath = os.path.join(outdir, outFile)
    if os.path.exists(outPath):
        return outPath

    keyVals = {
        "videoId": str(videoId),
        "hmsStart": helpers.seconds2hms(secStart),
        "hmsDUR": helpers.seconds2hms(secDuration),
        "outPath": str(outPath)
    }

    t = string.Template("""ffmpeg \
        -y `youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4 \
        -g https://www.youtube.com/watch?v=${videoId} | \
        sed "s/.*/-ss ${hmsStart} -i &/"` \
        -t ${hmsDUR} -c copy ${outPath}""")
    command = t.substitute(keyVals)
    test = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = test.communicate()[0]
    return outPath

def cutBaseVideo(inputVideoPath, outdir, videoId, secStart, secDuration):
    helpers.make_path(outdir)
    logger.Print("downloading: {0}, {1}-{2}".format(videoId, secStart, secDuration))
    outFile = "{0}-{1}-{2}.mp4".format(videoId, str(secStart), str(secDuration))
    outPath = os.path.join(outdir, outFile)
    if os.path.exists(outPath):
        return outPath

    keyVals = {
        "hmsStart": helpers.seconds2hms(secStart),
        "hmsDUR": helpers.seconds2hms(secDuration),
        "outPath": str(outPath),
        "inPath": str(inputVideoPath)
    }
    print(keyVals)

    t = string.Template("""ffmpeg -i ${inPath} -ss ${hmsStart} -t ${hmsDUR} ${outPath}""")
    command = t.substitute(keyVals)
    test = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = test.communicate()[0]
    return outPath

def downloadPart(outdir, videoId, secStart, secDuration):
    baseDir = os.path.join(outdir, 'bases')
    bufferBefore = 10    
    bufferAfter = 4    
    safeStart = float(secStart) - bufferBefore
    if safeStart < 0:
        safeStart = 0
        bufferBefore = float(secStart)
    safeDuration = float(secDuration) + bufferBefore + bufferAfter

    print(secStart)
    print(secDuration)
    print(safeStart)
    print(safeDuration)

    baseVidPath = downloadBase(baseDir, videoId, safeStart, safeDuration)
    cutVidPath = cutBaseVideo(baseVidPath, outdir, videoId, bufferBefore, secDuration)
    return cutVidPath

# (<[\w\.\/c>]*)?([\w',]*)(<[\w\.\/c>]*)*(<[\d\:\.]*>)
downloadPart("out", "0iID-OpwZ4E", "57.990", "0.5")
