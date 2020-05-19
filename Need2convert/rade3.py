#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
# Distributed under the terms of MIT License (MIT)
#
# for more information see [[fa:ویکی‌پدیا:درخواست‌های ربات/رده همسنگ]] and [[fa:ویکی‌پدیا:رده‌دهی مقالات همسنگ]]
# Python 3
from pywikibot import config
from pywikibot import pagegenerators
import re
import sys
import fa_cosmetic_changes_core
import pywikibot
import codecs
import string
import time
import MySQLdb
_cache = {}
page_list_run = []
#-----------------------------------------------version-----------------------------------------
fa_site = pywikibot.Site('fa', 'wikipedia')
en_site = pywikibot.Site('en', 'wikipedia')
versionpage = pywikibot.Page(fa_site, 'کاربر:Rezabot/رده‌دهی مقالات همسنگ/نسخه')
lastversion = versionpage.get().strip()
version = '۳۰.۱'
new_edition = '۲'
if lastversion != version:
    pywikibot.output("\03{lightred}Your bot dosen't use the last verion please update me!\03{default}")
    pywikibot.stopme()
    sys.exit()
#-----------------------------------------------------------------------------------------------

def namespacefinder(enlink, site):
    if _cache.get(tuple([enlink, site, 'ns'])):
        return _cache[tuple([enlink, site, 'ns'])]
    try:
        enlink = str(enlink).replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    except:
        enlink = enlink.replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    enlink = enlink.replace(' ', '_')
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit': 500,
    }
    a = 1
    if a:
        categoryname = pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname['query']['pages']:
            fanamespace = categoryname['query']['pages'][item]['ns']
        _cache[tuple([enlink, site, 'ns'])] = fanamespace
        return fanamespace
    else:
        _cache[tuple([enlink, site, 'ns'])] = False
        return False

def englishdictionry(enlink, firstsite, secondsite):
    if _cache.get(tuple([enlink, firstsite, secondsite, 'en_dic'])):
        return _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])]
    try:
        enlink = str(enlink).replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '').replace(' ','_')
    except:
        enlink = enlink.replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '').replace(' ','_')
    if enlink.find('#') != -1:
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
        return False
    if enlink == '':
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
        return False
    result=link_translator(enlink,firstsite,secondsite)
    #print (result)
    if result:
        if str(result).find('#') != -1:
            _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
            return False
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = result
        return result
    else:
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])]=False
        return False 

def link_translator(title,ensite,fasite):

    params = {
        'action': 'query',
        'redirects': '',
        'titles': title
    }
    query_res = pywikibot.data.api.Request(site=ensite, **params).submit()


    normalizeds = query_res['query'].get('normalized', [])
    if len(normalizeds):
        title = normalizeds[0]['to']
        
    redirects = query_res['query'].get('redirects', [])
    if len(redirects):
        title = redirects[0]['to']


    wikidata = pywikibot.Site('wikidata', 'wikidata')
    
    endbName = ensite.dbName()
    fadbName = fasite.dbName()
    params = {
        'action': 'wbgetentities',
        'sites': endbName,
        'titles': title,
        'props': 'sitelinks'
    }

    try:
        query_res = pywikibot.data.api.Request(site=wikidata, **params).submit()
    except:
        return ''

    matches_titles = {}
    entities = query_res.get('entities', {})
    for qid, entity in entities.items():
        if fadbName in entity.get('sitelinks', {}):
            fa_title = entity['sitelinks'][fadbName]

            # for not updated since addition of badges on Wikidata items
            if not isinstance(title, str):
                fa_title = fa_title['title']

            return fa_title

    return ''


def catquery(enlink, firstsite, hidden):
    if _cache.get(tuple([enlink, firstsite, hidden, 'cat_query'])):
        return _cache[tuple([enlink, firstsite, hidden, 'cat_query'])]
    cats = []
    try:
        enlink = str(enlink).replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    except:
        enlink = enlink.replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    enlink = enlink.split('#')[0].strip()
    if enlink == '':
        _cache[tuple([enlink, firstsite, hidden, 'cat_query'])] = False
        return False
    enlink = enlink.replace(' ', '_')
    site = pywikibot.Site(firstsite)
    params = {
        'action': 'query',
        'prop': 'categories',
        'titles': enlink,
        'redirects': 1,
        'cllimit': 500,
    }
    if not hidden:
        params['clshow'] = '!hidden'
    try:
        categoryname = pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname['query']['pages']:
            categoryha = categoryname['query']['pages'][item]['categories']
            break
        for cat in categoryha:
            cats.append(cat['title'])
        _cache[tuple([enlink, firstsite, hidden, 'cat_query'])] = cats
        return cats
    except:
        _cache[tuple([enlink, firstsite, hidden, 'cat_query'])] = False
        return False

