## HAYSTACKR
# Generate clean http network traffic for labs by downloading a list of websites
# Ben Greenbaum, github.com/bgreenba/, @secintsight


#deps: pip install requests argparse bs4
import requests, argparse, sys, time, urllib
from bs4 import BeautifulSoup




# import logging, , sys, configparser, argparse, json

 
def getopts(argv):
    parser = argparse.ArgumentParser(
        description='haystackr',
        epilog='''This script simply generates web requests to a provided list of URLs. It will also request all references resources with a 'src' attribute (eg; img, script)'''
                )
    #program level options
    config=parser.add_argument_group('Configuration','Program configuration settings')
    config.add_argument('-p', '--perpetual', help='loop through the URL list until process is killed',
                        action='store_true')
    config.add_argument('-s', '--sleep_ms', help='sleep value between requests for listed URLs, in milliseconds. (default %(default)s)',
                        type=int, default='100')
    config.add_argument('-v', '--verbose', help='print diagnostic and troubleshooting information to stdout. Once for a reasonable amount, more for lots (0-4)',
                        action='count', default=0)
    config.add_argument('-x', '--experiment', help='Do everything except request the pages. Most useful with -v',
                        action='store_true')
    sources=parser.add_argument_group('URL Sources','Where to get the list of URLs - without at least one of these, it won\'t work')
    sources.add_argument('-a', '--alexa', help='get the most visited top 50 sites from Alexa and add that to the URL list. WARNING: This option may cause your computer to download porn.',
                        action='store_true')
    sources.add_argument('-m', '--moz', help='get the most visited top 500 sites from Moz and add that to the URL list. WARNING: This option may cause your computer to download porn.',
                        action='store_true')  
    sources.add_argument('-l', '--list_file', help='specify a file to add to the list of URLs',
                        type=argparse.FileType('r'))


    #process and gather args
    args = parser.parse_args()
    return(args)

#print messages if msg priority is above user specified verbosity level
def verbose(msg, vlvl=1):
    if args['verbose'] >=vlvl: print(msg,'\n')

#get requested urls
def myget(url):
    try:
        r = requests.get(url)
        verbose('Myget function received and requested URL:'+ r.url+'\n',4)
        if r.status_code // 100 != 2:
            verbose("Error: {} at {}".format(r.status_code,r.url),1)
        return r.content
    except requests.exceptions.RequestException as e:
        return 'Error: Exception - {}'.format(e)


## get ready
# get cmdline options
args=vars(getopts(sys.argv))
verbose('\n'.join(['Command line options, including defaults','\n'.join('{}={}'.format(key, val) for key, val in args.items())]),2)


## Sanity checking
#at least one URL source?
if args['alexa'] is False and args['moz'] is False and args['list_file'] is not True:
    print('no URL sources specified... exiting')
    
#get URLs
urls=[]
#if 'alexa' specified, get list
if args['alexa'] is True:
    verbose ('consulting Alexa for top 50 sites',1)
    r = requests.get('https://www.alexa.com/topsites')
    alexaSoup=BeautifulSoup(r.content,"html.parser")
    for top in alexaSoup.findChildren('div', {"class": "td DescriptionCell"}):
        thistop=top.find('a').string
        topstring=str(thistop)
        verbose('found alexa listing for '+thistop,3)
        urls.append('http://'+thistop.lower()+'/')

#if 'moz' specified, get list
if args['moz'] is True:
    verbose ('consulting Moz for top 500 sites',1)
    r = requests.get('https://moz.com/top500/domains/csv')
    for row in r.content.splitlines():
        url='http://'+str(row).split(',')[1].strip('"')
        verbose('found moz listing for '+url,3)
        urls.append(url)

# if file specified, read list file to get URLs
if args['list_file'] is True:
    verbose('reading list file '+args['list_file'].name)
    file_urls=args['list_file'].readlines()
    urls=urls+file_urls

#make URL list unique
verbose (str(len(urls))+' total URLs',1)
urls=list(set(urls))
verbose (str(len(urls))+' unique URLs',1)


## do the things

#set up the loop:
while True:
    # iterate through list, retrieving each url and each linked object in that response
    verbose('Processing URL list...',1)
    for url in urls:
        url=url.strip()
        if len(url)>0:
            verbose('listed url: '+url,2)
            if args['experiment'] is not True:
                soup=BeautifulSoup(myget(url), "html.parser")
                verbose('following all links to direct referenced object sources:',3)
                links=[]
                for link in soup.find_all(src=True): 
                    verbose('found link: '+link.get('src'),4)
                    newlink=urllib.parse.urljoin(url,link.get('src'))
                    verbose('   directly referenced resource: '+newlink, 4)
                    links.append(newlink)
                ulinks=list(set(links))
                for link in ulinks:
                    myget(link)
            else:
                verbose('Option "experiment" is true, didn\'t fetch',4)

    
            verbose('sleeping for '+str(args['sleep_ms'])+'ms',2)
            time.sleep(args['sleep_ms']/1000)
    if args['perpetual'] is not True:
            exit()

exit()


