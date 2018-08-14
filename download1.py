#!/usr/bin/python3

from tools import vidPart
from tools import subtitle
from tools import logger

import concurrent.futures
import urllib.request
import shutil

subsDir = 'out/subs'
clipsDir = 'out/clips'
vidId = '0iID-OpwZ4E'

logger.debugOn()

vidPart.downloadPart(clipsDir, vidId, 0, 6)