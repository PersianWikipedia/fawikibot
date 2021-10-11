#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot checks if any IP in a list may be an open proxy

The list must be a plain text file where each row is a single IP address
"""
#
# (C) User:Mensis Mirabilis, 2019
# (C) User:Huji, 2020
#
# Distributed under the terms of the CC-BY-SA license.
#
from __future__ import absolute_import
#

import config
import json
import requests
import re
import os
from ipwhois import IPWhois
from cidr_trie import PatriciaTrie
import argparse


class ProxyCheckBot():

    def __init__(self, path=None, nowiki=None):
        self.path = path
        self.IPQSkey = config.findproxy['IPQSkey']
        self.PCkey = config.findproxy['PCkey']
        self.GIIemail = config.findproxy['GIIemail']
        self.IPv4cache = PatriciaTrie()
        self.IPv6cache = PatriciaTrie()

    def load_ip_list(self, path):
        # If path starts with ~ make it an absolute path
        path = os.path.expanduser(path)
        if not os.path.isfile(path):
            print('Provided path does not exist')
            exit()
        fh = open(path)
        lines = fh.read().splitlines()
        fh.close()
        return lines

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
            self.query_GetIPIntel(ip)
        ]

    def format_result(self, res):
        if res == 1:
            return '{{yes}}'
        elif res == 0:
            return '{{no}}'

    def progress(self, str):
        """
        Displays a progress message to the user.
        The message is updated as IPs are checked or skipped.
        The message will be removed in the end, once final output is printed.
        """
        blank = '                                                             '
        print(blank, end='\r')
        print(str, end='\r')

    def run(self):
        out = '{| class="wikitable sortable"\n'
        out += '! IP !! CIDR !! Country !! ' +\
               'IPQualityScore !! proxycheck !! GetIPIntel'

        if self.path is None:
            print('Error: no IP list provided!')
            exit()
        else:
            iplist = self.load_ip_list(self.path)

        rowtemplate = '\n|-\n| %s || %s || %s || %s || %s || %s'

        for ip in iplist:
            ipinfo = self.get_ip_info(ip)
            if ipinfo['country_code'] == 'IR':
                """
                IPs from Iran are almost never proxies, skip the checks
                """
                self.progress('Skipping %s' % ip)
                pass
            else:
                self.progress('Checking %s' % ip)
                IPQS, PC, GII = self.run_queries(ip)
                row = rowtemplate % (
                    ip,
                    ipinfo['cidr'],
                    ipinfo['country_code'],
                    self.format_result(IPQS),
                    self.format_result(PC),
                    self.format_result(GII)
                )
                out += row

        out += '\n|}'

        print(out)


parser = argparse.ArgumentParser()
parser.add_argument('--path', help='path to text file containing IP list')
args = parser.parse_args()

robot = ProxyCheckBot(args.path)
robot.run()
