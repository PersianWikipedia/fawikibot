#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of anonymous editors on the wiki in the
last 24 hours and tries to identify proxies within that list.

"""
#
# (C) User:Mensis Mirabilis, 2019
# (C) User:Huji, 2019
#
# Distributed under the terms of the CC-BY-SA license.
#
from __future__ import absolute_import
#

import pywikibot
from pywikibot.data import api
from datetime import datetime, timedelta
from ipwhois import IPWhois
from iptools import IpRange
import config
import json
import requests


class FindProxyBot():

    def __init__(self):
        self.site = pywikibot.Site()
        self.ipcheck_url = 'https://tools.wmflabs.org/ipcheck-dev/index.php'
        self.apikey = config.findproxy['apikey']

    def get_ip_list(self, max_number, max_hours):
        """
        Gathers a list of up to max_number IPs which edited within the last
        max_hours hours in the wiki.
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=max_hours)
        cutoff_ts = cutoff_time.strftime("%Y%m%d%H%M%S")

        gen = api.Request(
                site=self.site,
                parameters={
                    'action': 'query',
                    'list': 'recentchanges',
                    'rcshow': 'anon',
                    'rcprop': 'user|title',
                    'rclimit': str(max_number),
                    'rcend': cutoff_ts})
        data = gen.submit()
        if 'error' in data:
            raise RuntimeError('API query error: {0}'.format(data))
        if data == [] or 'query' not in data:
            raise RuntimeError('No results given.')
        iplist = {x['user'] for x in data['query']['recentchanges']}
        return list(set(iplist))

    def get_cidr_ends(self, cidr):
        """
        Returns the start and end IP address for a given CIDR
        """
        ipr = IpRange(cidr)
        start = ipr[0]
        end = ipr[ipr.__len__() - 1]
        return [start, end]

    def get_ip_info(self, ip):
        """
        TODO: Use caching so that if we already queried an IP from the same
        CIDR then we would not actually run WHOIS again
        """
        request = IPWhois(ip)
        result = request.lookup_rdap(depth=1)
        cidr = result['asn_cidr']
        country = result['asn_country_code']
        if 'start_address' in result.keys():
            start = result['start_address']
            end = result['end_address']
        else:
            start, end = self.get_cidr_ends(cidr)

        return {
            'cidr': cidr,
            'country_code': country,
            'start_address': start,
            'end_address': end
        }

    def query_ipcheck(self, ip):
        """
        Query User:SQL's ipcheck tool to determine if an IP is likely a proxy

        TODO: Ideally, we should use pywikibot.data.api's _http_request method
        to make the webservice call, so that we would not need the dependency
        to json and requests modules.
        """
        session = requests.Session()
        params = {
            'ip': ip,
            'api': True,
            'key': self.apikey
        }
        request = session.get(url=self.ipcheck_url, params=params)
        print(request.text)
        result = request.json()

        result_getipintel = result['getIpIntel']['result']['chance']
        result_proxycheck = result['proxycheck']['result']['proxy']
        result_ipQualityScore = result['ipQualityScore']['result']['proxy']

        if not result['teohio']['error']:
            result_teohio = result['teohio']['result']['vpnOrProxy']

        numerator = (
            float(result_getipintel) / 100 +
                 (result_proxycheck is True) +
                 (result_ipQualityScore is True) +
                 (result_teohio is True))
        denominator = 3 if result_teohio is None else 4
        return numerator / denominator

    def find_proxies(self):
        iplist = self.get_ip_list(10, 24)
        """
        TODO: Loop over the IPs and check if each of them is a proxy or not.
        TODO: Add exception handling for above functions
        """

        ip = iplist[0]
        print(ip)
        print(self.get_ip_info(ip))
        print(self.query_ipcheck(ip))


robot = FindProxyBot()
robot.find_proxies()
