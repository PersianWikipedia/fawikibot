#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of long term IP blocks on enwiki and applies them to
fawiki as well. The query aims to only capture blocks for proxy or web host IP
addresses.
"""
#
# (C) User:Mensis Mirabilis, 2019
# (C) User:Huji, 2022
#
# Distributed under the terms of the MIT License.
#
from __future__ import absolute_import

#

import pywikibot
import toolforge
from ipwhois import IPWhois
import re
from cidr_trie import PatriciaTrie


class ImportBlockBot:
    def __init__(self):
        self.site = pywikibot.Site()
        self.target = "ویکی‌پدیا:گزارش دیتابیس/درون‌ریزی بستن‌های پروکسی"
        self.summary = "روزآمدسازی نتایج (وظیفه ۲۲)"
        self.blocksummary = "{{پروکسی باز}}"
        self.IPv4cache = PatriciaTrie()
        self.IPv6cache = PatriciaTrie()

    def get_ip_list(self):
        """
        Gathers a list of IPs with a long-term block that is about to expire.
        """
        conn = toolforge.connect("enwiki")
        cursor = conn.cursor()
        query = """
SELECT
  bt_address
FROM block
join block_target
  on bl_target = bt_id
JOIN comment
  ON bl_reason_id = comment_id
WHERE
  bt_user IS NULL
  AND bt_auto = 0
  AND bl_expiry NOT IN (
    'infinity',
    'indefinite'
  )
  AND DATEDIFF(
    NOW(),
    STR_TO_DATE(LEFT(bl_timestamp, 8), '%Y%m%d')
  ) BETWEEN 8 AND 15
  AND DATEDIFF(
    STR_TO_DATE(LEFT(bl_expiry, 8), '%Y%m%d'),
    STR_TO_DATE(LEFT(bl_timestamp, 8), '%Y%m%d')
  ) > 90
  AND (
    comment_text LIKE '%webhost%'
    OR comment_text LIKE '%proxy%'
  )
"""
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def get_cache(self, ip):
        pat = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
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
        pat = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
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
                cidr = result["asn_cidr"]
                country = result["asn_country_code"]
                self.set_cache(ip, cidr, country)
            except Exception:
                cidr = ""
                country = ""
        else:
            cidr = cached_info[0][0]
            country = cached_info[0][1]

        return {"cidr": cidr, "country_code": country}

    def format_result(self, res):
        if res == 1:
            return "{{yes}}"
        elif res == 0:
            return "{{no}}"
        else:
            return "{{yes-no|}}"

    def main(self):
        out = '{| class="wikitable sortable"\n'
        out += "! آی‌پی !! بازه !! کد کشور !! بسته شد"

        iplist = self.get_ip_list()
        rowtemplate = "\n|-\n| %s || %s || %s || %s"

        for ipdata in iplist:
            ip = ipdata[0].decode("ASCII")
            pywikibot.output("Checking %s" % ip)
            ipinfo = self.get_ip_info(ip)
            if ipinfo["country_code"] == "IR":
                """
                IPs from Iran are almost never proxies, skip the checks
                """
                pass
            else:
                target = pywikibot.User(self.site, ip)
                if target.is_blocked():
                    blocked = 2
                else:
                    pywikibot.output("Blocking %s" % ip)
                    try:
                        self.site.blockuser(
                            target,
                            "1 year",
                            self.blocksummary,
                            anononly=False,
                            allowusertalk=True,
                        )
                        blocked = 1
                    except pywikibot.exceptions.APIError:
                        blocked = 2
                row = rowtemplate % (
                    ip,
                    ipinfo["cidr"],
                    ipinfo["country_code"],
                    self.format_result(blocked),
                )
                out += row

        out += "\n|}"

        page = pywikibot.Page(self.site, self.target)
        page.text = out
        page.save(self.summary)

        page = pywikibot.Page(self.site, self.target + "/امضا")
        page.text = "~~~~~"
        page.save(self.summary)


robot = ImportBlockBot()
robot.main()