def templatequery(enlink, firstsite):
    if _cache.get(tuple([enlink, firstsite, 'tem_query'])):
        return _cache[tuple([enlink, firstsite, 'tem_query'])]
    temps = []
    try:
        enlink = str(enlink).replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    except:
        enlink = enlink.replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    enlink = enlink.split('#')[0].strip()
    if enlink == '':
        _cache[tuple([enlink, firstsite, 'tem_query'])] = False
        return False
    enlink = enlink.replace(' ', '_')
    site = pywikibot.Site(firstsite)
    params = {
        'action': 'query',
        'prop': 'templates',
        'titles': enlink,
        'redirects': 1,
        'tllimit': 500,
    }

    try:
        categoryname = pywikibot.data.api.Request(site, **params).submit()
        for item in categoryname['query']['pages']:
            templateha = categoryname['query']['pages'][item]['templates']
            break
        for temp in templateha:
            temps.append(temp['title'].replace('_', ' '))
        return temps
    except:
        _cache[tuple([enlink, firstsite, 'tem_query'])] = False
        return False

def subcatquery(enlink, firstsite):
    if _cache.get(tuple([enlink, firstsite, 'subcat_query'])):
        return _cache[tuple([enlink, firstsite, 'subcat_query'])]
    cats = []
    try:
        enlink = str(enlink).replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    except:
        enlink = enlink.replace('[[', '').replace(']]', '').replace('en:', '').replace('fa:', '')
    enlink = enlink.split('#')[0].strip()
    if enlink == '':
        _cache[tuple([enlink, firstsite, 'subcat_query'])] = False
        return False
    enlink = enlink.replace(' ', '_')
    site = pywikibot.Site(firstsite)
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': enlink,
        'cmtype': 'subcat',
        'cmlimit': 500,
    }
    try:
        categoryname = pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname['query']['categorymembers']:
            categoryha = item['title']
            pywikibot.output(categoryha)
            cats.append(categoryha)
        if cats != []:
            _cache[tuple([enlink, firstsite, 'subcat_query'])] = cats
            return cats
    except:
        _cache[tuple([enlink, firstsite, 'subcat_query'])] = False
        return False

def sitop(link, wiki):
    link = link.replace('[[', '').replace(']]', '').strip()
    site = pywikibot.Site(wiki)
    try:
        page = pywikibot.Page(site, link)
        if wiki == 'fa':
            cats = page.categories()
        else:
            cats = pywikibot.textlib.getCategoryLinks(page.get(), site=site)
        return cats
    except pywikibot.IsRedirectPage:
        return False
    except:
        return False

def category(PageTitle, koltuple):
    counters = 0
    PageTitle = PageTitle.replace('[[', '').replace(']]', '').strip()
    listacategory = [PageTitle]
    listacategory2 = []
    for catname in listacategory:
        counters += 1
        if counters > 150:
            break
        gencat = subcatquery(catname, 'fa')  # ---function
        if not gencat:
            time.sleep(5)
            gencat = subcatquery(catname, 'fa')
        if gencat:
            if len(gencat) > 100:
                continue
            for subcat in gencat:
                subcat2 = '[[fa:' + subcat + ']]'
                if subcat in listacategory:
                    continue
                else:
                    listacategory.append(subcat)
                    if subcat2 in koltuple:
                        listacategory2.append(subcat2)
                        listacategory2.append(' ')
                        return listacategory2
    if listacategory == []:
        return False
    else:
        return listacategory

