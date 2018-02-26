#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import time

import jwt

import requests


class NoInstallationException(Exception):
    pass


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


class GitHubApp(GitHubRequest):
    private_key = None

    def __init__(self):
        super().__init__()
        self.session.auth = JWTAuth(
            iss=os.environ['APP_ID'],
            key=self.read_private_key())

    def read_private_key(self):
        if self.private_key is None:
            with open(os.environ['PRIVATE_KEY_FILE']) as fp:
                self.private_key = fp.read()
        return self.private_key

    def get_app(self):
        return self._get('app')

    def get_installations(self):
        return self._get('app/installations')

    def get_installation(self, login):
        installation = [installation for
            installation in self.get_installations()
                if installation['account']['login'] == login]

        if len(installation) > 0:
            return GitHubAppInstallation(self,
                installation[0],
                self.get_installation_access_token(installation[0]['id']))

        else:
            raise NoInstallationException(
                'No installation found for "{}".'.format(login))

    def get_installation_access_token(self, installation_id):
        return self._post('installations/{}/access_tokens'
                .format(installation_id))


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, app, access_token):
        self._app = app
        self._access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'token {}'.format(self._access_token['token'])
        return r


class GitHubAppInstallation(GitHubRequest):
    def __init__(self, app, installation_dict, access_token):
        super().__init__()

        self._app = app
        self._dict = installation_dict
        self._access_token = access_token

        for k in installation_dict:
            setattr(self, k, installation_dict[k])

        self.session.auth = TokenAuth(app, access_token)

    def get_repositories(self):
        return self._get('installation/repositories')


if __name__ == '__main__':
    import pprint

    app = GitHubApp()
    installation = app.get_installation('swinton')
    pprint.pprint(installation.get_repositories())
