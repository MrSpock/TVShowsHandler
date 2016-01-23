#!/bin/bash
DOWNLOAD_DIR="/nas/transmission"
LOG="/tmp/tl.log"
SCRIPT_PATH="/etc/scripts"
SUBJECT="TV Show ready to watch"
TVSHOWHANDLER="${SCRIPT_PATH}/tvshowhandler.py"

function log {
timestamp=`date +"%Y-%m-%d %H:%M:%S"`
printf "${timestamp} $1\n" >> $LOG
}

## Use pushover to send message that TV Show is ready do watch :)
log "Sending pushover notification for ${TR_TORRENT_NAME}"
/usr/local/bin/apush "$SUBJECT" "${TR_TORRENT_NAME} is downloaded"

if [ -d "${DOWNLOAD_DIR}/${TR_TORRENT_NAME}" ]; then
	log "Entering to ${DOWNLOAD_DIR}/${TR_TORRENT_NAME}"
	cd "${DOWNLOAD_DIR}/${TR_TORRENT_NAME}"
	for tvshow in `ls *.mkv *avi *mp4 2>/dev/null`; do
	$TVSHOWHANDLER "${tvshow}"
	done
else
	log "Single file downloaded. Processing with tvshowhandler (${DOWNLOAD_DIR}/${TR_TORRENT_NAME})"
	$TVSHOWHANDLER "${DOWNLOAD_DIR}/${TR_TORRENT_NAME}"
fi


## remove torrent from transmission-daemin
transmission-remote -t ${TR_TORRENT_ID} -r

## Done :-)
