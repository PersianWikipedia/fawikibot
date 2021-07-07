#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This bot finds templates that create red/blue links with an interwiki
link hint, and replaces them with a normal blue link whenever possible.
"""
#
# (C) User:Huji, 2021
#
# Distributed under the terms of the CC-BY-SA 4.0 license.
#


import pywikibot
import re


class iwlinkfixer:
    def __init__(self):
        self.summary = "جایگزین کردن الگوی پم با پیوند ساده"

    def process_page_text(self, page_text):
        tpl_pattern = "پیوند با میان‌ویکی|پم|پبم|[Ll]int-interwiki|[Pp]am"
        param_pattern = r"\| *([^=|]+= *)?([^|]*)"
        usage_pattern = r"\{\{( *(?:" + tpl_pattern + r") *)(.+)\}\}"

        matches = re.findall(usage_pattern, page_text)
        if matches is None:
            return False
        for m in matches:
            original = "{{%s%s}}" % (m)
            param_str = m[1]
            params = re.findall(param_pattern, param_str)

            param_counter = 1
            link_target = None
            link_title = ""
            iw_title = None
            iw_lang = "en"
            new_target = None

            for p in params:
                if p[0].strip() == "" and param_counter == 1:
                    link_target = p[1].strip()
                    param_counter += 1
                elif p[0].strip() == "" and param_counter == 2:
                    iw_title = p[1].strip()
                    param_counter += 1
                elif p[0].strip() == "fa":
                    link_target = p[1].strip()
                elif p[0].replace(" ", "") == "عنوان=":
                    link_title = p[1].strip()
                elif p[0].replace(" ", "") == "زبان=":
                    iw_lang = p[1].strip()

            if link_title != "":
                link_title = "|" + link_title

            print("Original wikitext: %s" % original)
            print("Locally links to %s" % link_target)
            print("References %s:%s" % (iw_lang, iw_title))

            p = pywikibot.Page(pywikibot.Site("fa"), link_target)
            if p.exists():
                print("Local page exists; using it to create a link")
                replacement = "[[%s%s]]" % (link_target, link_title)
                print("Replacement wikitext: %s" % replacement)
                page_text = page_text.replace(original, replacement)
                continue

            try:
                iw_site = pywikibot.Site(iw_lang)
                iw_page = pywikibot.Page(iw_site, iw_title)
                # TODO: follow redirects on the target wiki
                lang_links = iw_page.langlinks()
                for l in lang_links:
                    p = pywikibot.Page(l)
                    if p.site.lang != "fa":
                        continue
                    else:
                        new_target = p.title()
                        break

                if new_target is not None:
                    print("Using interwiki backlink to create a link")
                    replacement = "[[%s%s]]" % (new_target, link_title)
                    print("Replacement wikitext: %s" % replacement)
                    page_text = page_text.replace(original, replacement)
                    continue
                else:
                    print("No interwiki backlink found; leaving it alone")

            except pywikibot.exceptions.UnknownSiteError:
                print("Invalid lang code; skipping...")
            print("")

        return page_text

    def process_page(self, page):
        text = self.process_page_text(page.text)
        page.put(text, self.summary)

    def main(self):
        page = pywikibot.Page(pywikibot.Site("fa"), "الگو:دیانت یونان")
        self.process_page(page)


robot = iwlinkfixer()
robot.main()
