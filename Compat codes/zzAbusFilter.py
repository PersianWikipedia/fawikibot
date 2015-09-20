#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2014
#
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import query,wikipedia,login,string
import pagegenerators,time,config
from datetime import timedelta,datetime
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
BotVersion=u'۲.۱'
faSite=wikipedia.getSite('fa')

def login_fa():    
    try:
        password_wiki = open("/home/reza/compat/passfile", 'r')
    except:
        password_wiki = open(wikipedia.config.datafilepath(config.password_file), 'r')
    password_wiki=password_wiki.read().replace('"','').strip()    
    passwords=password_wiki.split(',')[1].split(')')[0].strip()
    usernames=password_wiki.split('(')[1].split(',')[0].strip()
    botlog=login.LoginManager(password=passwords,username=usernames,site=faSite)
    botlog.login()

def En2Fa(a):
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

def check_user_rights(username):
    username=username.replace(u' ',u'_').replace(u'کاربر:',u'').replace(u'user:',u'').replace(u'User:',u'')
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'rights'    
    }
    try:
        usernamequery = query.GetData(params,faSite)
        user_rights=usernamequery[u'query'][u'users'][0][u'rights']
        return user_rights
    except:
        return []

def Query_Abus(pasttime,abusnum):
    #http://en.wikipedia.org/w/api.php?action=query&list=abuselog&aflprop=details|ids&format=json&afllimit=1000
    params = {
        'action': 'query',
        'list': 'abuselog',
        'aflprop': 'details|ids',
        'format':'json',
        'afllimit': 1000,
        'aflend':pasttime
    }
    abus_dict={} 
    abuslog = query.GetData(params,faSite)
    for item in abuslog[u'query'][u'abuselog']:
        abus_id=item['filter_id']
        log_id=str(item['id'])
        item=item['details']
        if abus_id==str(abusnum):#abus number
            #wikipedia.output(u'-----------------------------------------')
            #wikipedia.output(str(item))
            user_editcount=item["user_editcount"]
            if not user_editcount.strip():
                user_editcount=0
            else:
                user_editcount=int(user_editcount)
            user_name=item["user_name"].replace(u'\r',u'')
            user_age=1000#int(item["user_age"])
            user_groups=item["user_groups"]
            user_mobile=item["user_mobile"]
            article_articleid=item["article_articleid"]
            article_namespace=int(item["article_namespace"])
            article_text=item["article_text"].replace(u'\r',u'')
            article_prefixedtext=item["article_prefixedtext"]
            article_recent_contributors=item["article_recent_contributors"].replace(u'\r',u'').split(u'\n')
            action=item["action"]
            summary=item["summary"].replace(u'\r',u'')
            old_wikitext=item["old_wikitext"].replace(u'\r',u'')
            new_wikitext=item["new_wikitext"].replace(u'\r',u'')
            edit_diff=item["edit_diff"].replace(u'\r',u'')
            new_size=int(item["new_size"])
            old_size=int(item["old_size"])
            edit_delta=int(item["edit_delta"])
            added_lines=item["added_lines"].replace(u'\r',u'')
            removed_lines=item["removed_lines"].replace(u'\r',u'')
            tor_exit_node=item["tor_exit_node"]
            timestamp=int(item["timestamp"])
            abus_dict[log_id]=[user_editcount,user_name,user_age,user_groups,user_mobile,article_articleid
                                ,article_namespace,article_text,article_prefixedtext,article_recent_contributors
                                ,action,summary,old_wikitext,new_wikitext,edit_diff,new_size,old_size,edit_delta
                                ,added_lines,removed_lines,tor_exit_node,timestamp,abus_id]
    return abus_dict

