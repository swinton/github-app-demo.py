#!/usr/bin/env python
# -*- coding: utf8 -*-

import github


if __name__ == '__main__':
    import pprint
    
    app = github.GitHubApp()
    installation = app.get_installation('swinton')
    pprint.pprint(installation.get_repositories())
