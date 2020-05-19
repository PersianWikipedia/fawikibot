#!/usr/bin/python
# -*- coding: utf-8 -*-
import wikipedia, re
import pagegenerators
import MySQLdb as mysqldb
import config
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
def templatequery(enlink,firstsite):
    temps=[]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    if enlink==u'':
        return False    
    enlink=enlink.replace(u' ',u'_')
    site = wikipedia.getSite(firstsite)
    params = {
            'action': 'query',
            'prop':'templates',
            'titles': enlink,
            'redirects': 1,
            'tllimit':500,
    }

    try:
        categoryname = query.GetData(params,site, encodeTitle = True)
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'])         
        return temps
    except: 
        return False

#--------------------black list--------------------------------
lists = [u'infoboxes',u'CS1',u'Certification_Table_Entry',u'pages',u'Populated',u'populated',u'All',u'Wikidata',u'wikidata',u'redirects',u'Singlechart',u'centric',u'tracking',u'Pages',u'centric',u'needing',u'incorrect',u'contain',u'Article',u'tracking',u'missing',u'article', u'Wikipedia',u'April',u'May',u'November',u'October',u'December',u'August',u'February',u'June',u'July',u'September',u'January',u'March',u'Use_dmy_dates', u'Use_mdy_dates',u'WikiProject',u'template',u'Infobox',u'sandbox',u'Drugbox',u'stubs',u'Navigational_box']
#--------------------black list--------------------------------

def numbertopersian(a):
    a=str(a)
    a = a.replace(u'0', u'۰')
    a = a.replace(u'1', u'۱')
    a = a.replace(u'2', u'۲')
    a = a.replace(u'3', u'۳')
    a = a.replace(u'4', u'۴')
    a = a.replace(u'5', u'۵')
    a = a.replace(u'6', u'۶')
    a = a.replace(u'7', u'۷')
    a = a.replace(u'8', u'۸')
    a = a.replace(u'9', u'۹')
    a = a.replace(u'.', u'٫')
    return a
    
todayup=u"'''به‌روز شده توسط ربات در تاریخ''''': ~~~~~''\n\n"
savetext = todayup+u'{| class="wikitable sortable"\n'
savetext = savetext + u'! ردیف !! رده‌های ساخته نشده !! تعداد مقالات' + u'\n|-'

# ------------------------------------------------------------------sql part-----------------------------
site  = wikipedia.getSite("en")
querys = u'''
SELECT /* SLOW_OK */ cl_to, count(cl_to)
FROM categorylinks
WHERE 
    cl_from IN
        (SELECT ll_from
        FROM langlinks
        WHERE ll_lang = "fa")
    AND
    cl_to NOT IN
        (SELECT page_title 
        FROM langlinks JOIN page
            ON page_id = ll_from        
        WHERE ll_lang = "fa"
            AND page_namespace = 14)
GROUP BY cl_to
ORDER BY count(cl_to) DESC
LIMIT 2000;
'''

wikipedia.output(querys)

conn = mysqldb.connect("enwiki.labsdb", db = site.dbName(),
                       user = config.db_username,
                       passwd = config.db_password)                                
cursor = conn.cursor()
wikipedia.output(u'Executing query:\n%s' % querys)
querys = querys.encode(site.encoding())
cursor.execute(querys)
results = cursor.fetchall()
counter = 0
templateblacklist=[u'loanword',u'Wikipedia category',u'wikipedia category',u'sockpuppet',u'Empty category',u'tracking category',u'container category',u'hiddencat',u'backlog subcategories',u'Stub category']
           
for row in results:
    titleOfCategory = unicode(str(row[0]), 'UTF-8')
    usageOfCategory = unicode(str(row[1]), 'UTF-8')
    if counter >= 1000:
        break
    if titleOfCategory:
        entranc = True 
        for black in lists:
            try:
                black = str(black)
            except:
                pass
            if titleOfCategory.find(black)!=-1:
                    wikipedia.output(u'the not cat=='+titleOfCategory)    
                    wikipedia.output(u'the key=='+black)
                    entranc = False
                    break
        temples=str(templatequery(titleOfCategory,'en')).replace( u'_',u' ' ).strip()
        temples=temples.replace( u'_',u' ' ).strip()
        passport=True   
        for black in templateblacklist:
                if temples.lower().find(black.lower())!=-1:    
                       passport=False
                       break
        if not passport:    
            continue
        if entranc == True:
                 counter += 1
                 titleOfCategory = titleOfCategory.replace(u"_", u" ")
                 savetext = savetext + u"\n| " + numbertopersian(counter) + u" || [[:en:Category:" + titleOfCategory + u"|" + titleOfCategory + u"]] || {{subst:formatnum:" + usageOfCategory + u"}}\n|-"
                
savetext = savetext + u"\n|}"
#----------------------------------------------------------------- pywikipedia part
wikipedia.output(savetext)
site = wikipedia.getSite('fa')
page = wikipedia.Page(site, u"ویکی‌پدیا:گزارش دیتابیس/رده‌های مهم ایجادنشده بر پایه تعداد مقاله/فهرست")
page.put(savetext, u"ربات: به روز رسانی")

page = wikipedia.Page(site, u"ویکی‌پدیا:گزارش دیتابیس/رده‌های مهم ایجادنشده بر پایه تعداد مقاله/امضا")
page.put(u'~~~~~', u"ربات: به روز رسانی")
