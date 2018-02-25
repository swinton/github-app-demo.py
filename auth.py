#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Authenticate as a GitHub App:
https://developer.github.com/apps/building-github-apps/authentication-options-for-github-apps/#authenticating-as-a-github-app
"""

import os
import time

import jwt

import requests


class JWTAuth(requests.auth.AuthBase):
    def __init__(self, iss, key, expiration=10 * 60):
        self.iss = iss
        self.key = key
        self.expiration = expiration

    def generate_token(self):
        # Generate the JWT
        payload = {
          # issued at time
          'iat': int(time.time()),
          # JWT expiration time (10 minute maximum)
          'exp': int(time.time()) + self.expiration,
          # GitHub App's identifier
          'iss': self.iss
        }

        tok = jwt.encode(payload, self.key, algorithm='RS256')

        return tok.decode('utf-8')

    def __call__(self, r):
        r.headers['Authorization'] = 'bearer {}'.format(self.generate_token())
        return r

with open(os.environ['PRIVATE_KEY_FILE']) as fp:
    private_pem = fp.read()

authorization = JWTAuth(
    iss=os.environ['APP_ID'],
    key=private_pem)

response = requests.get('https://api.github.com/app',
    auth=authorization,
    headers=dict(accept='application/vnd.github.machine-man-preview+json'))

# Print the response
print(response.json())