def pagefafinder(encatTitle):

    cats = []
    try:
        item = str(encatTitle).replace('[[en:', '').replace(']]', '').replace(' ', '_').replace('Category:', '')
    except:
        item = str(encatTitle).replace('[[en:', '').replace(']]', '').replace(' ', '_').replace('Category:', '')
    # -----------------start sql---------------------------------------
    queries = 'SELECT /* SLOW_OK */ ll_title,page_namespace  FROM page JOIN categorylinks JOIN langlinks WHERE cl_to = "' + item + '" AND cl_from=page_id AND page_id =ll_from AND ll_lang = "fa" GROUP BY ll_title ;'
    cn = MySQLdb.connect("enwiki.labsdb", db=en_site.dbName()+ '_p', user=config.db_username, passwd=config.db_password)
    cur = cn.cursor()
    cur.execute(queries)
    results = cur.fetchall()
    cn.close()
    # -----------------end of sql--------------------------------------------
    for raw in results:
       raw=list(raw)
       cats.append([raw[0],raw[1]])
    if cats != []:
        return cats
    else:
        return False

def duplic(catfa, radeh):
    catfa = catfa.replace('fa:', '')
    radeht = ' '
    if len(radeh.strip()) < 1:
        return False
    if len(catfa.replace(',', '').strip()) < 1:
        return radeh
    for x in catfa.split(','):
        catfax = x.split('|')[0].split(']]')[0].replace('[[', '').strip()
        for y in radeh.split(','):
            radehy = y.split('|')[0].split(']]')[0].replace('[[', '').strip()
            if catfax == radehy:
                radeh = radeh.replace(y, '')
                break
    for rad in radeh.split(','):
        radeht += rad + '\n'
    return radeht

def pedar(catfa, radehi, link):
    link = link.replace('[[', '').replace(']]', '').strip()
    hazflist = catfa
    if englishdictionry(link, fa_site, en_site) is False:
        return hazflist
    radehi = re.sub(r'\n+?', r'\n', radehi.strip())
    kol = catfa.strip() + radehi.replace('\n', ',').strip()
    kol = kol.replace(',,', ',').strip()
    radehtest = radehi.replace('\n', ',').replace(',,', ',').strip().split(',')
    koltuple = kol.split(',')
    for x in range(0, len(radehtest)):
        if radehtest[x].find('مقاله‌های') != -1:
            continue
        catslistx = category(radehtest[x], koltuple)  # ----------category function
        if catslistx is False:
            continue
        for y in range(0, len(koltuple)):
            if radehi.find(radehtest[x]) == -1:
                break
            for catlis in catslistx:
                try:
                    catlis = str(catlis).strip()
                except:
                    catlis = catlis.strip()
                if koltuple[y].strip() == catlis:
                    if radehi.find(radehtest[x]) != -1:
                        hazfi = radehtest[x].replace('[[', '').replace(']]', '').replace(
                            'رده:', '').replace('Category:', '').strip()
                        try:
                            hazfi = re.search('\[\[ *(?:[Cc]ategory|رده) *:*%s*(?:\|.*?|)\]\]' % hazfi, radehi).group(0)
                            radehi = radehi.replace(hazfi, '')
                        except:
                            try:
                                radehi = radehi.replace('(', ' اااا ').replace(')', ' بببب ')
                                hazfi = hazfi.replace('(', ' اااا ').replace(')', ' بببب ')
                                hazfi = re.search('\[\[ *(?:[Cc]ategory|رده) *:*%s*(?:\|.*?|)\]\]' % hazfi, radehi)
                                if hazfi:
                                    hazfi= hazfi.group(0)
                                    radehi = radehi.replace(hazfi, '')
                                    radehi = radehi.replace(' اااا ', '(').replace(' بببب ', ')')
                            except:
                                pass
                        radehi = radehi.replace('\n\n', '\n').strip()
                        break
    radehi = radehi.replace(',', '\n').strip()
    return radehi

