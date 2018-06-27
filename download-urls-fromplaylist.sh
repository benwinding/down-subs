# curl URL:
curl "https://www.googleapis.com/youtube/v3/playlistItems?playlistId=$1&maxResults=50&part=snippet%2CcontentDetails&key=$2" |
	grep videoId |
	sed -n 'n;p' |
	grep -o -P '(?<=videoId\"\:\ \").*(?=\"\,)' > .temp/youtube-ids.txt

awk '{print "https://www.youtube.com/watch?v=" $0}' .temp/youtube-urls.txt > .temp/youtube-urls.txt
