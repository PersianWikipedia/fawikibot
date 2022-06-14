#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of anonymous editors on the wiki in the
last few hours and tries to identify proxies within that list.

"""
#
# (C) User:Huji, 2020
#
# Distributed under the terms of the CC-BY-SA license.
#
from __future__ import absolute_import

#

import pywikibot
import re
import toolforge
from ipwhois import IPWhois
from cidr_trie import PatriciaTrie


class FindRangesBot:
    def __init__(self):
        self.site = pywikibot.Site()
        self.target = "ویکی‌پدیا:گزارش دیتابیس/کشف پروکسی/بازه"
        self.summary = "روزآمدسازی نتایج (وظیفه ۲۲)"
        self.IPv4cache = PatriciaTrie()
        self.IPv6cache = PatriciaTrie()
        self.success = {}
        self.failure = []
        self.whois_reqs = 0
        self.block_link = (
            "//fa.wikipedia.org/wiki/Special:Block?wpExpiry="
            + "1%20year&wpReason={{پروکسی%20باز}}&wpDisableUTEdit=1"
            + "&wpHardBlock=1&wpTarget="
        )
        self.sql = """
SELECT
  ipb_address AS IP,
  ipb_range_start AS HEX
FROM ipblocks
WHERE ipb_by_actor = 1789 -- HujiBot
AND ipb_range_start = ipb_range_end
ORDER BY ipb_range_start
"""

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

    def set_cache(self, ip, cidr, cases):
        pat = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        if re.match(pat, ip) is None:
            self.IPv6cache.insert(cidr, cases)
        else:
            self.IPv4cache.insert(cidr, cases)

    def update_cache(self, ip):
        cached_info = self.get_cache(ip)

        if len(cached_info) == 0:
            try:
                self.whois_reqs += 1
                print("WHOIS query #%d" % self.whois_reqs)
                request = IPWhois(ip)
                result = request.lookup_rdap(depth=1)
                cidr = result["asn_cidr"]
                cases = [ip]
                self.set_cache(ip, cidr, cases)
            except Exception:
                self.failure.append(ip)
                cidr = None
                cases = None
        else:
            cidr = cached_info[0][0]
            cases = cached_info[0][1]
            cases.append(ip)
            self.set_cache(ip, cidr, cases)

        return {"cidr": cidr, "cases": cases}

    def get_ip_list(self, max_number, max_hours):
        conn = toolforge.connect("fawiki")
        cursor = conn.cursor()
        cursor.execute(self.sql)
        results = cursor.fetchall()

        return results

    def purge_ip_list(self, iplist):
        purged_iplist = []
        for idx in range(len(iplist)):
            item = iplist[idx]

            if idx > 0:
                prv = iplist[idx - 1]
                if prv[1].decode("utf-8")[0:2] == "v6":
                    prv = None
                else:
                    prv = int("0x" + prv[1].decode("utf-8"), 16)

            else:
                prv = None

            if idx < len(iplist) - 1:
                nxt = iplist[idx + 1]
                if nxt[1].decode("utf-8")[0:2] == "v6":
                    nxt = None
                else:
                    nxt = int("0x" + nxt[1].decode("utf-8"), 16)
            else:
                nxt = None

            """
            For now we keep all IPv6's
            As for IPv4's, we will only keep them if they are not far from
            the one before or the one after
            """
            if item[1].decode("utf-8")[0:2] == "v6":
                ip = item[0].decode("utf-8")
                purged_iplist.append(ip)
            else:
                ip = item[0].decode("utf-8")
                cur = int("0x" + item[1].decode("utf-8"), 16)
                if prv is not None and cur - prv < 65536:
                    purged_iplist.append(ip)
                elif nxt is not None and nxt - cur < 65536:
                    purged_iplist.append(ip)

        return purged_iplist

    def find_ranges(self):
        iplist = self.get_ip_list(1000, 24)
        iplist = self.purge_ip_list(iplist)

        for ip in iplist:
            pywikibot.output("Checking %s" % ip)
            ipinfo = self.update_cache(ip)
            if ipinfo["cidr"] is not None:
                self.success[ipinfo["cidr"]] = ipinfo["cases"]

        print("Generating output for wiki ...")

        out = "== بازه‌های حاوی پروکسی =="
        out += "\n{| class='wikitable sortable'"
        out += "\n! بازه !! تعداد پروکسی !! فهرست !! بسته"

        for k, v in self.success.items():
            out += "\n|-"
            out += "\n| "
            out += "[[ویژه:مشارکت‌ها/%s|%s]] " % (k, k)
            out += " ([" + self.block_link + k + " بستن])"
            out += "\n| {{formatnum:" + str(len(v)) + "}}"
            out += "\n|"
            for i in v:
                out += "\n* [[ویژه:مشارکت‌ها/%s|%s]]" % (i, i)
            out += "\n|"
            target = pywikibot.User(self.site, k)
            if target.isBlocked():
                out += "{{yes}}"
            else:
                out += "{{no}}"

        out += "\n|}"

        if len(self.failure) > 0:
            out += "\n== تلاش‌های ناموفق =="
            out += "\nربات از دریافت اطلاعات این موارد عاجز بود:"
            for i in self.failure:
                out += "\n* [[ویژه:مشارکت‌ها/%s|%s]]" % (i, i)

        page = pywikibot.Page(self.site, self.target)
        page.text = out
        page.save(self.summary)


robot = FindRangesBot()
robot.find_ranges()
