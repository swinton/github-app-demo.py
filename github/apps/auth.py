#!/usr/bin/env python
# -*- coding: utf8 -*-

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


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, app, access_token):
        self._app = app
        self._access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'token {}'.format(self._access_token['token'])
        return r
