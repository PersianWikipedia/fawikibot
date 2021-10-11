#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of long term IP blocks on the wiki and tries to
identify if any of them are proxies. If so, it extends the block for another
year.
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
import MySQLdb as mysqldb
from ipwhois import IPWhois
import config
import json
import requests
import re
from cidr_trie import PatriciaTrie


class FindProxyBot():

    def __init__(self):
        self.site = pywikibot.Site()
        self.target = 'ویکی‌پدیا:گزارش دیتابیس/تمدید بستن پروکسی'
        self.summary = 'روزآمدسازی نتایج (وظیفه ۲۳)'
        self.blocksummary = '{{پروکسی باز}}'
        self.IPQSkey = config.findproxy['IPQSkey']
        self.PCkey = config.findproxy['PCkey']
        self.GIIemail = config.findproxy['GIIemail']
        self.IPv4cache = PatriciaTrie()
        self.IPv6cache = PatriciaTrie()

    def get_ip_list(self):
        """
        Gathers a list of IPs with a long-term block that is about to expire.
        """
        conn = mysqldb.connect(
            host='fawiki.web.db.svc.wikimedia.cloud',
            db='fawiki_p',
            read_default_file='~/replica.my.cnf'
        )
        cursor = conn.cursor()
        query = """
SELECT
  ipb_address,
  STR_TO_DATE(LEFT(ipb_expiry, 8), '%Y%m%d') AS start_date,
  STR_TO_DATE(LEFT(ipb_timestamp, 8), '%Y%m%d') AS expiry,
  0 - DATEDIFF(NOW(), STR_TO_DATE(LEFT(ipb_expiry, 8), '%Y%m%d')) AS days_left,
  DATEDIFF(NOW(), STR_TO_DATE(LEFT(ipb_timestamp, 8), '%Y%m%d')) AS block_age
FROM ipblocks
WHERE
  ipb_user = 0
  AND ipb_expiry NOT IN (
    'infinity',
    'indefinite'
  )
  AND DATEDIFF(NOW(), STR_TO_DATE(LEFT(ipb_expiry, 8), '%Y%m%d')) > -30
  AND DATEDIFF(NOW(), STR_TO_DATE(LEFT(ipb_timestamp, 8), '%Y%m%d')) > 300
  AND ipb_range_start = ipb_range_end -- exclude CIDRs
"""
        cursor.execute(query)
        results = cursor.fetchall()
        return results

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
        else:
            return '{{yes-no|}}'

    def find_proxies(self):
        out = '{| class="wikitable sortable"\n'
        out += '! آی‌پی !! بازه !! کد کشور !! ' +\
               'IPQualityScore !! proxycheck !! GetIPIntel !! ' +\
               'بسته شد'

        iplist = self.get_ip_list()
        rowtemplate = '\n|-\n| %s || %s || %s || %s || %s || %s || %s'

        for ipdata in iplist:
            ip = ipdata[0].decode('ASCII')
            print(ip)
            pywikibot.output('Checking %s' % ip)
            ipinfo = self.get_ip_info(ip)
            if ipinfo['country_code'] == 'IR':
                """
                IPs from Iran are almost never proxies, skip the checks
                """
                pass
            else:
                IPQS, PC, GII = self.run_queries(ip)
                if IPQS + PC + GII == 3:
                    target = pywikibot.User(self.site, ip)
                    pywikibot.output('Blocking %s' % ip)
                    self.site.blockuser(
                        target, '1 year', self.blocksummary,
                        anononly=False, reblock=True, allowusertalk=True)
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
                    self.format_result(blocked)
                )
                out += row

        out += '\n|}'

        page = pywikibot.Page(self.site, self.target)
        page.text = out
        page.save(self.summary)

        page = pywikibot.Page(self.site, self.target + '/امضا')
        page.text = '~~~~~'
        page.save(self.summary)


robot = FindProxyBot()
robot.find_proxies()
