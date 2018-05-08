# haystackr
A simple tool to generate web traffic, primarily intended for making infosec lab exercises more realistic.

## usage: haystackr.py [-h] [-p] [-s SLEEP_MS] [-v] [-x] [-a] [-m] [-l LIST_FILE]

optional arguments:
  -h, --help            show this help message and exit

## Configuration:  Program configuration settings
switch|description
-|-
  -p, --perpetual       |loop through the URL list until process is killed
  -s SLEEP_MS, --sleep_ms SLEEP_MS                        |sleep value between requests for listed URLs, in
                        milliseconds. (default 100)
                        
  -v, --verbose        |print diagnostic and troubleshooting information to
                        stdout. Once for a reasonable amount, more for lots
                        (0-4)
                        
  -x, --experiment      |Do everything except request the pages. Most useful
                        with -v
                        
                        

## URL Sources:  Where to get the list of URLs - without at least one of these, it won't work
  switch|description
  -|-
  -a, --alexa           |get the most visited top 50 sites from Alexa and add
                        that to the URL list. WARNING: This option may cause
                        your computer to download porn.
                        
  -m, --moz            |get the most visited top 500 sites from Moz and add
                        that to the URL list. WARNING: This option may cause
                        your computer to download porn
                        .
  -l LIST_FILE, --list_file LIST_FILE  |specify a file to add to the list of URLs

This script simply generates web requests to a provided list of URLs. It will 
also request all references resources with a 'src' attribute (eg; img, script)