def alarm_to_user(all_alarms):
    add_text,add_text2=u'\n',u'\n'
    for alarms in all_alarms:
        counter=0
        add_line=u'\n'
        for i in all_alarms[alarms]:
            article_history=u'[//fa.wikipedia.org/w/index.php?title='+i[5].replace(u' ',u'_')+u'&action=history تاریخچه]'
            reverted,watched_by=u'',u''
            counter+=1
            if i[2]:
                last_edit=u"بله"
            else:
                if i[3]:
                    watched_by=u'[[کاربر:'+u' ]] — [[کاربر:'.join(i[3])+u']]'
                else:
                    watched_by=u''
                if i[4]:
                    reverted=u'{{شد}}'
                else:
                    reverted=u''
                last_edit=u''
            add_line+=u'|'+En2Fa(counter)+u'||'+i[0]+u'||[[:'+i[5]+u']]||['+i[1].replace(u' ',u'_')+u' پیوند تفاوت]||'+watched_by+u'||'+reverted+u'||'+last_edit+u'||'+article_history+u'\n|-\n'
            
        if add_line.strip():
            add_text+=u'\n== '+alarms+u' ==\n{| class="wikitable plainlinks" style="width:70%; text-align:center;"\n|- style="white-space:nowrap;"\n|+'+alarms+u'\n!#!!کاربر!!در صفحهٔ!!پیوند تفاوت ویرایش!!ویرایش بعدی توسط{{سخ}}کاربر گشت یا گشت‌خودکار!!واگردانی شد؟!!آخرین ویرایش؟!!تاریخچه'+u'\n|-\n'
            add_text+=add_line+u'|}\n'

    Alarm_page = wikipedia.Page(faSite,u'ویکی‌پدیا:گزارش دیتابیس/ویرایش‌های تازه‌کاران که نیازمند بازبینی هستند')
    Alarm_page.put(u'{{/بالا}}\n'+add_text,u'ربات:به‌روزرسانی گزارش')
    Alarm_page2 = wikipedia.Page(faSite,u'ویکی‌پدیا:گزارش دیتابیس/ویرایش‌های تازه‌کاران که نیازمند بازبینی هستند/امضا')
    Alarm_page2.put(u'~~~~~',u'ربات:به‌روزرسانی گزارش')
    #Alarm_text=
    '''\n== هشدار ==
درود، ویرایش شما در صفحهٔ %s مشکوک به خرابکاری بود.
لطفاً شیوه‌نامه و سیاست‌نامه‌های ویرایشی ویکی‌پدیای فارسی را مطالعه کنید.~~~~''' #General Alarm
    '''
    UserTalkPage = wikipedia.Page(faSite,u'بحث کاربر:'+user)
    try:               
        usertext = UserTalkPage.get()+Alarm_text
        UserTalkPage.put(usertext, u'ربات:گزارش خرابکاری')
    except:
        wikipedia.output(u'User Talk page was blocked or does not exist')
        pass
    '''
