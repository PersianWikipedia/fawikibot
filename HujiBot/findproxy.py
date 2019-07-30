#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of anonymous editors on the wiki in the
last few hours and tries to identify proxies within that list.

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
import re
from cidr_trie import PatriciaTrie


class FindProxyBot():

    def __init__(self):
        self.site = pywikibot.Site()
        self.target = 'User:Mensis Mirabilis/کشف پروکسی'
        self.summary = 'روزآمدسازی نتایج'
        self.blocksummary = '{{پروکسی باز}}'
        self.IPQSkey = config.findproxy['IPQSkey']
        self.PCkey = config.findproxy['PCkey']
        self.GIIemail = config.findproxy['GIIemail']
        self.IPv4cache = PatriciaTrie()
        self.IPv6cache = PatriciaTrie()

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

    def get_cache(self, ip):
        pat = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.match(pat, ip) is None:
            """
            Temporary fix for https://github.com/Figglewatts/cidr-trie/issues/2
            """
            if self.IPv6cache.size == 0:
                return []
            return self.IPv6cache.find_all(ip)
        else:
            return self.IPv4cache.find_all(ip)

    def set_cache(self, ip, cidr, country):
        pat = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.match(pat, ip) is None:
            self.IPv6cache.insert(cidr, country)
        else:
            self.IPv4cache.insert(cidr, country)

    def get_ip_info(self, ip):
        """
        Retrieves pertinent fields from IP WHOIS information
        """
        cached_info = self.get_cache(ip)

        if len(cached_info) == 0:
            try:
                request = IPWhois(ip)
                result = request.lookup_rdap(depth=1)
                cidr = result['asn_cidr']
                country = result['asn_country_code']
                self.set_cache(ip, cidr, country)
            except Exception:
                cidr = ''
                country = ''
        else:
            cidr = cached_info[0][0]
            country = cached_info[0][1]

        return {
            'cidr': cidr,
            'country_code': country
        }

    def query_IPQualityScore(self, ip):
        """
        Queries the IPQualityScore API to check if an IP is a proxy
        """
        url = 'https://www.ipqualityscore.com/api/json/ip/%s/%s'
        request = requests.get(url % (self.IPQSkey, ip))
        result = request.json()
        if 'proxy' in result.keys():
            return 1 if result['proxy'] is True else 0
        else:
            return False

    def query_proxycheck(self, ip):
        """
        Queries the proxycheck.io API to check if an IP is a proxy
        """
        url = 'http://proxycheck.io/v2/%s?key=%s&vpn=1'
        request = requests.get(url % (ip, self.PCkey))
        result = request.json()
        if ip in result.keys() and 'proxy' in result[ip]:
            return 1 if result[ip]['proxy'] == 'yes' else 0
        else:
            return False

    def query_GetIPIntel(self, ip):
        """
        Queries the GetIPIntel API to check if an IP is a proxy
        """
        url = 'http://check.getipintel.net/check.php' + \
              '?ip=%s&contact=%s&format=json&flags=m'
        request = requests.get(url % (ip, self.GIIemail))
        result = request.json()
        if 'result' in result.keys():
            return 1 if result['result'] == '1' else 0
        else:
            return False

    def query_teoh_io(self, ip):
        """
        Queries the teoh.io API to check if an IP is a proxy
        """
        url = 'https://ip.teoh.io/api/vpn/%s'
        request = requests.get(url % ip)
        """
        Sadly, teoh.io sometimes generates PHP notices before the JSON output.
        Therefore, we will have to find the actual JSON output and parse it.
        """
        result = request.text
        if result[0] != '{':
            result = result[result.find('{'):]
        result = json.loads(result)

        if 'vpn_or_proxy' in result.keys():
            return 1 if result['vpn_or_proxy'] == 'yes' else 0
        else:
            return False

    def run_queries(self, ip):
        return [
            self.query_IPQualityScore(ip),
            self.query_proxycheck(ip),
            self.query_GetIPIntel(ip),
            self.query_teoh_io(ip)
        ]

    def format_result(self, res):
        if res == 1:
            return '{{yes}}'
        elif res == 0:
            return '{{no}}'
        else:
            return '{{yes-no|}}'

    def find_proxies(self):
        out = '{| class="wikitable sortable"\n'
        out += '! آی‌پی !! CIDR !! کد کشور !! ' +\
               'IPQualityScore !! proxycheck !! GetIPIntel !! teoh.ir !! ' +\
               'بسته شد'

        iplist = self.get_ip_list(1000, 24)
        rowtemplate = '\n|-\n| %s || %s || %s || %s || %s || %s || %s || %s'

        for ip in iplist:
            pywikibot.output('Checking %s' % ip)
            ipinfo = self.get_ip_info(ip)
            if ipinfo['country_code'] == 'IR':
                """
                IPs from Iran are almost never proxies, skip the checks
                """
                pass
            else:
                IPQS, PC, GII, TEOH = self.run_queries(ip)
                if IPQS + PC + GII + TEOH == 4:
                    target = pywikibot.User(self.site, ip)
                    if target.isBlocked():
                        blocked = 2
                    else:
                        self.site.blockuser(
                            target, '1 year', self.blocksummary,
                            anononly=False, allowusertalk=True)
                        blocked = 1
                else:
                    blocked = 0
                row = rowtemplate % (
                    ip,
                    ipinfo['cidr'],
                    ipinfo['country_code'],
                    self.format_result(IPQS),
                    self.format_result(PC),
                    self.format_result(GII),
                    self.format_result(TEOH),
                    self.format_result(blocked)
                )
                out += row

        out += '\n|}'

        page = pywikibot.Page(self.site, self.target)
        page.text = out
        page.save(self.summary)


robot = FindProxyBot()
robot.find_proxies()
