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
import re
import urllib


class CentiTanhaBot():

    def __init__(self):
        self.site = pywikibot.Site()
        self.summary = "به روز کردن آمار"
        self.output_page = "وپ:گزارش دیتابیس/" + \
                           "کاربران ویکی‌پدیا بر پایه شاخص سانتی‌تنها"

    def process_users(self):
        page = pywikibot.Page(self.site, self.output_page + "/فهرست")
        pattern = r"\* \[\[(کاربر:[^\]]+)\]\]"
        if re.search(pattern, page.text):
            m = re.findall(pattern, page.text)
            data = self._watchers(m)
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
            for item in data:
                ct = '{:.2f}'.format(100 * item[1] / max_watchers)
                output += '|-\n| [[' + item[0] + '|]] || ' + \
                          '{{formatnum:' + ct + '}}\n'
            output += '|}'
            page = pywikibot.Page(self.site, self.output_page)
            page.put(output, self.summary)
            page = pywikibot.Page(self.site, self.output_page + "/امضا")
            page.put("~~~~~", self.summary)

    def _watchers(self, page_list):
        site = mwclient.Site('fa.wikipedia.org')
        results = site.api(
            action='query',
            prop='info',
            inprop='watchers',
            titles='|'.join(page_list)
        )
        pages = results[u'query'][u'pages']
        watcher_data = {}
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
