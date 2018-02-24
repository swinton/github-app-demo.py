#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import time

import requests
import jwt


# Generate the JWT
payload = {
  # issued at time
  'iat': int(time.time()),
  # JWT expiration time (10 minute maximum)
  'exp': int(time.time()) + (10 * 60),
  # GitHub App's identifier
  'iss': os.environ['APP_ID']
}

with open(os.environ['PRIVATE_KEY_FILE']) as fp:
    private_key = fp.read()
encoded = jwt.encode(payload, private_key, algorithm='RS256')

print "👋", encoded
