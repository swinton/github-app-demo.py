#!/usr/bin/env python
# -*- coding: utf8 -*-


import os

import requests


class GitHubRequest():
    session = None

    def __init__(self):
        self.domain = os.environ.get('GITHUB_API_DOMAIN', 'api.github.com')
        self.session = requests.Session()
        self.session.headers.update(dict(
            accept='application/vnd.github.machine-man-preview+json'))

    def _request(self, method, path):
        self.response = self.session.request(method, 'https://{}/{}'.format(self.domain, path))
        return self.response.json()

    def _get(self, path):
        return self._request('GET', path)

    def _post(self, path):
        return self._request('POST', path)
