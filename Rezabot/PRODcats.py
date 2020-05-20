#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (C) w:fa:User:Reza1615, 2020
# (C) w:fa:User:Huji, 2020
# Distributed under the terms of the CC-BY-SA 3.0


import pywikibot
from persiantools import digits
from datetime import datetime


month_names = [
    "ژانویه",
    "فوریه",
    "مارس",
    "آوریل",
    "مه",
    "ژوئن",
    "ژوئیه",
    "اوت",
    "سپتامبر",
    "اکتبر",
    "نوامبر",
    "دسامبر"
]
summary = "ربات:ساخت رده حذف زمان‌دار"
content = "{{جا:الگو:شروع حذف زمان‌دار}}"

now = datetime.now()
year = digits.en_to_fa(str(now.year))
month = month_names[now.month - 1]
day = digits.en_to_fa(str(now.day))
title = 'رده:صفحه‌های حذف زمان‌دار در %s %s %s' % (day, month, year)

p = pywikibot.Page(pywikibot.getSite("fa"), title)

if not p.exists():
    p.put(content, summary)
