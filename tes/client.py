# -*- coding: utf-8 -*-
import json

import requests


class AlfaInsTESClient:
    api_host = ''
    base_path = '/travel-ext-services/api/v2'

    def __init__(self, api_key, verify_ssl=True):
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.req = self.resp = None

    def request(self, method, path, data=None):
        """Constructs and sends a request to API Gateway.

        :param method: HTTP method, e.g. 'GET', 'POST', 'PUT', 'DELETE'.
        :type method: str
        :param path: API path, e.g. '/products'.
        :type path: str
        :param data: (optional) dictionary of parameters to send in the query.
        :param data: dict or None
        :return: main content of the response API.
        :rtype: object
        """
        headers = {
            'X-API-Key': self.api_key,
        }
        self.req = json.dumps(data, cls=MultiJSONEncoder)
        url = '{api_host}{base_path}{path}'.format(api_host=self.api_host, base_path=self.base_path, path=path)
        r = requests.request(method, url,
                             headers=headers, data=self.req, verify=self.verify_ssl)
        self.resp = r.json()
        return self.resp


class MultiJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json') and callable(o.to_json):
            return o.to_json()
        # Let the base class default raise the TypeError
        return json.JSONEncoder.default(self, o)
