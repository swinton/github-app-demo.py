#!/usr/bin/env python
# -*- coding: utf8 -*-

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


class GitHubApp():
    session = None
    private_key = None

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = JWTAuth(
            iss=os.environ['APP_ID'],
            key=self.read_private_key())
        self.session.headers.update(dict(
            accept='application/vnd.github.machine-man-preview+json'))

    def read_private_key(self):
        if self.private_key is None:
            with open(os.environ['PRIVATE_KEY_FILE']) as fp:
                self.private_key = fp.read()
        return self.private_key

    def _request(self, method, url):
        self.response = self.session.request(method, url)
        return self.response.json()

    def _get(self, url):
        return self._request('GET', url)

    def _post(self, url):
        return self._request('POST', url)

    def get_app(self):
        return self._get('https://api.github.com/app')

    def get_installations(self):
        return self._get('https://api.github.com/app/installations')

    def get_installation_access_token(self, installation_id):
        return self._post('https://api.github.com/installations/{}/access_tokens'
                .format(installation_id))

if __name__ == '__main__':
    import pprint

    app = GitHubApp()
    pprint.pprint(app.get_app())

    installations = app.get_installations()
    pprint.pprint(installations)
    pprint.pprint([(installation['id'], app.get_installation_access_token(installation['id'])) for installation in installations])
