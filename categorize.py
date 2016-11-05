#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bots finds the English Wikipedia counterpart of a non-English Wikipedia
page and fetches its categories. If any of those categories has a counterpart
in the origin Wikipedia, the bot then adds the page to those categories.
"""
#
# (C) User:Huji, 2016
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals
#

import pywikibot
from pywikibot import pagegenerators

from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from pywikibot.tools import issue_deprecation_warning

# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}


class CategorizeBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    # CurrentPageBot,  # Sets 'current_page'. Process it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
    NoRedirectPageBot,  # CurrentPageBot which only treats non-redirects
    AutomaticTWSummaryBot,  # Automatically defines summary; needs summary_key
):

    def __init__(self, generator, **kwargs):
        """
        Constructor.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        # call constructor of the super class
        super(CategorizeBot, self).__init__(site=True, **kwargs)

        # assign the generator to the bot
        self.generator = generator
        
        # define the edit summary
        self.summary = u'افزودن رده‌های همسنگ'
        
        # allowed namespaces
        self.allowednamespaces = [0, 4, 6, 10, 12, 14, 16]

    def treat_page(self):
        if self.current_page.site.code == 'en':
            pywikibot.output(u'\03{lightred}Cannot accept EN WP page as input!\03{default}')
            return False
        
        text = self.current_page.text
        lang = self.current_page.site.code
        
        if self.current_page.namespace() not in self.allowednamespaces:
            pywikibot.output(u'\03{lightred}Namespace not allowed!\03{default}')
            return False

        if text.find(u'{{رده همسنگ نه}}') != -1 or text.find(u'{{رده‌همسنگ نه}}') != -1:
            pywikibot.output(u'\03{lightred}Skipped!\03{default}')
            return False
            
        current_categories = []
        remote_site = pywikibot.Site('en')
        remote_title = ''
        remote_categories = []
        new_categories = []
        
        params = {
            'action': 'query',
            'prop': 'categories',
            'titles': self.current_page.title(),
            'redirects': 1,
            'cllimit': 500,
            'clshow': '!hidden'
        }

        try:
            req = pywikibot.data.api.Request(site=pywikibot.Site(lang), **params).submit()
            page_id = req[u'query'][u'pages'].keys()[0]
            for cat in req[u'query'][u'pages'][page_id][u'categories']:
                current_categories.append(cat[u'title'])
        except:
            pywikibot.output(u'\03{lightred}Unable to fetch local categories!\03{default}')
            return False
            
        params = {
            'action': 'query',
            'prop': 'langlinks',
            'titles': self.current_page.title(),
            'redirects': 1,
            'lllimit': 500,
        }
        
        try:
            req = pywikibot.data.api.Request(site=pywikibot.Site(lang), **params).submit()
            page_id = req[u'query'][u'pages'].keys()[0]
            for ll in req[u'query'][u'pages'][page_id][u'langlinks']:
                if ll[u'lang'] == u'en':
                    remote_title = ll[u'*']
        except:
            pywikibot.output(u'\03{lightred}Unable to fetch interwiki links!\03{default}')
            return False

        params = {
            'action': 'query',
            'prop': 'categories',
            'titles': remote_title,
            'redirects': 1,
            'cllimit': 500,
            'clshow': '!hidden'
        }
        try:
            req = pywikibot.data.api.Request(site=remote_site, **params).submit()
            page_id = req[u'query'][u'pages'].keys()[0]
            remote_categories = req[u'query'][u'pages'][page_id][u'categories']
        except:
            pywikibot.output(u'\03{lightred}Unable to fetch remote categories!\03{default}')
            return False

        for rc in remote_categories:
            remote_category = pywikibot.Page(remote_site, rc[u'title'])
            for ll in remote_category.langlinks():
                if ll.site.code == lang:
                    # TODO: Get the local namespace name
                    if u'رده:' + ll.title not in current_categories:
                        text += u'\n[[رده:' + ll.title + ']]'

        self.put_current(text, summary=self.summary)


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

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()

    # Parse command line arguments
    for arg in local_args:

        # Catch the pagegenerators options
        if genFactory.handleArg(arg):
            continue  # nothing to do here

        # Now pick up your own options
        arg, sep, value = arg.partition(':')
        option = arg[1:]
        if option in ('summary', 'text'):
            if not value:
                pywikibot.input('Please enter a value for ' + arg)
            options[option] = value
        # take the remaining options as booleans.
        # You will get a hint if they aren't pre-definded in your bot class
        else:
            options[option] = True

    gen = genFactory.getCombinedGenerator()
    if gen:
        # The preloading generator is responsible for downloading multiple
        # pages from the wiki simultaneously.
        gen = pagegenerators.PreloadingGenerator(gen)
        # pass generator and private options to the bot
        bot = CategorizeBot(gen, **options)
        bot.run()  # guess what it does
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False

if __name__ == '__main__':
    main()
