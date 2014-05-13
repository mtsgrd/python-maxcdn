import logging
from requests_oauthlib import OAuth1Session as OAuth1
from os import environ as env

try:
    import urlparse
except ImportError: # handly python 3.x
    from urllib import parse as urlparse


"""This is a python API module for MaxCDN services."""

class MaxCDN(object):
    """A class for interacting with the MaxCDN API.

    Reade more at https://github.com/maxcdn/api-docs
    """

    logger = logging.getLogger(__name__)
    max_retries = 5

    def __init__(self, alias, key, secret, server="rws.maxcdn.com", **kwargs):
        self.url    = "https://%s/%s" % (server, alias)
        self.client = OAuth1(key, client_secret=secret, **kwargs)


    def _make_request(self, method, *args, **kwargs):
        while retries > 0:

    def _get_headers(self, json=True):
        headers = { "User-Agent": "Python MaxCDN API Client" }
        if json:
            headers["Content-Type"] = "application/json"
        return headers

    def _get_url(self, end_point):
        if not end_point.startswith("/"):
            return "%s/%s" % (self.url, end_point)
        else:
            return self.url + end_point

    def _data_request(self, method, end_point, data, **kwargs):
        if data is None and "params" in kwargs:
            params = kwargs.pop("params")
            if type(params) is str:
                params = urlparse.parse_qs(params)
            data = params
        self.logger.debug('Requesting %s', self._get_url(end_point))
        method = getattr(self.client, method) 
        return self._make_request(method, self._get_url(end_point), data=data,
                headers=self._get_headers(json=True), **kwargs)

    def get(self, end_point, **kwargs):
        self.logger.debug('Requesting %s', self._get_url(end_point))
        return self.client.get(self._get_url(end_point),
                headers=self._get_headers(json=False), **kwargs)

    def patch(self, end_point, data=None, **kwargs):
        return self._data_request("post", end_point, data=data, **kwargs)

    def post(self, end_point, data=None, **kwargs):
        return self._data_request("post", end_point, data=data, **kwargs)

    def put(self, end_point, data=None, **kwargs):
        return self._data_request("put", end_point, data=data, **kwargs)

    def delete(self, end_point, data=None, **kwargs):
        return self._data_request("delete", end_point, data=data, **kwargs)

    def purge(self, zoneid, file_or_files=None, **kwargs):
        path = "/zones/pull.json/%s/cache" % (zoneid)
        if file_or_files is not None:
            return self.delete(path, data = { "files": file_or_files },
                    **kwargs)
        self.logger.debug('Purging %s from %s', zoneid, file_or_files)
        return self.delete(path, **kwargs)

