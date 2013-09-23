##Crawler for YP
For general run - version 1

This will put the files in HOMEDIR/items.csv There are going to be a lot of cleanups needed for this file

```scrapy crawl yumellow -o HOMEDIR/items.csv -t csv > /tmp/crawl```

Then to clean them up move that file to the __data__ directory.  This should probably be moved out so that we are not working inside the repository. For now that was just quick and dirty. 

```cd /yum_scrape/scripts/data```

Run the __CleanCSV__ to clean up the input file.  This should remove newlines and trim up everything.  It will also remove exclusions based on some sloppy text search against the excludes file. 

	python CleanCSV.py  -h
	DEBUGGING ON
	Usage: CleanCSV.py [options]
	
	Copyright 2013 Solvire (SJS)
	Licensed under the Apache License 2.0
	http://www.apache.org/licenses/LICENSE-2.0
	
	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -i FILE, --in=FILE    set input path [default: ./data/items.csv]
	  -o FILE, --out=FILE   set output path [default: ./data/output.csv]
	  -x FILE, --exclusion_file=FILE
							set path of the exclusion file [default:
							./data/exclusion.txt]
	  -v, --verbose         set verbosity level [default: none]
	  
	python CleanCSV.py  -v


move into the data directory and run this to split the files into their cities 

```awk -F, 'NR>1 {print > ("cities/" $2 ".csv")}' output.csv```