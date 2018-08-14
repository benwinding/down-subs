
def hms2seconds(hmsString):
    h, m, s = hmsString.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def seconds2hms(seconds):
    seconds = abs(float(seconds))
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02f" % (hours, minutes, seconds)

import shutil, os, errno
def make_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
