#!/bin/bash

# NOTIFY_HOME and NOTIFY_RECIPIENT are set in dotenv.  Sourcing this outside the working directory
# requires that they be discoverable from a known location, /opt/event-notify/dotenv.  The preamble
# of this script ensures that the symbolic link and dotenv file are available.

if [ ! -h /opt/event-notify ]; then
	>&2 echo "error: missing symbolic link /opt/event-notify to install directory"
	exit 1
elif [ ! -f /opt/event-notify/dotenv ]; then 
	>&2 echo "error: missing dotenv file"
	exit 1
else
	source /opt/event-notify/dotenv
fi

if [ "$1" = '--rebuild' ] || [ -z "$(docker images -q event-notify:latest 2> /dev/null)" ]; then
	docker build --tag event-notify:latest .
fi

if [ "$1" = '--rebuild' ]; then
	shift
fi

docker run -it --rm \
	-v ${NOTIFY_HOME}/conf:/home/notify/conf \
	-v ${NOTIFY_HOME}/templates:/home/notify/templates \
	event-notify ${NOTIFY_RECIPIENT} "$@"
