#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of long term IP blocks on metawiki and applies them
at fawiki as well. The query aims to only capture blocks for proxy or web host
IP addresses.

This script is meant to be run occasionally to address the limitation of
importglobalblocks.py in identifying blocks whose expiration date was updated
before they expired.

This version does not retreive IP WHOIS information and does not populate an
on-wiki log. This script may import thousands of blocks, therefore it may be
blocked by WHOIS servers otherwise.
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
from pywikibot.exceptions import APIError
import toolforge


class ImportBlockBot:
    def __init__(self):
        self.site = pywikibot.Site()
        self.target = "ویکی‌پدیا:گزارش دیتابیس/درون‌ریزی بستن‌های سراسری آی‌پی"
        self.summary = "روزآمدسازی نتایج (وظیفه ۲۲)"
        self.blocksummary = "{{پروکسی باز}}"

    def get_ip_list(self):
        """
        Gathers a list of IPs with a long-term block that is about to expire.
        """
        conn = toolforge.connect("metawiki")
        cursor = conn.cursor()
        query = """
SELECT
  bt_address
FROM block
JOIN block_target
  ON bl_target = bt_id
JOIN comment_block
  ON bl_reason_id = comment_id
WHERE
  bt_user IS NULL
  AND bt_auto = 0
  AND bl_sitewide = 1
  AND bl_expiry NOT IN (
    'infinity',
    'indefinite'
  )
  AND DATEDIFF(
    NOW(),
    STR_TO_DATE(LEFT(bl_timestamp, 8), '%Y%m%d')
  ) > 8
  AND DATEDIFF(
    STR_TO_DATE(LEFT(bl_expiry, 8), '%Y%m%d'),
    STR_TO_DATE(LEFT(bl_timestamp, 8), '%Y%m%d')
  ) > 90
  AND (
    comment_text LIKE '%m:NOP%'
    OR comment_text LIKE '%m:NOOP%'
    OR comment_text LIKE '%[[NOP%'
    OR comment_text LIKE '%[[NOOP%'
    OR comment_text LIKE '%Open prox%'
    OR comment_text LIKE '%Open Prox%'
    OR comment_text LIKE '%open prox%'
    OR comment_text LIKE '%Hosting%'
    OR comment_text LIKE '%hosting%'
  )
"""
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def main(self):
        iplist = self.get_ip_list()

        for ipdata in iplist:
            ip = ipdata[0].decode("ASCII")
            pywikibot.output("Checking %s" % ip)
            target = pywikibot.User(self.site, ip)
            if target.is_blocked():
                pywikibot.output("It was already blocked")
            else:
                try:
                    self.site.blockuser(
                        target,
                        "2 years",
                        self.blocksummary,
                        anononly=False,
                        allowusertalk=True,
                    )
                    pywikibot.output("Blocked it!")
                except APIError as err:
                    if err.code == "alreadyblocked":
                        pywikibot.output("Range was already blocked")
                    else:
                        pywikibot.output("Unknown error occurred:")
                        pywikibot.output(err)


robot = ImportBlockBot()
robot.main()
