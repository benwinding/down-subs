#!/usr/bin/env bash

seconds() { 
	date -d "1970-01-01 $1+0" "+%s"
}

hhmmss() { 
	date -d "1970-01-01 $1 seconds" "+%T"
}

secStart=$(seconds $2)
secFin=$(seconds $3)

secStart2=`expr $secStart - 10`
secFin2=`expr $secFin + 5`

secDuration=`expr $secFin2 - $secStart2`

hmsStart=$(hhmmss $secStart2)
hmsFin=$(hhmmss $secFin2)
hmsDUR=$(hhmmss $secDuration)

echo "Downloading video: https://www.youtube.com/watch?v="$1
echo "            Start: "$hmsStart" = "$secStart2 "secs"
echo "           Finish: "$hmsFin" = "$secFin2 "secs"
echo "         Duration: "$hmsDUR" = "$secDuration "secs"

mkdir -p out

ffmpeg -loglevel quiet -y $(youtube-dl -f 'bestvideo[height<=480]+bestaudio/best[height<=480]' -g https://www.youtube.com/watch?v=$1 |  
 sed "s/.*/-ss $hmsStart -i &/") -t $hmsDUR -c copy out/$1-$secStart2-$secDuration.mkv 
