# = = = = =  AUTO-RSS  = = = = = #
# Automatically checks RSS feeds with downloadable links (from soundcloud, youtube, etc) and only downloads new entries
# Dependencies: python feedparser, youtube-dl package.
# HOW-TO: Add all feed links in the list rss_feeds, schedule this program to run however often with crontab -e
# By Jesse Wallace (c0deous)
# http://c0deo.us
# Copyright 2015

import os, sys, feedparser

# Feeds #
rss_feeds = ['http://feeds.soundcloud.com/users/soundcloud:users:82926214/sounds.rss', 'http://feeds.soundcloud.com/users/soundcloud:users:27399956/sounds.rss']

# Feed Cache Location #
autorss_dir = "./.autorss/" # Will be created if it doesn't exist
autorss_cachefile_ext = ".arss"

# Debugging #
autorss_debug = False
autorss_dl_debug = False # Enables downloading while in debug mode

# youtube-dl #
ytdl_xopts = '' # Extra options to append to the youtube-dl command
ytdl_audio_format = 'mp3' # Pipes into the --audio-format youtube-dl option.  For help run 'man youtube-dl'


# Functions #

# ANSI Colors #
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def colored(text, color):
    try:
        colorcode = getattr(bcolors, color)
        print(colorcode + text + bcolors.ENDC)
    except AttributeError:
        print(text)


def dbg(debugmessage): # A simple function that enables debug messages when set
    if autorss_debug == True:
        colored('    ' + debugmessage, 'OKBLUE')

def ytdl(link):
    dbg('[/] Printing userland message about link (' + link + ') and format (' + ytdl_audio_format + ')...')
    print('[+] Downloading ' + link + ' as a .' + ytdl_audio_format + '...')
    if autorss_debug != True or autorss_dl_debug == True: # Set 'autorss_dl_debug' var to True to debug downloads.  Default debug mode disables them.
        dbg('[/] Downloading during debug because autorss_dl_debug is set to True...') 
        ytdl_dl_cmd = 'youtube-dl -x --audio-format ' + ytdl_audio_format + ' ' + link + ' ' + ytdl_xopts
        dbg('[/] Download command: $ ' + ytdl_dl_cmd)
        os.system(ytdl_dl_cmd)
    else:
        dbg('[/] Disabled downloads during debugging for testing purposes.  Enable by setting autorss_dl_debug and autorss_debug to True...')
        print('[+] Skipped Download due to the "autorss_debug" cvar being set to True...')


def main():
    if autorss_debug == True:
        dbg('[/] Program Settings for Debug [/]')
        dbg('[/] RSS Feeds [rss_feeds]:\n')
        for i in rss_feeds:
            dbg(i + '\n')
        dbg('[/] Caching directory [autorss_dir]: ' + str(autorss_dir))
        dbg('[/] Cache file extension [autorss_cachefile_ext]: ' + str(autorss_cachefile_ext))
        dbg('[/] Debug [autorss_debug]: ' + str(autorss_debug))
        dbg('[/] Download Debug [autorss_dl_debug]: ' + str(autorss_dl_debug))
        dbg('[/] Youtube-dl Extra Options [ytdl_xopts]: ' + str(ytdl_xopts))
        dbg('[/] Youtube-dl Audio Format [ytdl_audio_format]: ' + str(ytdl_audio_format))
        print(' ')

    for i in rss_feeds:
        dbg('[/] Parsing Feed... [var=feed]')
        feed = feedparser.parse(i) # Grab feed elements
        dbg('[/] Grabbing Link from parsed feed... [var=link]')
        link = feed.entries[0]['link']
        dbg('[/] Grabbing Feed Title from parsed feed... [var=title]')
        title = feed['feed']['title']
        dbg('[/] Grabbing Newest Entry from parsed feed... [var=itemname]')
        itemname = feed.entries[0]['title']
        dbg('[/] Printing Link, Feed Title, and Newest Entry Name for everybody in userland...')
        dbg(' ')
        print('Link: ' + str(link))
        print('Feed Title: ' + str(title))
        print('Newest Entry Name: ' + str(itemname))
        dbg(' ')
        dbg("[/] Creating caching directory if it doesn't exist at " + autorss_dir + "...")
        if not os.path.exists(autorss_dir): # Create caching dir if not exists
            os.makedirs(autorss_dir)
        testname = 'test'
        def querycache():
            dbg('[/] Attempting to open cachefile at ' + autorss_dir + title + autorss_cachefile_ext + '... [var=cachefile, openmode=w+]')
            with open(autorss_dir + title + autorss_cachefile_ext, 'w+') as cachefile:
                dbg('[/] Searching cachefile (' + autorss_dir + title + autorss_cachefile_ext + ') for "' + itemname + '\"...')
                for line in cachefile:
                    if itemname in line:
                        dbg('[/] querycache() found the cachefile populated with the newest item name (' + itemname + ')...')
                        dbg('[/] Closing cachefile (' + autorss_dir + title + autorss_cachefile_ext + ') and returning "found"...')
                        cachefile.close()
                        return 'found'
                    else:
                        dbg('[/] querycache() did not find the newest item name (' + itemname + ') within the cachefile (' + autorss_dir + title + autorss_cachefile_ext + ')...')
                        dbg('[/] Closing cachefile (' + autorss_dir + title + autorss_cachefile_ext + ') and returning "not found"...')
                        cachefile.close()
                        return 'not found'
        dbg('[/] Beginning cachefile query... [func=querycache()]')
        query = querycache()
        if query == 'found':
            dbg('[/] Translating querycache() output into english understood by userland [no new entries]...')
            dbg(' ')
            print('[*] No new RSS Feed Entries for: ' + title)
        else:
            dbg('[/] Translating querycache() output into english understood by userland [new entry found]...')
            dbg(' ')
            print('[+] New RSS Feed Entry: ' + itemname)
            dbg(' ')
            dbg('[/] Opening cachefile (' + autorss_dir + title + autorss_cachefile_ext + ') to log the newest entry name (' + itemname + ')... [var=cachefile, openmode=w+]')
            with open(autorss_dir + title + '.arss', 'w+') as cachefile:
                dbg('[/] Overwriting cachefile entry with new entry name (' + itemname + ')...')
                cachefile.write(itemname)
                dbg('[/] Closing cachefile...')
                cachefile.close()
            dbg('[/] Passing link (' + link + ') to ytdl()...')
            dbg(' ')
            ytdl(link)
if __name__ == '__main__':
    dbg('[/] Program Debug BEGIN [/]')
    main()
