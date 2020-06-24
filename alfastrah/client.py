# -*- coding: utf-8 -*-
import json

import requests


class AlfaStrahClient:
    API_HOST = ''

    def __init__(self, api_key, verify_ssl=True):
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.req = self.resp = None

    def request(self, method, endpoint, data=None):
        """Constructs and sends a request to API Gateway.

        :param method: HTTP method, e.g. 'GET', 'POST', 'PUT', 'DELETE'.
        :type method: str
        :param endpoint: API endpoint, e.g. '/travel-ext-services/api/v2/products'.
        :type endpoint: str
        :param data: (optional) dictionary of parameters to send in the query.
        :param data: dict or None
        :return: main content of the response API.
        :rtype: object
        """
        headers = {
            'X-API-Key': self.api_key,
        }
        self.req = json.dumps(data, cls=MultiJSONEncoder)
        url = '{api_host}{endpoint}'.format(api_host=self.API_HOST, endpoint=endpoint)
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
