#!/bin/env bash
echo "Start Crawl Iphone Data"
cd /crawler/Ingestion_Project/Crawler/Crawler/spiders/iphone
rm -r -f __pycache__
iphone_crawler=`ls | grep -l py *`
for crawler in $iphone_crawler
do	
	crawler_name="${crawler%%".py"}"
	echo "Start crawl du lieu tren trang $crawler_name"
	scrapy crawl iphone_$crawler_name -o /data/unprocessed/iphone/${crawler_name}.csv
  echo "Crawl $crawler_name Done!!!"
done
echo "Exit Crawler"
