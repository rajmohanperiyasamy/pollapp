#!/bin/bash
set -e
LOGFILE=/home/blackmonk15/webapps/moscowme/blackmonk/deploy/logs/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
USER=blackmonk15
GROUP=blackmonk15
ADDRESS=107.170.120.130:8037
cd /home/blackmonk15/webapps/moscowme/blackmonk
source /home/blackmonk15/.virtualenv/bm/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -D --pid /home/blackmonk15/webapps/moscowme/blackmonk/deploy/guni.pid -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER  --group=$GROUP --log-level=warning\
  --log-file=$LOGFILE 2>>$LOGFILE blackmonk.wsgi:application