def run(gen):
    for pagework in gen:
        if True:
        #try:
            radehf, catsfas, maghalehen, radeh, finallRadeh = ' ', ' ', ' ', ' ', ' '
            try:
                pagework = str(pagework)
            except:
                pagework = pagework

            if pagework in page_list_run:
                continue
            else:
                page_list_run.append(pagework)
            try:
                pagework=pagework.title()
            except:
                pass
            pywikibot.output('-----------------------------------------------')
            pywikibot.output('opening....' + pagework)
            catsfa = sitop(pagework, 'fa')
            if catsfa is False:
                continue
            for tem in catsfa:
                #if str(tem).find('رده:مقاله‌های ایجاد شده توسط ایجادگر') != -1:
                #    continue
                cat_queries_result=catquery(str(tem), 'fa', True)
                if cat_queries_result:
                    if 'رده:رده‌های پنهان' in cat_queries_result:
                        pywikibot.output('>> Continueing the hidden category '+str(tem))
                        continue
                catsfas += str(tem) + ','
            maghalehen = englishdictionry(pagework, fa_site, en_site)
            if not maghalehen:
                continue
            pageblacklist = ['Sandbox']
            passing = True
            for item in pageblacklist:
                if maghalehen.find(item.lower()) != -1:
                    passing = False
                    break
            if not passing:
                continue
            if namespacefinder(maghalehen, en_site) != namespacefinder(pagework, fa_site):
                pywikibot.output("\03{lightred}Interwikis have'nt the same namespace\03{default}")
                continue
            catsen = catquery(maghalehen, 'en', False)
            if not catsen:
                time.sleep(5)
                catsen = catquery(maghalehen, 'en', False)
                if not catsen:
                    continue
            templateblacklist = ['Wikipedia category', 'sockpuppet', 'Empty category', 'tracking category',
                                 'container category', 'hiddencat', 'backlog subcategories', 'Stub category']
            nameblcklist = ['Current events', 'Tracking', 'articles‎', 'Surnames', 'Loanword',
                            'Words and phrases', 'Given names', 'Human names', 'stubs‎', 'stub‎', 'Nicknames']
            for cat in catsen:
                passport = True
                temples = str(templatequery(cat, 'en')).replace('_', ' ').strip()
                cat = cat.replace('_', ' ').strip()
                if namespacefinder(pagework, fa_site) != 14:
                    for black in templateblacklist:
                        if temples.lower().find(black.lower()) != -1:
                            passport = False
                            break
                for item in nameblcklist:
                    if cat.lower().find(item.lower()) != -1:
                        passport = False
                        break
                if not passport:
                    continue
                interwikifarsibase = englishdictionry(cat, en_site, fa_site)
                if interwikifarsibase:
                    if interwikifarsibase.find(',') != -1:
                        try:
                            errorpage = pywikibot.Page(fa_site, 'user:Rezabot/CategoriesWithBadNames')
                            texterror = errorpage.get()
                            if texterror.find(interwikifarsibase) == -1:
                                texterror += '\n#[[:' + interwikifarsibase + ']]'
                                errorpage.put(texterror, 'ربات:گزارش رده با نام اشتباه')
                            continue
                        except:
                            continue
                    interwikifarsi = '[[' + interwikifarsibase + ']]'
                    if cat == englishdictionry(interwikifarsibase, fa_site, en_site):
                        radeh += interwikifarsi + ','
            radehf = duplic(catsfas, radeh)
            if radehf is False:
                continue
            radehf = radehf.replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').strip()
            if radehf == "":
                continue
            if catsfas.strip() != '':
                finallRadeh = pedar(catsfas, radehf, pagework)
            else:
                finallRadeh = radehf.replace(',', '\n')
            if finallRadeh is False:
                continue
            if finallRadeh.replace('\n', '').strip() == '':
                continue
            try:
                link = pagework.replace('[[', '').replace(']]', '').strip()
                page = pywikibot.Page(fa_site, link)

                try:
                    text = page.get()
                except pywikibot.IsRedirectPage:
                    continue
                except:
                    pywikibot.output('\03{lightred}Could not open page\03{default}')
                    continue
                namespaceblacklist = [1, 2, 3, 5, 7, 8, 9, 11, 13, 15, 101, 103,118,119,446,447, 828, 829]
                if page.namespace() in namespaceblacklist:
                    continue
                if text.find('{{رده همسنگ نه}}') != -1 or text.find('{{الگو:رده همسنگ نه}}') != -1 or text.find('{{رده‌همسنگ نه}}') != -1 or text.find('{{رده بهتر') != -1:
                    pywikibot.output('\03{lightred}this page had {{رده همسنگ نه}} so it is skipped!\03{default}')
                    continue
                #---------------------------------------remove repeative category-----------------
                text = text.replace(']]‌', ']]@12@').replace('‌[[', '@34@[[')  # for solving ZWNJ+[[ or ]]+ZWNJ Bug
                for item in finallRadeh.split('\n'):
                    item2 = item.split('|')[0].replace('[[', '').replace(']]', '').strip()
                    radehbehtar = templatequery(item2, 'fa')
                    if radehbehtar:
                        if ('الگو:رده بهتر' in radehbehtar) or ('الگو:delete' in radehbehtar) or ('الگو:حذف سریع' in radehbehtar):
                            pywikibot.output(
                                '\03{lightred}Category %s had {{رده بهتر}} or  {{delete}} so it is skipped! please edit en.wiki interwiki\03{default}' % item2)
                            finallRadeh = finallRadeh.replace(item, '').replace('\n\n', '\n')
                            continue
                    textremove = text.replace('  |', '|').replace(' |', '|').replace(
                        ' |', '|').replace('|  ', '|').replace('| ', '|')
                    if textremove.find('{{رده همسنگ میلادی نه}}') != -1 or textremove.find('{{الگو:رده همسنگ میلادی نه}}') != -1:
                        if item.find('(میلادی)') != -1 or item.find('(پیش از میلاد)') != -1 or item.find('(قبل از میلاد)') != -1:
                            finallRadeh = finallRadeh.replace(item, '').replace('\n\n', '\n')
                    if textremove.find('رده:درگذشتگان') != -1:
                        if item.find('افراد زنده') != -1 or item.find('افراد_زنده') != -1:
                            finallRadeh = finallRadeh.replace(item, '').replace('\n\n', '\n')
                    if item.find('حذف_سریع') != -1 or item.find('حذف سریع') != -1:
                        finallRadeh = finallRadeh.replace(item, '').replace('\n\n', '\n')
                    if textremove.find(item2 + ']]') != -1 or textremove.find(item2 + '|') != -1:
                        finallRadeh = finallRadeh.replace(item, '').replace('\n\n', '\n')

                if finallRadeh.replace('\r', '').replace('\n', '').strip() == '':
                    continue
                finallRadeh = finallRadeh.replace('\r', '').replace('\n\n\n\n', '\n').replace('\n\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace(
                    '\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n')  # ---------------------------------------------------------------------------------
                if text.find(r'رده:') != -1 and page.namespace() != 10:
                    num = text.find('[[رده:')
                    text = text[:num] + finallRadeh + '\n' + text[num:]
                else:
                    m = re.search(r'\[\[([a-z]{2,3}|[a-z]{2,3}\-[a-z\-]{2,}|simple):.*?\]\]', text)
                    if m:
                        if m.group(0) == '[[en:Article]]':
                            try:
                                if string.count(text, '[[en:Article]] --->') == 1:
                                    finallRadeh = re.sub(r'\n+?', '\n', finallRadeh.replace('\r', '')).strip()
                                    text = text.split('[[en:Article]] --->')[0] + \
                                        '[[en:Article]] --->\n' + finallRadeh + \
                                        text.split('[[en:Article]] --->')[1]
                                else:
                                    if page.namespace() == 10:
                                        continue
                                    text += '\n' + finallRadeh
                            except:
                                if page.namespace() == 10:
                                    continue
                                text += '\n' + finallRadeh
                        else:
                            num = text.find(m.group(0))
                            text = text[:num] + finallRadeh + '\n' + text[num:]
                    else:
                        if page.namespace() == 10:
                            continue
                        text += '\n' + finallRadeh
                pywikibot.output('\03{lightpurple} Added==' + finallRadeh + "\03{default}")
                radehfmsg = finallRadeh.strip().replace('\n', '+')
                if len(radehfmsg.split('+')) > 4:
                    numadd = str(len(radehfmsg.split('+'))).replace('0', '۰').replace('1', '۱').replace('2', '۲').replace('3', '۳').replace(
                        '4', '۴').replace('5', '۵').replace('6', '۶').replace('7', '۷').replace('8', '۸').replace('9', '۹')
                    radehfmsg = ' %s رده' % numadd
                msg = 'ربات [[وپ:رده همسنگ#' + version + '|ردهٔ همسنگ (' + version + ')]] %s: + %s'
                text_new = text
                if page.namespace() == 0:  # ----------------cleaning
                    text_new, cleaning_version, msg_clean = fa_cosmetic_changes_core.fa_cosmetic_changes(text, page)
                else:
                    msg_clean = ' '
                msg = msg % (msg_clean, radehfmsg)
                msg = msg.replace('  ', ' ').strip()
                text_new = text_new.replace(']]@12@', ']]‌').replace('@34@[[', '‌[[')
                page.put(text_new.strip(), msg)

                pywikibot.output('\03{lightpurple} Done=' + pagework + "\03{default}")
            except Exception as e:
                 pywikibot.output('\03{lightred}Could not open page\03{default}')
                 continue
        #except:
        #    pywikibot.output('\03{lightred}Bot has error\03{default}')
        #    continue
