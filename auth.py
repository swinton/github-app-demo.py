#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests

import jsonwebtoken


class JWTAuth(requests.auth.AuthBase):
     def __call__(self, r):
        r.headers['Authorization'] = 'bearer {}'.format(jsonwebtoken.generate())
        return r

response = requests.get('https://api.github.com/app',
    auth=JWTAuth(),
    headers=dict(accept='application/vnd.github.machine-man-preview+json'))
print(response.json())
