#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
hujibot_25 - a script that moves certain templates to the article talk page

usage:

    python pwb.py hujibot_25
"""
#
# (C) w:fa:User:Huji, 2021
#
# Distributed under the terms of the MIT license.
#


import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import NoRedirectPageBot
import re


class MoveToTalkBot(NoRedirectPageBot):

    def __init__(self, template_title):
        self.template_title = template_title
        self.site = pywikibot.Site()
        self.summary = 'انتقال الگو به صفحهٔ بحث ([[ویکی‌پدیا:' + \
            'سیاست ربات‌رانی/درخواست مجوز/HujiBot/وظیفه ۲۵|وظیفه ۲۵]])'
        self.talk_page_prefix = '{{رتب}}\n{{بصب}}\n'

    def getReferringArticles(self):
        full_template_title = 'الگو:' + self.template_title
        template_page = pywikibot.Page(self.site, full_template_title)
        return template_page.getReferences(namespaces=(0))

    def get_template_pattern(self):
        first_letter = self.template_title[0:1]
        the_rest = self.template_title[1:]
        the_rest = re.sub('( |_)', '[ _]', the_rest)
        pattern = r'\{\{\s*[%s%s]%s\s*\}\}' % (
            first_letter,
            first_letter.upper(),
            the_rest
        )
        return pattern

    def treat_page(self, page):
        pywikibot.output(page)

        page_text = page.text
        new_text = re.sub(self.get_template_pattern(), '', page_text)
        if page_text == new_text:
            pywikibot.output('No change...')
            return

        talk_page = page.toggleTalkPage()
        if talk_page.exists():
            talk_page_text = talk_page.text
            first_header = talk_page_text.find('\n==')
            if first_header >= 0:
                section_zero = talk_page_text[0:first_header]
                section_zero = section_zero.rstrip('\n')
                the_rest = talk_page_text[first_header:]
                new_talk_page_text = '%s\n{{%s}}\n%s' % (
                    section_zero,
                    self.template_title,
                    the_rest
                )
            else:
                new_talk_page_text = '%s\n{{%s}}' % (
                    talk_page_text,
                    self.template_title
                )
        else:
            new_talk_page_text = '%s{{%s}}' % (
                self.talk_page_prefix,
                self.template_title
            )

        page.text = new_text
        page.save(summary=self.summary)
        talk_page.text = new_talk_page_text
        talk_page.save(summary=self.summary)


def main():
    bot = MoveToTalkBot('عکس-نیاز')
    articles = bot.getReferringArticles()
    for article in articles:
        bot.treat_page(article)
    bot.treat_page(page)


if __name__ == '__main__':
    main()