# -------------------------------encat part-----------------------------------

def categorydown(listacategory):
    listacategory = [listacategory]
    count = 1
    for catname in listacategory:
        count += 1
        if count == 200:
            break
        gencat = pagegenerators.SubCategoriesPageGenerator(catname, recurse=False)
        for subcat in gencat:
            try:
                pywikibot.output(str(subcat))
            except:
                pywikibot.output(subcat)
            if subcat in listacategory:
                continue
            else:
                listacategory.append(subcat)
        break
    return listacategory

def encatlist(encat):
    count = 0
    listenpageTitle = []
    encat = encat.replace('[[', '').replace(']]', '').replace('Category:', '').replace('category:', '').strip()
    language = 'en'
    encat = pywikibot.Category(pywikibot.Site(language), encat)
    listacategory = [encat]
    for enpageTitle in listacategory:
        try:
            fapages = pagefafinder(enpageTitle)
            if fapages is not False:
                for pages,profix_fa in fapages:
                    if  profix_fa=='14':
                        pages = 'Category:'+pages
                    elif  profix_fa=='12':
                        pages = 'Help:'+pages
                    elif  profix_fa=='10':
                        pages = 'Template:'+pages
                    elif  profix_fa=='6':
                        pages = 'File:'+pages
                    elif  profix_fa=='4':
                        pages = 'Wikipedia:'+pages
                    elif  profix_fa=='100':
                        pages = 'Portal:'+pages
                    elif profix_fa in ['1', '2', '3', '5', '7', '8', '9', '11', '13', '15', '101', '103','118','119','446','447', '828', '829']:
                        continue
                    else:
                        pages = pages
                    pywikibot.output('\03{lightgreen}Adding ' + pages + ' to fapage lists\03{default}')
                    listenpageTitle.append(pages)

        except:

            try:
                enpageTitle = str(enpageTitle).split('|')[0].split(']]')[0].replace('[[', '').strip()
            except:
                enpageTitle = enpageTitle.split('|')[0].split(']]')[0].replace('[[', '').strip()
            cat = pywikibot.Category(pywikibot.Site(language), enpageTitle)
            gent = pagegenerators.CategorizedPageGenerator(cat)
            for pagework in gent:
                count += 1
                try:
                    link = str(pagework).split('|')[0].split(']]')[0].replace('[[', '').strip()
                except:
                    pagework = str(pagework)
                    link = pagework.split('|')[0].split(']]')[0].replace('[[', '').strip()
                pywikibot.output(link)
                fapagetitle = englishdictionry(link, en_site, fa_site)
                if fapagetitle is False:
                    continue
                else:
                    pywikibot.output('\03{lightgreen}Adding ' + fapagetitle + ' to fapage lists\03{default}')
                    listenpageTitle.append(fapagetitle)

    if listenpageTitle == []:
        return False, False
    return listenpageTitle, listacategory
