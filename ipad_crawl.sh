#!/bin/env bash
echo "Start Crawl Ipad Data"
cd /crawler/Project/Crawler/Crawler/spiders/ipad
rm -r -f __pycache__
ipad_crawler=`ls | grep -l py *`
for crawler in $ipad_crawler
do
	crawler_name="${crawler%%".py"}"
	echo "Start crawl du lieu tren trang $crawler_name"
	scrapy crawl ipad_$crawler_name -o /crawler/Project/Crawler/Data/ipad/${crawler_name}.csv --nolog
       	echo "Crawl $crawler_name Done!!!"	
done
echo "Exit Crawler"
