#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Solar Eclipse Bot

This bot finds all pages created for non-notable solar eclipses and turns them
into a redirect. It also updates their item on Wikidata.
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

from pywikibot.bot import (
    SingleSiteBot, ExistingPageBot, NoRedirectPageBot, AutomaticTWSummaryBot)
from pywikibot.tools import issue_deprecation_warning

docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}


class EclipseBot(
    # Refer pywikobot.bot for generic bot classes
    SingleSiteBot,  # A bot only working on one site
    # CurrentPageBot,  # Sets 'current_page'. Processes it in treat_page method.
    #                  # Not needed here because we have subclasses
    ExistingPageBot,  # CurrentPageBot which only treats existing pages
    NoRedirectPageBot,  # CurrentPageBot which only treats non-redirects
):

    def __init__(self, generator, **kwargs):
        self.availableOptions.update({
            'summary': u'ربات: تبدیل صفحه‌های ناسرشناس به تغییرمسیر ([[ویکی‌پدیا:سیاست ربات‌رانی/درخواست مجوز/HujiBot/وظیفه ۱۴|وظیفه ۱۴]])',
        })

        # Call constructor of the super class
        super(EclipseBot, self).__init__(site=True, **kwargs)

        # Handle old -dry paramter
        self._handle_dry_param(**kwargs)

        # Assign the generator to the bot
        self.generator = generator

        # Save edits without asking
        self.options['always'] = True

    def _handle_dry_param(self, **kwargs):
        if 'dry' in kwargs:
            issue_deprecation_warning('dry argument',
                                      'pywikibot.config.simulate', 1)
            # use simulate variable instead
            pywikibot.config.simulate = True
            pywikibot.output('config.simulate was set to True')

    def treat_page(self):
        text = self.current_page.text
        ListPattern = r'\* \[\[(فهرست خورشیدگرفتگی‌های قرن .+ میلادی|فهرست خورشیدگرفتگی‌های قرن .+ پیش از میلاد|فهرست خورشیدگرفتگی‌های دوران باستان)\]\]'

        hasListPattern = re.search(ListPattern, text)
        if hasListPattern:
            newText = u'#تغییرمسیر [[%s]]' % hasListPattern.group(1)
            print newText
            self.put_current(newText, summary=self.getOption('summary'))

            item = pywikibot.ItemPage.fromPage(self.current_page)
            item.removeSitelink(site='fawiki', summary=u'Remove sitelink')


def main(*args):
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
        # Take the remaining options as booleans.
        # You will get a hint if they aren't pre-definded in your bot class
        else:
            pywikibot.output('Unknown argument(s)!')

    gen = genFactory.getCombinedGenerator()
    if gen:
        # The preloading generator is responsible for downloading multiple
        # pages from the wiki simultaneously.
        gen = pagegenerators.PreloadingGenerator(gen)
        # pass generator and private options to the bot
        bot = EclipseBot(gen, **options)
        bot.run()  # guess what it does
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False

if __name__ == '__main__':
    main()
