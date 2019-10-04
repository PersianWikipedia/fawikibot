#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot fetches the number of watchers of talk pages for a pre-defined list
of users.

This code is and adaptation of CentijimoBot by theopolisme:
https://github.com/theopolisme/theobot/blob/master/centijimbo.py
"""
#
# (C) User:Huji, 2019
#
# Distributed under the terms of the CC-BY-SA license.
#
from __future__ import absolute_import
#

import pywikibot
import mwclient
import urllib
import MySQLdb as mysqldb


class CentiTanhaBot():

    def __init__(self):
        self.site = pywikibot.Site()
        self.summary = "به روز کردن آمار"
        self.output_page = "وپ:گزارش دیتابیس/" + \
                           "کاربران فعال ویکی‌پدیا بر پایه شاخص سانتی‌تنها"

    def process_users(self):
        user_list = self._active_users()
        if len(user_list) > 0:
            data = self._watchers(user_list)
            data = sorted(
                data.items(),
                reverse=True,
                key=lambda kv: (kv[1], kv[0])
            )
            output = '[[رده:گزارش‌های دیتابیس ویکی‌پدیا]]\n'
            output += '{{/بالا}}\n\n'
            output += 'آخرین به روز رسانی: ~~~~~\n'
            output += '{| class="wikitable sortable"\n'
            output += '! صفحه !! سانتی‌تنها\n'
            max_watchers = data[0][1]
            if max_watchers == 0:
                max_watchers = 1
            for item in data:
                if item[1] == 0:
                    continue
                ct = '{:.2f}'.format(100 * item[1] / max_watchers)
                output += '|-\n| [[' + item[0] + '|]] || ' + \
                          '{{formatnum:' + ct + '}}\n'
            output += '|}'
            page = pywikibot.Page(self.site, self.output_page)
            page.put(output, self.summary)
            page = pywikibot.Page(self.site, self.output_page + "/امضا")
            page.put("~~~~~", self.summary)

    def _active_users(self):
        conn = mysqldb.connect(
            host='fawiki.labsdb',
            db='fawiki_p',
            read_default_file='~/replica.my.cnf'
        )
        cursor = conn.cursor()
        query = """
SELECT CONCAT('User:', actor_name)
FROM revision
JOIN actor
  ON rev_actor = actor_id
LEFT JOIN user_groups
  ON actor_user = ug_user
  AND ug_group = 'bot'
WHERE
  rev_timestamp >= DATE_FORMAT(
    DATE_SUB(NOW(), INTERVAL 30 DAY),
    '%Y%m%d000000'
  )
  AND actor_user <> 0
  AND ug_user IS NULL
  AND actor_id NOT IN (
    13,
    138
  )
GROUP BY rev_actor
HAVING COUNT(*) > 5
"""
        cursor.execute(query)
        result = [item[0].decode('utf-8') for item in cursor.fetchall()]
        return result

    def _watchers(self, page_list):
        watcher_data = {}
        site = mwclient.Site('fa.wikipedia.org')
        cnt = len(page_list)

        for i in range(0, int(cnt / 50) + 1):
            start = i * 50
            end = min((i+1) * 50, cnt)
            subset = page_list[start:end]
            results = site.api(
                action='query',
                prop='info',
                inprop='watchers',
                titles='|'.join(subset)
            )
            pages = results[u'query'][u'pages']
            for page in pages:
                try:
                    watchers = pages[page][u'watchers']
                except KeyError:
                    watchers = 0
                if len(page_list) == 1:
                    return watchers
                title = pages[page][u'title']
                watcher_data[title] = watchers
        return watcher_data


robot = CentiTanhaBot()
robot.process_users()
