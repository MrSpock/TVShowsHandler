# TVShowsHandler
Script for automatically move downloaded TV Shows to directory structure compatible with PLEX media server and find and download subtitles.
This script used as "script-torrent-done-filename" hook in transmission-remote settings.json will make all magic descibed below.

### Description
I'm lazy. Really lazy :) When some TV Show episode is downloaded before my wife can watch it I need to:
- move video file to proper PLEX location (sometime you need to create new folders when new season start)
- sanitize tv show filename so they are all consistent and easy readable
- download subtitles and convert them to SRT UTF8 encoded format

When you watch a lot of shows that is many tasks. How about just automate all this ? :)

### Howto
- put two scripts somewhere. Mine are in /etc/scripts
- edit settings.json and provide path to transmission-done.sh for script-torrent-done-filename variable. Remember to shutdown daemin before makeing any changes. Otherwise you will loose your changes when daemn be restarted.
- check permissions to PLEX root folder transmission-daemon user
- set all CAPITAL letters variables in transmission-done.sh file begining
- set variables in tvshowhandler.py (TVSHOWS_PATH - your PLEX root for TV Shows,SUBTITLE_DOWNLOAD, NAPI_SH_PATH)

All done !

