#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
image_resizer.py - a script that reduces the size of non-free images

usage:

    python pwb.py oversize_image
"""
#
# (C) w:fa:User:Huji, 2021
#
# Distributed under the terms of the MIT license.
#


import pywikibot
from pywikibot import pagegenerators
import pandas as pd
from persiantools import digits


class OversizeImageBot:

    def __init__(self):
        self.site = pywikibot.Site()
        self.cat = 'رده:محتویات غیر آزاد'
        self.out = 'User:Huji/oversize_images'
        self.detail = 'User:Huji/oversize_images/details'
        self.summary = 'روزآمدسازی آمار'
        self.df = pd.DataFrame(
            columns=['user', 'file', 'ts', 'width', 'height'],
            dtype=str)

    def short_date(self, ts):
        return '%s-%s-%s' % (
            digits.en_to_fa(str(ts.year)),
            digits.en_to_fa(('0' + str(ts.month))[-2:]),
            digits.en_to_fa(('0' + str(ts.day))[-2:])
        )

    def tally(self, title, fileinfo):
        self.df = self.df.append({
            'user': fileinfo.user,
            'file': title,
            'ts': self.short_date(fileinfo.timestamp),
            'width': digits.en_to_fa(str(fileinfo.width)),
            'height': digits.en_to_fa(str(fileinfo.height))
        }, ignore_index=True)

    def aggregate(self):
        tab = self.df[['user', 'file']].groupby('user').count(). \
            sort_values('file', ascending=False)

        wikitab = '{| class=wikitable\n'
        wikitab += '! کاربر !! شمار پرونده\n'

        for idx, row in tab.iterrows():
            wikitab += '|-\n'
            wikitab += '| [[User:' + row.name + '|]]\n'
            wikitab += '| ' + str(row['file']) + '\n'

        wikitab += '|}'

        return wikitab

    def tabulate(self):
        wikitab = '{| class=wikitable\n'
        wikitab += '! کاربر !! پرونده !! تاریخ بارگذاری !! ابعاد\n'

        for idx, row in self.df.sort_values('user').iterrows():
            wikitab += '|-\n'
            wikitab += '| [[User:' + row['user'] + '|]]\n'
            wikitab += '| [[:' + row['file'] + ']]\n'
            wikitab += '| ' + row['ts'] + '\n'
            wikitab += '| %s×%s\n' % (row['width'], row['height'])

        wikitab += '|}'

        return wikitab

    def treat(self, filepage):
        print(filepage)
        title = filepage.title()
        fi = filepage.latest_file_info
        if fi.width * fi.height > 1000000:
            self.tally(title, fi)

    def run(self):
        cat = pywikibot.Category(self.site, self.cat)
        gen = pagegenerators.CategorizedPageGenerator(cat)

        for page in pagegenerators.PreloadingGenerator(gen):
            self.treat(page)

        tab = self.aggregate()
        page = pywikibot.Page(self.site, self.out)
        page.text = tab
        page.save(summary=self.summary, minor=False, botflag=False)

        tab = self.tabulate()
        page = pywikibot.Page(self.site, self.detail)
        page.text = tab
        page.save(summary=self.summary, minor=False, botflag=False)


if __name__ == "__main__":
    bot = OversizeImageBot()
    bot.run()
