# haystackr
A simple tool to generate web traffic, primarily intended for making infosec lab exercises more realistic.

## usage: haystackr.py [-h] [-p] [-s SLEEP_MS] [-v] [-x] [-a] [-m] [-l LIST_FILE]

haystackr -h for more usage infromation

Haystacker can read URLs from 
* a user supplied file of URLs (one per line)
* The first (free) page of the Alexa top 500 (which only shows 50)
* The free list of the top 500 sites at moz.com
* Any combination of the above

It then removes duplicates, and iterates through the resulting list, grabbing each URL and compiling a list of all src-referenced resources in that page (images, scripts, etc). That list is then deduplicated, and those files are requested. 

Once the list is complete, the program exits, unless the -p/perpetual option was specificed in which case it starts at the top of the list again. 

This is not a spidering tool; there are already excellent tools for that. The only point was to crate a quick script to generate "clean" traffic.
