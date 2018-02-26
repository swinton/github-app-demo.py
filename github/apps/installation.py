#!/usr/bin/env python
# -*- coding: utf8 -*-


from . import request
from . import auth


class GitHubAppInstallation(request.GitHubRequest):
    def __init__(self, app, installation_dict, access_token):
        super().__init__()

        self._app = app
        self._dict = installation_dict
        self._access_token = access_token

        for k in installation_dict:
            setattr(self, k, installation_dict[k])

        self.session.auth = auth.TokenAuth(app, access_token)

    def get_repositories(self):
        return self._get('installation/repositories')
