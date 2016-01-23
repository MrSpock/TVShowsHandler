#!/usr/bin/env python

## This tool will try to smart detect TV show metadadas(title,episode,season)
## remove all useless data and move it to destination according to PLEX
## guidelines (Show Name/Season No/Show.Title.S01E01.720p.mkv)
## Spock - spock@omegastar.eu

import sys
from os import path,chmod
import re
from distutils.dir_util import mkpath
from distutils.file_util import move_file
from subprocess import check_output
import stat


## some defaults
## CHANGEME ! - change this to your plex video root
TVSHOWS_PATH="/nas/Video/Seriale"
## default umask 644 for subtitles
## this requires napi.sh (https://github.com/dagon666/napi)
SUBTITLE_DOWNLOAD=True
NAPI_SH_PATH="/usr/bin/napi.sh"
SUBTITLE_DEFAULT_PERMISSIONS = stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IROTH

class TVShow:
    def __init__(self):
        self.title = ""
        self.season = ""
        self.episode = ""
        self.resolution = ""
        self.container = ""
    def __repr__(self):
        return "TVShow(title:{0}, season:{1}, episode:{2}, resolution:{3})".format(self.title.replace("."," "),self.season,self.episode,self.resolution)


pattern="(.*)\.(S\d+|s\d+)(E\d+|e\d+)\.(720p|1080p|HDTV)(.*)\.(\w{3})"
#pattern="(.*)\.(S\d+|s\d+)(E\d+|s\d+e\d+)\.(720p|1080p)(.*)"

## try to split video name to its parts and extract video metadata
def get_metadata(fname):
   rs = re.match(pattern,fname)
   if rs:
    show = TVShow()
    metadata = rs.groups()
    if len(metadata) >= 5:
        show.title,show.season,show.episode,show.resolution,misc,show.container= metadata
        return show
    else:
        return nil

## small function that will return "Season No" part of path
def get_season(show):
    rs = re.match("(S|s)(\d+)",show.season)
    if rs:
        data = rs.groups()
        if len(data) == 2:
            try:
                result="Season %i" % int(data[1])
            except:
                return nil
            return result
        return nil

## build full path to final TV Episode location including PLEX root, Show Name, Season     
def build_storage_path(show):
    season = get_season(show)
    title = show.title.replace(".", " ")
    if season:
        tv_show_path = path.join(TVSHOWS_PATH," ".join([x.capitalize() for x in title.split()]),season)
        return tv_show_path
    else:
        return False

# execute mkdir and make physical changes on storage device      
def make_storage_path(path):
    mkpath(path)

# make_new_name - generate clear tv show name containing
# Title.Season.Episode.resolution.ext (The.100.S01E01.720p.mkv)
def make_new_name(show):
    return "{0}.{1}{2}.{3}.{4}".format(".".join([x.capitalize() for x in show.title.split(".")]),show.season.upper(),show.episode.upper(),show.resolution,show.container)

## this requires napi.sh (https://github.com/dagon666/napi)
## for automatic subtitles download 
def download_subtitles(movie_path):
            if SUBTITLE_DOWNLOAD:
                out = check_output([NAPI_SH_PATH,movie_path])
                # napisy sie pobraly czyli nie znaleziono ciagu UNAV
                # poprawiam umask napisow (https://github.com/dagon666/napi/issues/33)
                if out.find("UNAV") < 0:
                    subtitle_file=movie_path.split(".")[:-1]
                    subtitle_file.append("srt")
                    subtitle_file=".".join(subtitle_file)
                    chmod(subtitle_file,SUBTITLE_DEFAULT_PERMISSIONS)

# launch from cli if not used as module
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # extract final filename
        filename=path.split(sys.argv[1])[-1]
        show = get_metadata(filename)
        if show:
            dest_d=build_storage_path(show)
            dest_f=make_new_name(show)
            make_storage_path(dest_d)
            print("Moving {0} -> {1}".format(filename,path.join(dest_d,dest_f)))
            print(move_file(sys.argv[1],path.join(dest_d,dest_f)))
            ## dociagamy napisy
            download_subtitles(path.join(dest_d,dest_f))
        else:
            print "Show not parsed"

