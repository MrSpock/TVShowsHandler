#!/bin/bash
DOWNLOAD_DIR="/nas/transmission"
LOG="/tmp/tl.log"
SCRIPT_PATH="/etc/scripts"
SUBJECT="TV Show ready to watch"
TVSHOWHANDLER="${SCRIPT_PATH}/tvshowhandler.py"

## Use pushover to send message that TV Show is ready do watch :)
/usr/local/bin/apush "$SUBJECT" "${TR_TORRENT_NAME} is downloaded"

echo "Entering to ${DOWNLOAD_DIR}/${TR_TORRENT_NAME}" >> $LOG
cd "${DOWNLOAD_DIR}/${TR_TORRENT_NAME}"
for tvshow in `ls *.mkv *avi *mp4 2>/dev/null`; do
$TVSHOWHANDLER "${tvshow}"
done

## remove torrent from transmission-daemin
transmission-remote -t ${TR_TORRENT_ID} -r

## Done :-)
