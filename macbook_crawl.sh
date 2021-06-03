#!/bin/env bash
echo "Start Crawl Macbook Data"
cd /crawler/Ingestion_Project/Crawler/Crawler/spiders/macbook
rm -r -f __pycache__
macbook_crawler=`ls | grep -l py *`
for crawler in $macbook_crawler
do	
	crawler_name="${crawler%%".py"}"
	echo "Start crawl du lieu tren trang $crawler_name"
	scrapy crawl macbook_$crawler_name -o /data/unprocessed/macbook/${crawler_name}.csv
  echo "Crawl $crawler_name Done!!!"
done
echo "Exit Crawler"