#-------------------------------------------------------------------encat part finish--------------------------

def main():
    summary_commandline, gen, template = None, None, None
    namespaces, PageTitles, exceptions = [], [], []
    encat, newcatfile = '', ''
    autoText, autoTitle = False, False
    recentcat, newcat = False, False
    genFactory = pagegenerators.GeneratorFactory()
    for arg in pywikibot.handleArgs():
        if arg == '-autotitle':
            autoTitle = True
        elif arg == '-autotext':
            autoText = True
        elif arg.startswith('-page'):
            if len(arg) == 5:
                PageTitles.append(pywikibot.input('Which page do you want to chage?'))
            else:
                PageTitles.append(arg[6:])
            break
        elif arg.startswith('-except:'):
            exceptions.append(arg[8:])
        elif arg.startswith('-template:'):
            template = arg[10:]
        elif arg.startswith('-facat:'):
            facat = arg.replace('Category:', '').replace('category:', '').replace('رده:', '')
            encat = englishdictionry('رده:' + facat[7:], fa_site, en_site).replace('Category:', '').replace('category:', '')
            break
        elif arg.startswith('-encat:'):
            encat = arg[7:].replace('Category:', '').replace('category:', '').replace('رده:', '')
            break
        elif arg.startswith('-newcatfile:'):
            newcatfile = arg[12:]
            break
        elif arg.startswith('-recentcat'):
            arg = arg.replace(':', '')
            if len(arg) == 10:
                genfa = pagegenerators.RecentchangesPageGenerator()
            else:
                genfa = pagegenerators.RecentchangesPageGenerator(number=int(arg[10:]))
            genfa = pagegenerators.DuplicateFilterPageGenerator(genfa)
            genfa = pagegenerators.NamespaceFilterPageGenerator(genfa, [14])
            preloadingGen = pagegenerators.PreloadingGenerator(genfa, 60)
            recentcat = True
            break
        elif arg.startswith('-newcat'):
            arg = arg.replace(':', '')
            if len(arg) == 7:
                genfa = pagegenerators.NewpagesPageGenerator(step=100, namespaces=14)
            else:
                genfa = pagegenerators.NewpagesPageGenerator(step=int(arg[7:]), namespaces=14)
            preloadingGen = pagegenerators.PreloadingGenerator(genfa, 60)
            newcat = True
            break
        elif arg.startswith('-namespace:'):
            namespaces.append(int(arg[11:]))
        elif arg.startswith('-summary:'):
            pywikibot.setAction(arg[9:])
            summary_commandline = True
        else:
            generator = genFactory.handleArg(arg)
            if generator:
                gen = genFactory.getCombinedGenerator(gen)
    if encat != '':
        encatfalist, encatlists = encatlist(encat)
        if encatlists:
            for encat in encatlists:
                encat = englishdictionry(encat, en_site, fa_site)
                if encat:
                    run([encat])
        if encatfalist is not False:
            run(encatfalist)
    if PageTitles:
        pages = [pywikibot.Page(fa_site, PageTitle) for PageTitle in PageTitles]
        gen = iter(pages)
    if recentcat:
        for workpage in preloadingGen:
            workpage = workpage.title()
            cat = pywikibot.Category(fa_site, workpage)
            gent = pagegenerators.CategorizedPageGenerator(cat)
            run(gent)
        pywikibot.stopme()
        sys.exit()
    if newcat:
        for workpage in preloadingGen:
            workpage = workpage.title()
            workpage = englishdictionry(workpage, fa_site, en_site)
            if workpage is not False:
                encatfalist, encatlists = encatlist(workpage)
                if encatlists:
                    for encat in encatlists:
                        encat = englishdictionry(encat, en_site, fa_site)
                        if encat:
                            run([encat])
                if encatfalist is not False:
                    run(encatfalist)
        pywikibot.stopme()
        sys.exit()
    if newcatfile:
        text2 = codecs.open(newcatfile, 'r', 'utf8')
        text = text2.read()
        linken = re.findall(r'\[\[.*?\]\]', text, re.S)
        if linken:
            for workpage in linken:
                pywikibot.output('\03{lightblue}Working on --- Link ' + workpage + ' at th newcatfile\03{default}')
                workpage = workpage.split('|')[0].replace('[[', '').replace(']]', '').strip()
                workpage = englishdictionry(workpage, fa_site, en_site)
                if workpage is not False:
                    encatfalist,encatlists=encatlist(workpage)
                    workpage=englishdictionry(workpage,fa_site,en_site)
                    if encatlists:
                        run(encatlists)
                    if encatfalist is not False:
                        run(encatfalist)
        pywikibot.stopme()
        sys.exit()
    if not gen:
        pywikibot.stopme()
        sys.exit()
    if namespaces != []:
        gen = pagegenerators.NamespaceFilterPageGenerator(gen, namespaces)
    preloadingGen = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    run(preloadingGen)


if __name__ == '__main__':
    main()
