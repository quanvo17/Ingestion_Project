#!/bin/bash

echo "Start crawling"
cd ./Crawler
for file in ./Crawler/spiders/apple_watch; do
  echo "${file##*/}"
done