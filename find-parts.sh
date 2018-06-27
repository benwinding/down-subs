mkdir -p .temp

echo Finding: \"$1\" in all subtitle files

grep --color -Ri -B 1 "$1" ./captions | grep .vtt- | sed -n 'n;p' > .temp/search-results.txt

cd .temp

cat search-results.txt | grep -o -P '(?<=captions/).*(?=\.en\.vtt)' > part-urls.txt
cat search-results.txt | grep -o -P '(?<=\.en\.vtt\-).*(?=\ \-\-)' > part-starts.txt
cat search-results.txt | grep -o -P '(?<=\-\-\>\ ).*(?=\ align)' > part-ends.txt

paste part-urls.txt part-starts.txt part-ends.txt > download-parts.txt