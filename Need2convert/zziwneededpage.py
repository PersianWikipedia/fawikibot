# -*- coding: utf-8 -*-
import wikipedia, re
import pagegenerators
import MySQLdb as mysqldb
import config

faSite = wikipedia.getSite('fa')
enSite=wikipedia.getSite('en')

def numbertopersian(a):
    a = str(a)
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

def data2fa(number, strict=False):
    data=wikipedia.DataPage(int(number))
    try:
        items=data.get()
    except:
        return ""
    if isinstance(items['links'],list):
        items['links']={}
    if items['links'].has_key('fawiki'):
        return items['links']['fawiki']['name']
    if strict:
        return ""
    if items['label'].has_key('fa'):
        return items['label']['fa']
    try:
        return items['label']['en']
    except:
        return ""

def ClaimFinder(our_Site,page_title,claim_num,more):
    fa_result=False
    fa_result_more=[]
    en_wdata=wikipedia.DataPage(wikipedia.Page(our_Site,page_title))
    try:
        items=en_wdata.get()
    except:
        return u' '
    if items['claims']:
        case=items['claims']
        for i in case:
            if i['m'][1]==claim_num:
                fa_result=data2fa(i[u'm'][3][u'numeric-id'])
                fa_result_more.append(fa_result)
    if fa_result_more:
        fa_result=u' '
        lenth=len(fa_result_more)-1
        if lenth>0:
            for i in fa_result_more:
                if i==fa_result_more[lenth]:
                   join=u' و '
                else:
                   join=u'، '
                fa_result+=join+i
            fa_result=fa_result[2:]
        else:
            fa_result=fa_result_more[0]
    if fa_result:
        wikipedia.output(u'\03{lightgreen}All Claims '+str(claim_num)+u' ='+fa_result+u'\03{default}')
        fa_result=fa_result.strip()
    return fa_result

    
    
savetext = u"{{ویکی‌پدیا:مقاله‌های مهم ایجادنشده/فهرست/بالا}}\n"+u"آخرین به روز رسانی: ~~~~~"+u"\n{| class=\"wikitable sortable\"\n! نام !! تعداد{{سخ}}میان‌ویکی‌ها"  + u" !! موضوع مقاله"

# sql part
query="Select /* SLOW_OK */ page_title AS title, cid From (Select ll_from As page_id, count(ll_lang) As cid From langlinks Group By ll_from Having count(ll_lang)>=35 And max(ll_lang='fa')=0) As sq Natural Join page Where page_is_redirect = 0 and page_namespace=0 Order By cid DESC,page_title;"
conn = mysqldb.connect('enwiki.labsdb', db = enSite.dbName(),
                       user = config.db_username,
                       passwd = config.db_password)
cursor = conn.cursor()

wikipedia.output(u'Executing query:\n%s' % query)
query = query.encode(enSite.encoding())
cursor.execute(query)

while True:
    try:
        pageTitle, pagelinkCount = cursor.fetchone()
        print pageTitle, pagelinkCount
    except TypeError:
        # Limit reached or no more results
        break
    if pageTitle:
        pageTitle = unicode(pageTitle, enSite.encoding())
        pageTitle = re.sub(ur"_",u" ",pageTitle)
        pageTitle = re.sub(ur"(^\"|\"$)",u"",pageTitle)
        pageTitle = re.sub(ur"(^\s*|\s$)",u"",pageTitle)
        if pageTitle != u"":
            type=False
            try:
                savetext = savetext + u"\n|-\n| [[:en:" + pageTitle + u"|]] || " + numbertopersian(pagelinkCount) + u" || " + ClaimFinder(enSite,pageTitle,31,True)
            except:
                savetext = savetext + u"\n|-\n| [[:en:" + pageTitle + u"|]] || " + numbertopersian(pagelinkCount) + u" || "
        
# pywikipedia part
savetext = savetext + "\n|}"
wikipedia.output(savetext)

page = wikipedia.Page(faSite,u"ویکی‌پدیا:گزارش دیتابیس/مقاله‌های مهم ایجادنشده")
page.put(savetext,u"ربات: به روز رسانی")


sign_page=u'ویکی‌پدیا:گزارش دیتابیس/مقاله‌های مهم ایجادنشده/امضا'
madak=u'~~~~~'
sign_page=wikipedia.Page(faSite,sign_page)
sign_page.put(madak,u'ربات:تاریخ بروز رسانی')
