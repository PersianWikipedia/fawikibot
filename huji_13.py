#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Qanat Bot

This bot moves the contents of articles about non-notable Qanats to a page that
lists all Qanats for the corresponding county.

It takes one parameter, which is the name of a category for the Qanats of a
certian county.
"""
#
# (C) Pywikibot team, 2006-2016
# (C) Huji, 2016
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

#

import pywikibot
import re
import string
from pywikibot import pagegenerators

from pywikibot.tools import issue_deprecation_warning

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}


class QanatBot:

    def __init__(self, **options):
        """
        Constructor.
        """
        self.summary = u'ربات: انتقال مقاله‌های قنات به صفحهٔ قنات‌های شهرستان'
        self.category = options['cat']
        self.site = pywikibot.Site('fa')

    def run(self):
        # listPage = pywikibot.Page(self.site, u'فهرست ' + self.category)
        listPage = pywikibot.Page(self.site, u'User:Huji/test')
        listText = u''
        if listPage.exists() and not listPage.isRedirectPage():
            raise 'List page already has contents, unable to proceed!'

        pywikibot.output('Fetching category members ...')
        cat = pywikibot.Category(self.site, self.category)
        articles = set(cat.articles())
        titles = set()
        texts = {}

        pywikibot.output('Processing category members ...')
        for article in articles:
            title = article.title()
            titles.add(title)
            text = article.get()
            texts[title] = text

        titles = sorted(titles)

        for title in titles:
            blob = self.parse_article(texts[title])
            if not blob:
                pywikibot.output('Unable to process %s' % title)
                raise 'Article is not structured properly'
            listText += u'==' + title + u'==\n'
            listText += blob + u'\n\n'

        listText += u'''
==منابع==
{{یادکرد وب
|نویسنده =
|نشانی=http://www.iranhydrology.com/qanat/qanatlist.asp
|عنوان=بانک اطلاعاتی قنات‌های کشور
| ناشر = وزارت جهاد کشاورزی ایران
|تاریخ =
|تاریخ بازبینی=۴ تیر ۱۳۹۱
| پیوند بایگانی =http://www.webcitation.org/68eh0vxzx
| تاریخ بایگانی = ۴ تیر ۱۳۹۱
}}
        '''
        listText += u'[[رده:%s]]' % self.category
        pywikibot.output('Saving list page ...')
        listPage.put(listText)

        pywikibot.output('Converting individual pages to redirects ...')
        for article in articles:
            article.put('#REDIRECT [[%s]]' % listPage.title())

    def parse_article(self, text):
        pattern = '\n==[^=]+==\n'
        pieces = re.split(pattern, text)
        if len(pieces) < 4:
            return False
        else:
            out = pieces[0] + '\n' + pieces[1]
            pattern = '<ref[^.]*>[^,]*</ref>'
            out = re.sub(pattern, '', out)
            out += '\n{{-}}'
            return out


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    options = {}

    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # Parse command line arguments
    for arg in local_args:
        arg, sep, value = arg.partition(':')
        option = arg[1:]
        if option in ('cat'):
            if not value:
                pywikibot.input('Please enter a value for ' + arg)
            options[option] = value

    bot = QanatBot(**options)
    bot.run()  # guess what it does
    return True

if __name__ == '__main__':
    main()
