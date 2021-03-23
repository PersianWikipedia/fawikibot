#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot generates a table summarizing currently open GANs on fawiki
"""
#
# (C) User:Huji, 2020
#
# Distributed under the terms of the CC-BY-SA 4.0 license.
#


import pywikibot
import re
from persiantools import digits


class GANtable:
    def __init__(self):
        self.site = pywikibot.Site()
        self.summary = 'روزآمدسازی آمار'
        self.GAN = 'ویکی‌پدیا:گزیدن مقاله‌های خوب'
        self.headers = [
            'ردیف',
            'صفحه خوبیدگی',
            'نامزدکننده',
            'بررسی‌کننده',
            'تاریخ نامزدی',
            'آخرین ویرایش نامزدکننده در مقاله',
            'آخرین ویرایش در گمخ'
        ]
        self.month_names = [
            'ژانویهٔ',
            'فوریهٔ',
            'مارس',
            'آوریل',
            'مهٔ',
            'ژوئن',
            'ژوئیهٔ',
            'اوت',
            'سپتامبر',
            'اکتبر',
            'نوامبر',
            'دسامبر'
        ]

    def process_list(self):
        page = pywikibot.Page(self.site, self.GAN)
        pattern = r'(?!\n)\{\{[^}]+\}\}'
        transcludes = re.findall(pattern, page.text)
        if transcludes is not None:
            output = '{| class="wikitable sortable"\n'
            rowid = 1
            for h in self.headers:
                output += '! %s\n' % h
            for t in transcludes:
                pattern = r'(\{\{(' + self.GAN + r')?/|\}\})'
                GANpage = re.sub(pattern, '', t)
                if GANpage == 'سرصفحه':
                    continue
                output += '|-\n| %s\n' % digits.en_to_fa(str(rowid))
                output += self.process_page(GANpage)
                rowid += 1
            output += '|}'

        page = pywikibot.Page(self.site, self.GAN + '/جدول')
        page.text = output
        page.save(summary=self.summary)

    def process_page(self, GANsubpage):
        GANpage = '%s/%s' % (self.GAN, GANsubpage)
        GAN = pywikibot.Page(self.site, GANpage)
        GANfirst = list(GAN.revisions(reverse=True, total=1))[0]

        # Identify GAN subject
        pattern = r"\{\{گمخ/مقاله[^\|\}]*\|([^\}]+)\}\}"
        m = re.findall(pattern, GAN.text)
        if len(m) > 0:
            GANsubject = m[0]
        else:
            GANsubject = ''

        # Identify GAN nominator
        pattern = r"\n'''نامزدکننده:'''.*?" + \
            r"\[\[(کاربر|User):([^\|\]]+)(\|[^\]]+)*\]\]"
        m = re.findall(pattern, GAN.text)
        if len(m) > 0:
            nominator = m[0][1]
        else:
            nominator = GANfirst.user

        # Identify GAN reviewer
        pattern = r"\n'''بررسی‌کننده:'''.*?" + \
            r"\[\[(کاربر|User):([^\|\]]+)(\|[^\]]+)*\]\]"
        m = re.findall(pattern, GAN.text)
        if len(m) > 0:
            reviewer = '[[User:%s|]]' % m[0][1]
        else:
            reviewer = ''

        # Identify GAN nominator's last edit in GAN subject
        latest = ''
        if GANsubject != '':
            article = pywikibot.Page(self.site, GANsubject)
            if article.isRedirectPage():
                article = article.getRedirectTarget()
            revs = article.revisions()
            for rev in revs:
                if rev.user == nominator:
                    latest = self.format_timestamp(rev.timestamp)
                    break

        row = '| [[%s|%s]]\n' % (GANpage, GANsubpage)
        row += '| [[User:%s|]]\n' % nominator
        row += '| %s\n' % reviewer
        row += '| %s\n' % self.format_timestamp(GANfirst.timestamp)
        row += '| %s\n' % latest
        row += '| %s\n' % self.format_timestamp(GAN.latest_revision.timestamp)
        return row

    def format_timestamp(self, ts):
        output = 'data-sort-value="%s%s%s"' % (
            str(ts.year),
            ('0' + str(ts.month))[-2:],
            ('0' + str(ts.day))[-2:]
        )
        output += ' | %s %s %s' % (
            digits.en_to_fa(str(ts.day)),
            self.month_names[ts.month - 1],
            digits.en_to_fa(str(ts.year))
        )
        return output


robot = GANtable()
robot.process_list()
