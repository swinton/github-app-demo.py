#!/usr/bin/env python

import sys
import os
import json

import requests

from sseclient import SSEClient as Client

# Allow interruption via `kill -s INT`
# https://stackoverflow.com/a/40785230
import signal; signal.signal(signal.SIGINT, signal.default_int_handler)

try:
    # Connect to stream
    stream = Client(os.environ['WEBHOOK_PROXY_URL'])

    # Prepare session
    session = requests.Session()

    for event in stream:
        # Parse JSON data
        data = json.loads(event.data)

        # Log event
        print "event", event.event, data

        # Deliver data to local Flask app
        if event.event == 'message':
            session.post('http://localhost:5000', json=data['body'])

except KeyboardInterrupt as e:
    print 'Done.'
    sys.exit(0)
