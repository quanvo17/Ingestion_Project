#!/bin/env bash
echo "Start Crawl Apple Watch Data"
cd /crawler/Ingestion_Project/Crawler/Crawler/spiders/apple_watch
rm -r -f __pycache__
applewatch_crawler=`ls | grep -l py *`
for crawler in $applewatch_crawler
do
	crawler_name="${crawler%%".py"}"
	echo "Start crawl du lieu tren trang $crawler_name"
	scrapy crawl watch_$crawler_name -o /data/unprocessed/applewatch/${crawler_name}.csv
  echo "Crawl $crawler_name Done!!!"
done
echo "Exit Crawler"
