cat .temp/youtube-urls.txt | parallel -j 30 \
	"youtube-dl --sub-lang en \
	--write-auto-sub \
	--skip-download \
	--output \"captions/%(id)s.%(ext)s\" \
	{}"