def Get_URL_link(user_name,article_prefixedtext,timestamp,summary,page_size):
    our_URL=False
    timestamp1=unicode(datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ'),'UTF8')
    timestamp2=unicode(datetime.fromtimestamp(timestamp-1).strftime('%Y-%m-%dT%H:%M:%SZ'),'UTF8')
    timestamp3=unicode(datetime.fromtimestamp(timestamp+1).strftime('%Y-%m-%dT%H:%M:%SZ'),'UTF8')
    PageHist = wikipedia.Page(faSite,article_prefixedtext)
    reverting=False
    watched_by_patroller=[]
    try:
        text_history=PageHist.getVersionHistory(revCount=20000)
    except:
        wikipedia.output(u'\03{lightred}Article is deleted\03{default}')
        return False,False,False,False
    counter,revetion_counter=0,0
    for l in text_history:
        counter+=1
        Hi_ArticleID=l[0]
        Hi_timestamp=l[1]
        Hi_user=l[2]
        Hi_summary=l[3]
        Hi_page_size=l[4]
        user_right=check_user_rights(Hi_user)
        if (u'واگردانده' in Hi_summary or u'خنثی‌سازی' in Hi_summary or u'واگردانی' in Hi_summary) and not reverting:
            revetion_counter=counter
            reverting=True
        if "patrol" in user_right or "autopatrol" in user_right:
            if not Hi_user in watched_by_patroller:
                watched_by_patroller.append(Hi_user)

        if Hi_user==user_name and  Hi_page_size==page_size:#Hi_summary==summary and
            if Hi_timestamp==timestamp1:
                our_URL=u'//fa.wikipedia.org/w/index.php?title='+article_prefixedtext+u'&diff=prev&oldid='+str(Hi_ArticleID)
                break
            elif Hi_timestamp==timestamp2:
                our_URL=u'//fa.wikipedia.org/w/index.php?title='+article_prefixedtext+u'&diff=prev&oldid='+str(Hi_ArticleID) 
                break
            elif Hi_timestamp==timestamp3:
                our_URL=u'//fa.wikipedia.org/w/index.php?title='+article_prefixedtext+u'&diff=prev&oldid='+str(Hi_ArticleID) 
                break
            else:
                continue
    if revetion_counter<counter and reverting:
        reverting=True
    else:
        reverting=False

    last_edit=False
    if counter==1 and our_URL:
        last_edit=True
    return our_URL,last_edit,watched_by_patroller,reverting

def check_abus_log(user_edit_detail,all_alarms):
    user_editcount=user_edit_detail[0]
    user_name=user_edit_detail[1]
    user_age=user_edit_detail[2]
    user_groups=user_edit_detail[3]
    user_mobile=user_edit_detail[4]
    article_articleid=user_edit_detail[5]
    article_namespace=user_edit_detail[6]
    article_text=user_edit_detail[7]
    article_prefixedtext=user_edit_detail[8]
    article_recent_contributors=user_edit_detail[9]
    action=user_edit_detail[10]
    summary=user_edit_detail[11]
    old_wikitext=user_edit_detail[12]
    new_wikitext=user_edit_detail[13]
    edit_diff=user_edit_detail[14]
    new_size=user_edit_detail[15]
    old_size=user_edit_detail[16]
    edit_delta=user_edit_detail[17]
    added_lines=user_edit_detail[18]
    removed_lines=user_edit_detail[19]
    tor_exit_node=user_edit_detail[20]
    timestamp=user_edit_detail[21]
    abus_id=user_edit_detail[22]

    double_s={u'{':u'}',u'[':u']',u'<':u'>',u'(':u')'}
    if article_namespace==0 and user_editcount<1000:
        our_cites=0
        my_Url,last_edit,watched_by_patroller,reverting=Get_URL_link(user_name,article_prefixedtext,timestamp,summary,new_size)
        if not my_Url:
            wikipedia.output(u'\03{lightred}I can not find the URL\03{default}')
            return False,all_alarms
        for cites in [u'<ref',u'{{یادکرد', u'{{Cite' , u'{{cite']:
            our_cites=our_cites-string.count(removed_lines,cites)+string.count(added_lines,cites)
        if our_cites<0: #حذف منبع از مقاله توسط تازه‌کار
            all_alarms[u'حذف منبع از مقاله توسط تازه‌کار'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
            return True,all_alarms
        if our_cites==0 and edit_delta>1000 and string.count(old_wikitext,u'<')==string.count(new_wikitext,u'<'):#افزودن متن فله‌ای
            all_alarms[u'افزودن متن فله‌ای'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
            return True,all_alarms
        for X in double_s:#خراب کردن سینتکس ویکی
            if string.count(old_wikitext,X)==string.count(old_wikitext,double_s[X]) and string.count(new_wikitext,X)!=string.count(new_wikitext,double_s[X]):
                all_alarms[u'خراب کردن سینتکس ویکی'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
                return True,all_alarms
        #افزودن لینک اسپم
        for X in [u'https://',u'http://',u'www.']:
            if string.count(new_wikitext,X) > string.count(old_wikitext,X) and (not user_name in article_recent_contributors) and our_cites<1:
                all_alarms[u'افزودن لینک اسپم'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
                return True,all_alarms

        #افزودن متن نامربوط
        if (not u'<ref' in added_lines) and len(added_lines)>0 and (removed_lines==u'') and (not user_name in article_recent_contributors):
            if (not u'[[' in added_lines) and (not u'{{' in added_lines):
                all_alarms[u'افزودن متن نامربوط'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
                return True,all_alarms

        #تغییر در متن منبع‌دار
        if (u'<ref' in added_lines) and (u'<ref' in removed_lines) and our_cites==0 and removed_lines.split(u'<ref')[0]!=removed_lines.split(u'<ref')[0] and (not user_name in article_recent_contributors):             
            all_alarms[u'تغییر در متن منبع‌دار'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
            return True,all_alarms

    added_items=edit_diff.split(u'\n+')
    removed_items=edit_diff.split(u'\n-')
    added_items_2,removed_items_2=[],[]
    for i in added_items:
        added_items_2.append(i.split(u'\n')[0])
    for i in removed_items:
        removed_items_2.append(i.split(u'\n')[0])
    first_added=added_items_2[0].replace(u'_',u' ')
    #افزودن عبارت‌های بی‌معنی
    if string.count(first_added,u' ')<2 and (not u'*' in first_added) and (not u'#' in first_added) and (not u'[' in first_added):
        all_alarms[u'افزودن عبارت‌های بی‌معنی'].append([user_name,my_Url,last_edit,watched_by_patroller,reverting,article_text])
        return True,all_alarms

    return False,all_alarms


def run(abus_dict,all_alarms):
    count=0
    for log_id in abus_dict:
        wikipedia.output(log_id+u'******')
        details=abus_dict[log_id]
        result,all_alarms=check_abus_log (details,all_alarms)
        count+=1
        if result:
            wikipedia.output(u'----'+str(count)+u'---'+log_id+u'--user='+details[1]+u'----abus_ID='+details[22]+u'----------')
        else:
            wikipedia.output(u'#'+str(count)+u' His/Her edit on '+details[7]+u' was correct')
            continue
    return all_alarms

    
def main():
    all_alarms={u'حذف منبع از مقاله توسط تازه‌کار':[],u'افزودن متن فله‌ای':[],u'خراب کردن سینتکس ویکی':[]
                ,u'افزودن لینک اسپم':[],u'افزودن متن نامربوط':[],u'تغییر در متن منبع‌دار':[],
                u'افزودن عبارت‌های بی‌معنی':[]}
    login_fa()
    minute_ago=1500# It checks AbuseLog every minute_ago
    pasttime = str(datetime.now()-timedelta(seconds=60*minute_ago)).replace(' ','T')[:-7]+'Z'
    wikipedia.output(u'\03{lightblue}Cheking AbuseLog since: '+pasttime+u'\03{default}')
    abus_nums=[122]#[105,104]#Abus ID (104 >Ip's edits 105> new users edits)
    for abusnum in abus_nums:
        abus_dict=Query_Abus(pasttime,abusnum)
        if abus_dict!=[]:#If any Abuse is acured in this period!
            all_alarms=run(abus_dict,all_alarms)
        else:
            wikipedia.output(u'There is not abus log in this period (20 last min)!')
    alarm_to_user(all_alarms)
if __name__ == '__main__':
    main()
