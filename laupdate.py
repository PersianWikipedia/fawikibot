#!/usr/bin/python
# -*- coding: utf-8 -*-
# Distributed under the terms of MIT License (MIT)
import pywikibot
import time
from pywikibot.data.api import Request
import re
site = pywikibot.Site('fa', fam='wikipedia')
print "Fetching admins list"
data = Request(site=site, action="query", list="allusers", augroup="sysop", aulimit=500).submit()
adminsac = []
adminbots = ["Dexbot"]
adminsdiac = {}
for admin in data["query"]["allusers"]:
    admin = admin["name"]
    if admin in adminbots:
        continue
    acaction = []
    dcaction = []
    actions = "block, protect, rights, delete, upload, import, renameuser".split(
        ", ")
    for adminaction in actions:
        data1 = Request(site=site, action="query", list="logevents",
                        leuser=admin, letype=adminaction).submit()
        for action in data1["query"]["logevents"]:
            times = action["timestamp"].split("T")[0].split("-")
            today = time.strftime('%Y/%m/%d').split("/")
            diff = ((int(today[0]) - int(times[0])) * 365) + (
                (int(today[1]) - int(times[1])) * 30) + (int(today[2]) - int(times[2]))
            if diff < 90:
                acaction.append(
                    action["timestamp"].split("T")[0].replace("-", ""))
            else:
                dcaction.append(
                    action["timestamp"].split("T")[0].replace("-", ""))
    thmag = {"y": int(time.strftime('%Y')), "m": int(
        time.strftime('%m')), "d": int(time.strftime('%d'))}
    if (int(thmag["m"]) - 3) <= 0:
        thmag["y"] = thmag["y"] - 1
        thmag["m"] = thmag["m"] + 9
    else:
        thmag["m"] = thmag["m"] - 3
    if thmag["m"] < 10:
        thmag["m"] = "0" + str(thmag["m"])
    if thmag["d"] < 10:
        thmag["d"] = "0" + str(thmag["d"])
    thmag1 = [str(thmag["y"]), str(thmag["m"]), str(thmag["d"])]
    data2 = Request(site=site, action="query", list="usercontribs", ucuser=admin,
                    ucnamespace=8, ucend="%sT00:00:00Z" % "-".join(thmag1)).submit()
    for actionmw in data2["query"]["usercontribs"]:
        acaction.append(actionmw["timestamp"].split("T")[0].replace("-", ""))
    if len(acaction) >= 10:
        if re.search(ur"[ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیآ]", admin[0]):
            adminsac.append(u"!!!!!!!!!!!!!!!!!!!!!!!!!!!" + admin)
        else:
            adminsac.append(admin)
    else:
        acaction.sort()
        dcaction.sort()
        if re.search(ur"[ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیآ]", admin[0]):
            admin = u"!!!!!!!!!!!!!!!!!!!!!!!!!!!" + admin
        try:
            adminsdiac[admin] = acaction[-1]
        except:
            adminsdiac[admin] = dcaction[-1]
    pywikibot.output(admin)
adminsac.sort()
activetext = u"\n{{ویکی‌پدیا:فهرست مدیران/سطرف|" + \
    u"}}\n{{ویکی‌پدیا:فهرست مدیران/سطرف|".join(adminsac) + u"}}"
deactivetext = u"\n"
activetext = activetext.replace(u"!!!!!!!!!!!!!!!!!!!!!!!!!!!", u"")
ak = adminsdiac.keys()
ak.sort()
for admin in ak:
    deactivetext = deactivetext + \
        u"{{ویکی‌پدیا:فهرست مدیران/سطرغ|" + admin + \
        u"|" + adminsdiac[admin] + u"}}\n"
deactivetext = deactivetext.replace(u"!!!!!!!!!!!!!!!!!!!!!!!!!!!", u"")
page = pywikibot.Page(site, u"ویکی‌پدیا:فهرست مدیران")
text = page.get()
pywikibot.output(deactivetext)
new_text = text.replace(text.split(u"<!-- Active -->")[1], activetext + u"\n")
new_text = new_text.replace(u"<!-- Deactive -->" + text.split(
    u"<!-- Deactive -->")[1], u"<!-- Deactive -->" + deactivetext + u"\n")
page.put(new_text, u"ربات: بروزرسانی فهرست")


