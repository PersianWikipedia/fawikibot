#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot retreives a list of anonymous editors on the wiki in the
last few hours and tries to identify proxies within that list.
"""
#
# (C) User:Huji, 2020
#
# Distributed under the terms of the CC-BY-SA 4.0 license.
#


import pywikibot
import re


class ANBcounter():
    def __init__(self):
        self.site = pywikibot.Site()
        self.summary = 'روزآمدسازی آمار'
        self.last_updated = 'ویکی‌پدیا:تابلوی اعلانات مدیران/آخرین شمارش'
        self.level2pages = [
            'ویکی‌پدیا:تابلوی اعلانات مدیران/نام‌های کاربری نامناسب',
            'ویکی‌پدیا:تابلوی اعلانات مدیران/نقض ۳ برگردان',
            'ویکی‌پدیا:درخواست انتقال',
            'ویکی‌پدیا:درخواست ادغام تاریخچه',
            'ویکی‌پدیا:درخواست برای دسترسی/گشت‌زن',
            'ویکی‌پدیا:درخواست برای دسترسی/گشت خودکار',
            'ویکی‌پدیا:درخواست احیا',
            'ویکی‌پدیا:تابلوی اعلانات مدیران',
            'ویکی‌پدیا:تابلوی اعلانات دیوان‌سالاران'
        ]
        self.level3pages = [
            'ویکی‌پدیا:درخواست برای دسترسی/واگردان',
            'ویکی‌پدیا:درخواست برای دسترسی/معافیت از قطع دسترسی ' +
            'نشانی اینترنتی',
            'ویکی‌پدیا:درخواست برای دسترسی/ویرایشگر خودکار',
            'ویکی‌پدیا:درخواست برای دسترسی/ویرایشگر الگو'
        ]
        self.protection_requests = 'ویکی‌پدیا:درخواست محافظت صفحه'

    def get_sections(self, text, level=2):
        if level == 3:
            pat = '\n===[^=]+===\n'
        else:
            pat = '\n==[^=]+==\n'

        sections = re.split(pat, text)
        sections = sections[1:]
        return sections

    def count_open(self, sections):
        count = 0
        for s in sections:
            if not re.match(r'\{\{بسته', s.strip()):
                count += 1

        return count

    def update_count(self, title, count, suffix=''):
        stat_title = title + '/شمار' + suffix
        stat_page = pywikibot.Page(self.site, stat_title)
        stat_page.text = '{{subst:formatnum:' + str(count) + '}}'
        stat_page.save(summary=self.summary, minor=False, botflag=False)

    def run_each(self):
        for title in self.level2pages:
            page = pywikibot.Page(self.site, title)
            sections = self.get_sections(page.text, 2)
            count = self.count_open(sections)
            self.update_count(title, count)

        for title in self.level3pages:
            page = pywikibot.Page(self.site, title)
            sections = self.get_sections(page.text, 3)
            count = self.count_open(sections)
            self.update_count(title, count)

    def run_protection_requests(self):
        page = pywikibot.Page(self.site, self.protection_requests)
        parent = self.get_sections(page.text, 2)
        # protection requests
        sections = self.get_sections(parent[0], 3)
        count = self.count_open(sections)
        self.update_count(self.protection_requests, count)
        # unprotection requests
        sections = self.get_sections(parent[1], 3)
        count = self.count_open(sections)
        self.update_count(self.protection_requests, count, '/۲')

    def run(self):
        self.run_each()
        self.run_protection_requests()

        page = pywikibot.Page(self.site, self.last_updated)
        page.text = '~~~~~'
        page.save(summary=self.summary, minor=False, botflag=False)


robot = ANBcounter()
robot.run()
