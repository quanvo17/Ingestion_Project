#!/bin/env bash
echo "Start Crawl Apple Watch Data"
cd /crawler/Project/Crawler/Crawler/spiders/applewatch
rm -r -f __pycache__
applewatch_crawler=`ls | grep -l py *`
for crawler in $applewatch_crawler
do
	crawler_name="${crawler%%".py"}"
	echo "Start crawl du lieu tren trang $crawler_name"
	scrapy crawl applewatch_$crawler_name -o /crawler/Project/Crawler/Data/applewatch/${crawler_name}.csv --nolog
       	echo "Crawl $crawler_name Done!!!"	
done
echo "Exit Crawler"
