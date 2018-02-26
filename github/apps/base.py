#!/usr/bin/env python
# -*- coding: utf8 -*-


import os

from . import request
from . import auth
from . import installation
from . import exceptions


class GitHubApp(request.GitHubRequest):
    private_key = None

    def __init__(self):
        super().__init__()
        self.session.auth = auth.JWTAuth(
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
        inst = [inst for inst in self.get_installations()
                    if inst['account']['login'] == login]

        if len(inst) > 0:
            return installation.GitHubAppInstallation(self,
                inst[0],
                self.get_installation_access_token(inst[0]['id']))

        else:
            raise exceptions.NoInstallationException(
                'No installation found for "{}".'.format(login))

    def get_installation_access_token(self, installation_id):
        return self._post('installations/{}/access_tokens'
                .format(installation_id))
