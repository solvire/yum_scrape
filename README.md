 Crawler for YP
 For general items
 
 scrapy crawl yumellow -o HOMEDIR/items.csv -t csv > /tmp/crawl
 
 Then to clean them up move that file to
 /yum_scrape/scripts/data
 
 run clean CSV to clean up the input file 
 python CleanCSV.py  -v
 
 move into the data directory and run this to split the files into their cities 
 awk -F, 'NR>1 {print > ("cities/" $2 ".csv")}' output.csv