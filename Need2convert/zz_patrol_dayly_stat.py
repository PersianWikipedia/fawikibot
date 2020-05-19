#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2017
# Saeid (User:Saeidpourbabak), 2017
#
# Distributed under the terms of MIT License (MIT)

import wikipedia,re,query
import MySQLdb as mysqldb
import config
from operator import itemgetter
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
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

def check_user(username):
    username=username.replace(u' ',u'_')
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'editcount'    
    }
    try:
        usernamequery = query.GetData(params,wikipedia.getSite('fa'))
        if usernamequery[u'query'][u'users'][0][u'editcount']>100:
            return True
        else:
            return False
    except:
        return False

def get_query(query):
    # sql part
    site = wikipedia.getSite('fa')
    conn = mysqldb.connect("fawiki.labsdb", db = site.dbName(),
                           user = config.db_username,
                           passwd = config.db_password)
    cursor = conn.cursor()

    wikipedia.output(u'Executing query:\n%s' % query)
    query = query.encode(site.encoding())
    cursor.execute(query)
    my_list=cursor.fetchall()
    return my_list

#List_days_ago=[u'NOW() - INTERVAL 1 YEAR <rev_timestamp',u'NOW() - INTERVAL 9 MONTH <rev_timestamp',u'NOW() - INTERVAL 6 MONTH <rev_timestamp',u'NOW() - INTERVAL 3 MONTH <rev_timestamp',u'NOW() - INTERVAL 1 MONTH <rev_timestamp',u'NOW() - INTERVAL 1 DAY <rev_timestamp']
List_days_ago=[u'NOW() - INTERVAL 1 DAY <rev_timestamp']

