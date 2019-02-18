#!/bin/bash

# try to curl-get ${APP_HOST}:${APP_PORT} for 30 seconds to check that app is running

APP_HOST="${APP_HOST:-localhost}"
APP_PORT="${APP_PORT:-8000}"
echo "APP_HOST=${APP_HOST} APP_PORT=${APP_PORT}"

RUNNING=false
for _ in $(seq 10); do
		if curl --get --head "${APP_HOST}":"${APP_PORT}" 2>/dev/null; then
			RUNNING=true
		  break
		fi
		echo "Waiting for app (${APP_HOST}:${APP_PORT})..."
		sleep 3
done

( [[ "$RUNNING" == true ]] && exit 0 ) || exit 1
