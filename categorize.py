#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bots finds the English Wikipedia counterpart of a non-English Wikipedia
page and fetches its categories. If any of those categories has a counterpart
in the origin Wikipedia, the bot then adds the page to those categories.
"""
#
# (C) User:Huji, 2021
#
# Distributed under the terms of the MIT license.
#

import pywikibot
from pywikibot import pagegenerators
import fa_cosmetic_changes_core as fccc

from pywikibot.bot import (
    SingleSiteBot,
    ExistingPageBot,
    NoRedirectPageBot,
    AutomaticTWSummaryBot,
)
from pywikibot.tools import issue_deprecation_warning

# Show help with the parameter -help.
docuReplacements = {"&params;": pagegenerators.parameterHelp}


class CategorizeBot(
    SingleSiteBot,
    ExistingPageBot,
    NoRedirectPageBot,
    AutomaticTWSummaryBot,
):
    update_options = {
        "cosmetic": False,  # Whether to run cosmetic changes script
    }

    def __init__(self, generator, **kwargs):
        """
        Constructor.

        @param generator: the page generator that determines on which pages
            to work
        @type generator: generator
        """
        super(CategorizeBot, self).__init__(site=True, **kwargs)
        self.generator = generator
        self.skip_categories = [
            "صفحه‌هایی که رده همسنگ نمی‌پذیرند",
            "صفحه‌هایی که رده همسنگ میلادی نمی‌پذیرند"
        ]
        self.summary = (
            "[[ویکی‌پدیا:رده‌دهی مقالات همسنگ|ربات]]: افزودن رده‌های همسنگ"
        )
        self.allowednamespaces = [0, 4, 6, 10, 12, 14, 16]
        self.cosmetic_changes = kwargs['cosmetic']
        self.hidden_cats = []

    def get_existing_cats(self, page):
        cats = list(page.categories())
        cat_titles = list()
        for c in cats:
            cat_titles.append(c.title(with_ns=False))
        return cat_titles

    def check_eligibility(self, candidate):
        if candidate in self.hidden_cats:
            return False
        cat = pywikibot.Page(pywikibot.Site("fa"), "رده:%s" % candidate)
        cat_cats = self.get_existing_cats(cat)
        if "رده‌های پنهان" in cat_cats:
            self.hidden_cats.append(candidate)
            return False
        return True

    def treat_page(self):
        page = self.current_page

        if page.namespace() not in self.allowednamespaces:
            pywikibot.output("Namespace not allowed!")
            return False

        langlinks = page.langlinks()
        remote_page = None

        for ll in langlinks:
            if ll.site.code == "en":
                remote_page = pywikibot.Page(ll)
                break

        if remote_page is None:
            pywikibot.output("No interwiki link to enwiki; skipped.")
            return False

        original_text = page.text

        current_categories = self.get_existing_cats(page)
        if len(set(self.skip_categories) & set(current_categories)) > 0:
            pywikibot.output("Page disallows this bot; skipped.")

        remote_categories = list(remote_page.categories())
        added_categories = list()

        for rc in remote_categories:
            candidate = None
            for ll in rc.langlinks():
                if ll.site.code == "fa":
                    candidate = ll.title
            if candidate is None:
                continue
            if candidate not in current_categories:
                if self.check_eligibility(candidate):
                    added_categories.append(candidate)

        if len(added_categories) > 0:
            text = page.text
            for ac in added_categories:
                text += "\n[[رده:%s]]" % ac

            if self.cosmetic_changes is True:
                text, ver, msg = fccc.fa_cosmetic_changes(text, page)
            self.put_current(text, summary=self.summary)


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    options = {}

    # Default value for "cosmetic" option
    options['cosmetic'] = False

    # Process global arguments to determine desired site
    local_args = pywikibot.handle_args(args)

    # Process pagegenerators arguments
    gen_factory = pagegenerators.GeneratorFactory()
    local_args = gen_factory.handle_args(local_args)

    # Parse command line arguments
    for arg in local_args:
        arg, sep, value = arg.partition(":")
        option = arg[1:]
        if option in ("summary", "text"):
            if not value:
                pywikibot.input("Please enter a value for " + arg)
            options[option] = value
        # Take the remaining options as booleans.
        else:
            options[option] = True

    gen = gen_factory.getCombinedGenerator(preload=True)
    if gen:
        bot = CategorizeBot(gen, **options)
        bot.run()
        return True
    else:
        pywikibot.bot.suggest_help(missing_generator=True)
        return False


if __name__ == "__main__":
    main()