for days_ago in List_days_ago:
    # تعداد مقالات گشت خورده
    query_patroled_pages=u'''SELECT distinct log_title
    FROM actor JOIN logging ON log_actor = actor_id LEFT JOIN user_groups ON log_actor = ug_user AND ug_group = 'bot'
    WHERE log_type ='patrol'
    AND log_action='patrol'
    AND (
      log_params LIKE '%auto";i:0;}'
      OR log_params LIKE '%0'
      )
    AND log_title IN (
      SELECT page_title
      FROM page
      WHERE page_namespace = 0
    )
    AND ug_group IS NULL
    AND NOW() - INTERVAL 1 DAY <log_timestamp
    GROUP BY log_title;'''
    query_patroled_pages=query_patroled_pages.replace(u'rev_timestamp',u'log_timestamp')
    my_list_patroled_pages =get_query(query_patroled_pages)


    # کل ویرایش انجام شده
    query_num_edit=u'''SELECT page_title
    FROM revision JOIN page ON rev_page=page_id
    JOIN actor ON rev_actor = actor_id
    WHERE actor_name NOT LIKE 'پیام_به_کاربر_جدید'
    AND actor_name NOT LIKE 'FawikiPatroller'
    AND page_namespace = 0

    AND actor_user NOT IN (
      SELECT ug_user
      FROM user_groups
      WHERE (
        ug_group = 'bot'
      )
    )
    AND '''+days_ago+u'''
    ORDER BY page_title;'''
    my_list_num_edit =get_query(query_num_edit)

    #کل مقالات ویرایش شده
    query_pages_edited=u'''SELECT DISTINCT page_title
    FROM revision JOIN page ON rev_page=page_id
    JOIN actor ON rev_actor = actor_id
    WHERE actor_name NOT LIKE 'پیام_به_کاربر_جدید'
    AND actor_name NOT LIKE 'FawikiPatroller'
    AND page_namespace = 0

    AND actor_user NOT IN (
      SELECT ug_user
      FROM user_groups
      WHERE (
        ug_group = 'bot'
      )
    )
    AND '''+days_ago+u'''
    ORDER BY page_title;'''
    my_list_pages_edited =get_query(query_pages_edited)

    # کل ویرایش کاربر تایید نشده
    query_none_autopatrolled_edited=u'''SELECT page_title
    FROM revision JOIN page ON rev_page=page_id
    JOIN actor ON rev_actor = actor_id
    WHERE actor_name NOT LIKE 'پیام_به_کاربر_جدید'
    AND actor_name NOT LIKE 'FawikiPatroller'
    AND page_namespace = 0

    AND actor_user NOT IN (
      SELECT ug_user
      FROM user_groups
      WHERE (
        ug_group = 'autopatrolled'
        OR ug_group = 'bureaucrat'
        OR ug_group = 'sysop'
        OR ug_group = 'bot'
        OR ug_group = 'eliminator'
        OR ug_group = 'patroller'
        OR ug_group = 'botadmin'
      )
    )
    AND '''+days_ago+u'''

    ORDER BY page_title;'''
    my_list_none_autopatrolled_edited =get_query(query_none_autopatrolled_edited)

    #کل مقالات کاربر تایید نشده
    query_none_autopatrolled_pages_edited=u'''SELECT DISTINCT page_title
    FROM revision JOIN page ON rev_page=page_id
    JOIN actor ON rev_actor = actor_id
    WHERE actor_name NOT LIKE 'پیام_به_کاربر_جدید'
    AND actor_name NOT LIKE 'FawikiPatroller'
    AND page_namespace = 0

    AND actor_user NOT IN (
      SELECT ug_user
      FROM user_groups
      WHERE (
        ug_group = 'autopatrolled'
        OR ug_group = 'bureaucrat'
        OR ug_group = 'sysop'
        OR ug_group = 'bot'
        OR ug_group = 'eliminator'
        OR ug_group = 'patroller'
        OR ug_group = 'botadmin'
      )
    )
    AND '''+days_ago+u'''

    ORDER BY page_title;'''
    my_list_none_autopatrolled_pages_edited =get_query(query_none_autopatrolled_pages_edited)

    # تعداد گشت‌زنی بر پایهٔ کاربر
    query_patroled_edits=u'''SELECT actor_name, COUNT(log_id) cnt
    FROM actor JOIN logging ON log_actor = actor_id LEFT JOIN user_groups ON log_actor = ug_user AND ug_group = 'bot'
    WHERE log_type ='patrol'
    AND log_action='patrol'
    AND (
      log_params LIKE '%auto";i:0;}'
      OR log_params LIKE '%0'
      )
    AND log_title IN (
      SELECT page_title
      FROM page
      WHERE page_namespace = 0
    )
    AND ug_group IS NULL
    AND NOW() - INTERVAL 1 DAY <log_timestamp
    GROUP BY actor_name
    ORDER BY cnt DESC;'''
    query_patroled_edits=query_patroled_edits.replace(u'rev_timestamp',u'log_timestamp')
    my_list_patroled_edits =get_query(query_patroled_edits)
    
    #ویرایش واگردانی‌شده بر پایه کاربر
    #  OR rev_comment LIKE '%_به_آخرین_تغییری_که_%'
    query_reverted_edited_by_user=u'''
    SELECT actor_name, COUNT(comment_text) cnt
    FROM revision JOIN page join comment  ON rev_page=page_id and rev_comment_id=comment_id
    JOIN actor ON rev_actor = actor_id
    WHERE page_namespace = 0
    AND (
          comment_text LIKE '%خنثی‌سازی_ویرایش%توسط%'
          OR comment_text LIKE '%ویرایش%به_وسیلهٔ_[[ویکی‌پدیا:تفاوت_سریع|تفاوت_سریع]]_خنثی_شد.%'

          OR comment_text LIKE '%آخرین_تغییر_متن_رد_شد%و_برگردانده_شد_به_نسخهٔ%'
          OR comment_text LIKE '%تغییر_آخر_متن_رد_شد%و_برگردانده_شد_به_نسخهٔ%'
          OR comment_text LIKE '%آخرین%تغییر_متن_رد_شد_و_برگردانده_شد_به_نسخهٔ%'
          OR comment_text LIKE '%_به_آخرین_تغییری_که_%'
          OR comment_text LIKE '%خنثی‌سازی%وپ:توینکل%'
          OR comment_text LIKE '%خنثی‌سازی%وپ:تل%'
          OR comment_text LIKE '%برگردانده%وپ:توینکل%'
          OR comment_text LIKE '%برگردانده%وپ:تل%'
          OR comment_text LIKE '%به_نسخهٔ%ویرایش%واگردانده_شد%وپ:توینکل%'
          OR comment_text LIKE '%به_نسخهٔ%ویرایش%واگردانده_شد%وپ:تل%'
          OR comment_text LIKE '%با_فرض_حسن_نیت%ویرایش%'
          OR comment_text LIKE '%ویرایش‌های%با_فرض_حسن_نیت%خنثی‌سازی_شد%'
          OR comment_text LIKE '%ویرایش%بحث%خنثی‌سازی_شد:%'
          OR comment_text LIKE '%ویرایش%بحث%واگردانی_شد%'
          OR comment_text LIKE '%ویرایش‌های%با_فرض_حسن_نیت%واگردانده_شد%'
          OR comment_text LIKE '%واگردانی_به_نسخهٔ%وپ:توینکل%'
          OR comment_text LIKE '%واگردانی%ویرایش%وپ:توینکل%'
          OR comment_text LIKE '%تغییرات%به_نسخهٔ%واگردانده_شد%'
          OR comment_text LIKE '%واگردانی_به_نسخهٔ%تاریخ%توسط%'

          OR comment_text LIKE '%واگردانی_ویرایش‌های%وپ:هاگ%'
          OR comment_text LIKE '%برگرداندن_ویرایش‌های%وپ:هاگ%'


          OR comment_text LIKE 'ویرایش%به_آخرین_تغییری_که%انجام_داده_بود%'
          OR comment_text LIKE '%خرابکاری%خنثی‌سازی%وپ:توینکل%'
          OR comment_text LIKE '%خرابکاری%خنثی‌سازی%وپ:تل%'
          OR comment_text LIKE '%خنثی‌سازی%به_آخرین_نسخهٔ%وپ:توینکل%'
          OR comment_text LIKE '%خنثی‌سازی%به_آخرین_نسخهٔ%وپ:تل%'
          OR comment_text LIKE '%ویرایش%خرابکارانهٔ%به_آخرین_ویرایش%'
          OR comment_text LIKE '%ویرایش%خرابکارانهٔ%بحث%واگردانی_شد%'
          OR comment_text LIKE '%خرابکاری%به_نسخهٔ%واگردانده_شد.%'
    )
    AND NOW() - INTERVAL 1 DAY <rev_timestamp group by actor_name ORDER BY cnt DESC;'''
    my_list_reverted_edited_by_user =get_query(query_reverted_edited_by_user)
    
    # ویرایش واگردانی شده
    #OR comment_text LIKE '%_به_آخرین_تغییری_که_%'
    query_reverted_edited=u'''SELECT page_title,comment_text
    FROM revision JOIN page join comment ON rev_page=page_id and rev_comment_id=comment_id
    WHERE page_namespace = 0
    AND (
          comment_text LIKE '%خنثی‌سازی_ویرایش%توسط%'
          OR comment_text LIKE '%ویرایش%به_وسیلهٔ_[[ویکی‌پدیا:تفاوت_سریع|تفاوت_سریع]]_خنثی_شد.%'

          OR comment_text LIKE '%آخرین_تغییر_متن_رد_شد%و_برگردانده_شد_به_نسخهٔ%'
          OR comment_text LIKE '%تغییر_آخر_متن_رد_شد%و_برگردانده_شد_به_نسخهٔ%'
          OR comment_text LIKE '%آخرین%تغییر_متن_رد_شد_و_برگردانده_شد_به_نسخهٔ%'
          OR comment_text LIKE '%_به_آخرین_تغییری_که_%'
          OR comment_text LIKE '%خنثی‌سازی%وپ:توینکل%'
          OR comment_text LIKE '%خنثی‌سازی%وپ:تل%'
          OR comment_text LIKE '%برگردانده%وپ:توینکل%'
          OR comment_text LIKE '%برگردانده%وپ:تل%'
          OR comment_text LIKE '%به_نسخهٔ%ویرایش%واگردانده_شد%وپ:توینکل%'
          OR comment_text LIKE '%به_نسخهٔ%ویرایش%واگردانده_شد%وپ:تل%'
          OR comment_text LIKE '%با_فرض_حسن_نیت%ویرایش%'
          OR comment_text LIKE '%ویرایش‌های%با_فرض_حسن_نیت%خنثی‌سازی_شد%'
          OR comment_text LIKE '%ویرایش%بحث%خنثی‌سازی_شد:%'
          OR comment_text LIKE '%ویرایش%بحث%واگردانی_شد%'
          OR comment_text LIKE '%ویرایش‌های%با_فرض_حسن_نیت%واگردانده_شد%'
          OR comment_text LIKE '%واگردانی_به_نسخهٔ%وپ:توینکل%'
          OR comment_text LIKE '%واگردانی%ویرایش%وپ:توینکل%'
          OR comment_text LIKE '%تغییرات%به_نسخهٔ%واگردانده_شد%'
          OR comment_text LIKE '%واگردانی_به_نسخهٔ%تاریخ%توسط%'
          
          OR comment_text LIKE '%واگردانی_ویرایش‌های%وپ:هاگ%'
          OR comment_text LIKE '%برگرداندن_ویرایش‌های%وپ:هاگ%'
          

          OR comment_text LIKE 'ویرایش%به_آخرین_تغییری_که%انجام_داده_بود%'
          OR comment_text LIKE '%خرابکاری%خنثی‌سازی%وپ:توینکل%'
          OR comment_text LIKE '%خرابکاری%خنثی‌سازی%وپ:تل%'
          OR comment_text LIKE '%خنثی‌سازی%به_آخرین_نسخهٔ%وپ:توینکل%'
          OR comment_text LIKE '%خنثی‌سازی%به_آخرین_نسخهٔ%وپ:تل%'
          OR comment_text LIKE '%ویرایش%خرابکارانهٔ%به_آخرین_ویرایش%'
          OR comment_text LIKE '%ویرایش%خرابکارانهٔ%بحث%واگردانی_شد%'
          OR comment_text LIKE '%خرابکاری%به_نسخهٔ%واگردانده_شد.%'
    )
    AND '''+days_ago+u''';'''
    my_list_reverted_edited =get_query(query_reverted_edited)
    
    patroler_users_dict={}
    for a , b in my_list_patroled_edits:
        if a:
             patroler_users_dict[unicode(a,'UTF-8')]=int(b)
    b=0
    for a,b in my_list_reverted_edited_by_user:
        if a:
            a=unicode(a,'UTF-8').replace(u'_',u' ')
            if a in patroler_users_dict:
                #wikipedia.output(patroler_users_dict[a])
                #wikipedia.output(a+u'   >   '+str(b))
                patroler_users_dict[a]=patroler_users_dict[a]+int(b)
                #wikipedia.output(a+u'   >   '+str(patroler_users_dict[a]))
            else:
                patroler_users_dict[a]=int(b)
    patroler_users_dict_list=sorted(patroler_users_dict.items(), key=itemgetter(1), reverse=True)

    #wikipedia.output(u'---------------------')
    #wikipedia.output(patroler_users_dict_list)
    savetext = u"{{سردر تغییرات اخیر/گشت‌زن‌ها"
    count=0
    patrol_actor_numbers=0
    for a in patroler_users_dict_list:
        b=a[1]
        a=a[0]
        if re.sub(ur'[a-zA-Zصثقفغعهخحجچشسیبلاتنمکگظطزرذدپوطكژ]+','',a)!=a:#نام آی‌پی در فهرست نیاید
            count+=1
            if count<11:
                try:
                    savetext = savetext + u"|" + a + u"|" + numbertopersian(b)
                except:
                    savetext = savetext + u"|" + unicode(a,'UTF-8') + u"|" + numbertopersian(b)
        patrol_actor_numbers+=b
    #wikipedia.output(savetext+u'}}')

    reverted_users=[]
    num_actor_not_ok=0
    reverted_article_list=[]
    for article,comment in my_list_reverted_edited:
        try:
            try:
                comment=unicode(comment,'UTF-8').replace(u'_',u' ')
            except:
                comment=comment.replace(u'_',u' ')
            user_n=u''
            if u'[[Special:Contributions/' in comment:
                user_n=comment.split(u'[[Special:Contributions/')[1].split(u'|')[0].strip()
            if not user_n:
                if u'[[ویژه:مشارکت‌ها/' in comment:
                    user_n=comment.split(u'[[ویژه:مشارکت‌ها/')[1].split(u'|')[0].strip()
            if user_n:
                if re.sub(ur'[a-zA-Zصثقفغعهخحجچشسیبلاتنمکگظطزرذدپوطكژ]+','',user_n)!=user_n:
                    user_n=ur'IP'
                if not user_n in reverted_users:
                    if user_n==ur'IP':
                        num_actor_not_ok+=1
                    else:
                        if not check_user(user_n):
                            num_actor_not_ok+=1
                    reverted_users.append(user_n)
        except:
            continue
        if not article in my_list_patroled_pages:
            reverted_article_list.append(article)
    for article in my_list_patroled_pages:
        if not article[0] in reverted_article_list:
            reverted_article_list.append(article[0])
    reverted_article_list = list(set(reverted_article_list))
    arti=u'\n'
    #print str(reverted_article_list)
    for i in reverted_article_list:
        arti+=u'#'+unicode(i,'UTF-8')+u'\n'
    to_save={
    u'تعداد نسخه ویرایش‌شده ':numbertopersian(len(my_list_num_edit)),
    u'تعداد مقاله ویرایش‌شده':numbertopersian(len(my_list_pages_edited)),#this
    u'تعداد نسخه توسط تاییدنشده ':numbertopersian(len(my_list_none_autopatrolled_edited)),
    u'تعداد مقاله توسط تائیدنشده ':numbertopersian(len(my_list_none_autopatrolled_pages_edited)),
    u'تعداد مقاله گشت‌خورده ':numbertopersian(len(arti.split(u'\n'))-1),
    u'تعداد نسخه‌های آسیب‌زننده ':numbertopersian(len(my_list_reverted_edited)),
    u"تعداد نسخه گشت‌خورده":numbertopersian(patrol_actor_numbers),
    u"تعداد کاربران گشت‌زن":numbertopersian(len(patroler_users_dict)),
    u"تعداد کل کاربر آسیب‌زننده":numbertopersian(len(reverted_users)),
    u"تعداد کاربر تایید نشده آسیب‌زننده":numbertopersian(num_actor_not_ok),
    u'فهرست مقاله گشت‌خورده ':arti.strip(),
    u"فهرست_گشت‌زن‌ها":savetext+u"}}"
    }
    for fapage_title in to_save:
        fapage = wikipedia.Page(wikipedia.getSite('fa'),u"الگو:نمایش وضعیت/آمار/"+fapage_title)
        fapage.put(to_save[fapage_title],u"ربات به‌روزرسانی آمار گشت‌زن‌ها ")#+days_ago.split(u'-')[1].split(u'<')[0].strip())