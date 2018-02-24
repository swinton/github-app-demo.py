#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import time

import jwt


def generate():
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
        private_pem = fp.read()

    jwt_token = jwt.encode(payload, private_pem, algorithm='RS256')

    return jwt_token.decode('utf-8')


if __name__ == '__main__':
    print(generate())
