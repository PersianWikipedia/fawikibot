#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot generates a table summarizing currently open FACs on fawiki
"""
#
# (C) User:Huji, 2021
#
# Distributed under the terms of the CC-BY-SA 4.0 license.
#


import pywikibot
import re
from persiantools import digits


class FACtable:
    def __init__(self):
        self.site = pywikibot.Site()
        self.summary = 'روزآمدسازی آمار'
        self.FAC = 'ویکی‌پدیا:گزیدن مقاله‌های برگزیده'
        self.headers = [
            'ردیف',
            'صفحه برگزیدگی',
            'نامزدکننده',
            'بررسی‌کننده',
            'تاریخ نامزدی',
            'آخرین ویرایش نامزدکننده در مقاله',
            'آخرین ویرایش در گمب'
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
        page = pywikibot.Page(self.site, self.FAC)
        pattern = r'(?!\n)\{\{[^}]+\}\}'
        transcludes = re.findall(pattern, page.text)
        if transcludes is not None:
            output = '{| class="wikitable sortable"\n'
            rowid = 1
            for h in self.headers:
                output += '! %s\n' % h
            for t in transcludes:
                pattern = r'(\{\{(' + self.FAC + r')?/|\}\})'
                FACpage = re.sub(pattern, '', t)
                if FACpage == 'سرصفحه':
                    continue
                output += '|-\n| %s\n' % digits.en_to_fa(str(rowid))
                output += self.process_page(FACpage)
                rowid += 1
            output += '|}'

        page = pywikibot.Page(self.site, self.FAC + '/جدول')
        page.text = output
        page.save(summary=self.summary)

    def process_page(self, FACsubpage):
        FACpage = '%s/%s' % (self.FAC, FACsubpage)
        FAC = pywikibot.Page(self.site, FACpage)
        FACfirst = list(FAC.revisions(reverse=True, total=1))[0]

        # Identify FAC subject
        pattern = r"\{\{گمب/مقاله[^\|\}]*\|([^\}]+)\}\}"
        m = re.findall(pattern, FAC.text)
        if len(m) > 0:
            FACsubject = m[0]
        else:
            FACsubject = ''

        # Identify FAC nominator
        pattern = r"\n'''نامزدکننده:'''.*?" + \
            r"\[\[(کاربر|User):([^\|\]]+)(\|[^\]]+)*\]\]"
        m = re.findall(pattern, FAC.text)
        if len(m) > 0:
            nominator = m[0][1]
        else:
            nominator = FACfirst.user

        # Identify FAC reviewer
        pattern = r"\n'''بررسی‌کننده:'''.*?" + \
            r"\[\[(کاربر|User):([^\|\]]+)(\|[^\]]+)*\]\]"
        m = re.findall(pattern, FAC.text)
        if len(m) > 0:
            reviewer = '[[User:%s|]]' % m[0][1]
        else:
            reviewer = ''

        # Identify FAC nominator's last edit in FAC subject
        latest = ''
        if FACsubject != '':
            article = pywikibot.Page(self.site, FACsubject)
            if article.isRedirectPage():
                article = article.getRedirectTarget()
            revs = article.revisions()
            for rev in revs:
                if rev.user == nominator:
                    latest = self.format_timestamp(rev.timestamp)
                    break

        row = '| [[%s|%s]]\n' % (FACpage, FACsubpage)
        row += '| [[User:%s|]]\n' % nominator
        row += '| %s\n' % reviewer
        row += '| %s\n' % self.format_timestamp(FACfirst.timestamp)
        row += '| %s\n' % latest
        row += '| %s\n' % self.format_timestamp(FAC.latest_revision.timestamp)
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


robot = FACtable()
robot.process_list()
