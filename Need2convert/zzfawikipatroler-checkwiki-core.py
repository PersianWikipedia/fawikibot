#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2017
# Distributed under the terms of the MIT license.
#
import string
import re
import urllib2
import pywikibot

faSite = pywikibot.Site('fa')
msg=u' '
version='1.1'
checkwiki_ids=[8,10,19,28,43,69,70,71,72,73,80,83,90,92,94,104,105]

Checkwiki_cases={}
def en2fa(text):
    counti=-1
    for i in u'۰۱۲۳۴۵۶۷۸۹':
        counti+=1
        text=text.replace(str(counti),i)
    return text

def login_fa(bot):
    if bot==u'FawikiPatroller':
        try:
            password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
        except:
            password_fa = open("/home/reza/compat/passfile2", 'r')
    else:
        try:
            password_fa = open("/data/project/rezabot/pywikipedia/passfile", 'r')
        except:
            password_fa = open("/home/reza/compat/passfile", 'r')

    password_fa=password_fa.read().replace('"','').strip()
    passwords=password_fa.split('(')[1].split(',')[1].split(')')[0].strip()
    usernames=password_fa.split('(')[1].split(',')[0].split(')')[0].strip()
    #-------------------------------------------
    botlog=login.LoginManager(password=passwords,username=usernames,site=faSite)
    botlog.login()

def get_history(workpage):
    try:
        page = pywikibot.Page(faSite,workpage)
        text=page.get()
        page_history=page.fullVersionHistory()
        #first_user=page_history[-1][2]
        #time_stamp=page_history[-1][1]
    except pywikibot.IsRedirectPage:
        page = page.getRedirectTarget()
        try:
            text=page.get()
            page_history=page.fullVersionHistory()
        except:
            return []
    except:
        return []
    return page_history

def history_result(page_history,case,article_title,Checkwiki_id,userdict,i):
    page_id=page_history[i][0]
    username=page_history[i][2]
    casewiki=u'<code><nowiki>'+case.replace(u'<',u'&lt;').replace(u'>',u'&gt;')+u'</nowiki></code>'
    if username in userdict:
        user_list=userdict[username]
        userdict[username]=userdict[username]+[[article_title,page_id,Checkwiki_id,casewiki]]
    else:
        userdict[username]=[[article_title,page_id,Checkwiki_id,casewiki]]
    pywikibot.output(u'\03{lightpurple}Checkwiki_id='+str(Checkwiki_id)+u'> username= '+username+u' article_title='+article_title+u' page_id='+str(page_id)+u'\03{default}')
    return userdict

def check_history(page_history,case,article_title,Checkwiki_id,userdict):
    case_old=case.replace(u'\r',u'').replace(u'\n',u'').strip()
    case=case.replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'\t',u' ').strip()
    for i in range(0, len(page_history)-1):
        if i < len(page_history)-2:
            page_text_1=page_history[i][3].replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'\t',u' ')
            page_text_2=page_history[i+1][3].replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'\t',u' ')
            comment=page_history[i][5]
            username=page_history[i][2]
            if u'خنثی' in comment or u'واگردان' in comment or u'برگردان' in comment:
                pywikibot.output(u"\03{lightred}it was revert so omited. comment > "+comment+u'\03{default}')
                continue
            if username:
                if not re.sub(ur'[0-9\.]+',u'',username).strip() or  u':' in username or  u'bot' in username or  u'Bot' in username:
                    pywikibot.output(u"\03{lightred}User:"+username+u' is IP or Bot so it is omited\03{default}')
                    if re.sub(ur'[0-9\.]+',u'',username).strip() and not u':' in username:
                        #gotorevert
                        pywikibot.output(u"\03{lightblue}Ip revision is reverted:"+username+u'\03{default}')
                        pass
                    continue
                if Checkwiki_id== 90:# number 43
                    page_text_1=page_text_1.replace(u'fa.m.wikipedia.org',u'fa.wikipedia.org')
                    page_text_2=page_text_2.replace(u'fa.m.wikipedia.org',u'fa.wikipedia.org')
                    if string.count(page_text_1,u'fa.wikipedia.org') > string.count(page_text_2,u'fa.wikipedia.org'):
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)
                        return userdict
                elif Checkwiki_id== 8: # number 8
                    if string.count(page_history[i][3].replace(u'\r',u''),u'==\n')-string.count(page_history[i][3].replace(u'\r',u''),u'\n==')!=string.count(page_history[i+1][3].replace(u'\r',u''),u'==\n')-string.count(page_history[i+1][3].replace(u'\r',u''),u'\n==') and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 10: # number 10
                    if string.count(page_text_1,u'[[')!=string.count(page_text_1,u']]') and string.count(page_text_2,u'[[')==string.count(page_text_2,u']]') and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 19: # number 19
                    if string.count(page_history[i][3].replace(u'\r',u''),u'\n=')-string.count(page_history[i][3].replace(u'\r',u''),u'=\n')!=string.count(page_history[i+1][3].replace(u'\r',u''),u'\n=')-string.count(page_history[i+1][3].replace(u'\r',u''),u'=\n') and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 83: # number 83
                    if (string.count(page_history[i][3].replace(u'\r',u''),u'===')!=string.count(page_history[i+1][3].replace(u'\r',u''),u'===') or  string.count(page_history[i][3].replace(u'\r',u''),u'==')!=string.count(page_history[i+1][3].replace(u'\r',u''),u'=='))and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 92: # number 92
                    if string.count(page_text_1,case)>string.count(page_text_2,case) and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 94: # number 94
                    page_text_11=page_history[i][3].replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    page_text_22=page_history[i+1][3].replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    page_text_1=page_text_1.replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    page_text_2=page_text_2.replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    case=case.replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    if case in page_text_1 and not case in page_text_2 and (string.count(page_text_11,u'<ref')-string.count(page_text_11,u'/>')-string.count(page_text_11,u'>')+string.count(page_text_11,u'</')!=string.count(page_text_22,u'<ref')-string.count(page_text_22,u'/>')-string.count(page_text_22,u'>')+string.count(page_text_22,u'</')):
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 43: # number 43
                    # when {{ <> }}
                    if string.count(page_text_1,u'}}')!=string.count(page_text_1,u'{{') and string.count(page_text_2,u'}}')==string.count(page_text_2,u'{{') and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)
                        return userdict
                    # when [[ <> ]]
                    if string.count(page_text_1,u']]')!=string.count(page_text_1,u'[[') and string.count(page_text_2,u']]')==string.count(page_text_2,u'[[') and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                elif Checkwiki_id== 105: # number 105
                    if string.count(page_history[i][3].replace(u'\r',u''),u'\n==')-string.count(page_history[i][3].replace(u'\r',u''),u'==\n')!=string.count(page_history[i+1][3].replace(u'\r',u''),u'\n==')-string.count(page_history[i+1][3].replace(u'\r',u''),u'==\n') and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)        
                        return userdict
                else:
                    if case in page_text_1 and not case in page_text_2:
                        comment=page_history[i][5]
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i)
                        return userdict
    #pywikibot.output(u'\03{lightpurple}userdict= '+str(userdict)+u'\03{default}')
    return userdict

def user_alarm (userdict):
    for user in userdict:
        user_text_begin=u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۰|'
        user_text_end=u'لطفاً نسبت به رفع خطا اقدام نمائید. باتشکر <b>[[ویکی‌پدیا:نگهبانی|<span style="color:#7D053F; font-size:150%; font-family: "Edwardian Script ITC" ; class=texhtml">↺</span>]] [[کاربر:FawikiPatroller|<span style="color:#616D7E">نگهبان ویکی‌پدیا</span>]]</b> ~~~~~'
        user_text=u'\n'
        articles=u' '
        for user_case in userdict[user]:
        
            user_text+=u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۱|'+user_case[0]+u'|'+str(user_case[1])+u'|'+str(user_case[2])+u'|'+user_case[3]+u'|'+user_case[0].replace(u' ',u'%20')+u'}}\n'
            articles+=u'[['+user_case[0]+u']]، '
            #article_title,page_id,Checkwiki_id
        if len(userdict[user])>1:
            user_text_begin=user_text_begin+u'خطاهای}}'
        else:
            user_text_begin=user_text_begin+u'خطای}}'

        alarms=user_text_begin+u'\n'+user_text.strip()+u'\n'+user_text_end
        msg_num=articles.split(u'،')
        if msg_num<6:
            msg=u'ربات-کاربر:ارسال پیام دربارهٔ خطای ویرایشی '+articles.strip()[:-1]
        else:
            msg=u'ربات-کاربر:ارسال پیام دربارهٔ خطای ویرایشی '+en2fa(str(msg_num))+u' مقاله'
        try:
            pageuser = pywikibot.Page(faSite,u'بحث کاربر:'+user)
            text_user=pageuser.get()
        except pywikibot.NoPage:
            text_user=u'\n'
        except pywikibot.IsRedirectPage:
            pageuser = pageuser.getRedirectTarget()
            try:
                text_user=pageuser.get()
            except pywikibot.NoPage:
                text_user=u'\n'
            except:
                pywikibot.output(u"couldn't open user page")
                text_user=u''
        except:
            pywikibot.output(u"couldn't open user page")
        try:
            #pageuser.put(text_user+u'\n'+alarms.strip(), msg)
            pywikibot.output(u"\03{lightgreen}="+user+u'=\n'+alarms.strip()+u'\03{default}')
            #pywikibot.output(u"\03{lightred} msg= "+msg+u'\03{default}')
            if not text_user:
                pywikibot.output(u'\03{lightred} user page not found or edit \03{default}')
        except:
            continue

def get_checkwiki_list(id):
    our_id_items={}
    url="https://tools.wmflabs.org/checkwiki/cgi-bin/checkwiki.cgi?project=fawiki&view=only&id="+str(id)+"&offset=0&limit=500&orderby=&sort="
    page = urllib2.urlopen(url)
    check_text= page.read()
    check_text=unicode(check_text,'UTF-8')
    items= check_text.split(u'<tr><td class="table"')
    for i in items:
        if u'</a></td><td class=' in i:
            article_title=i.split(u'</a></td><td class="table"')[0].split(u'<a href="')[1].split(u'>')[1].strip()
            edit_case=i.split(u'<span style="unicode-bidi:embed;">')[1].split('</span></td><td class=')[0].strip()
            edit_case=edit_case.replace(u'&lt;',u'<').replace(u'&gt;',u'>')
            if edit_case.strip():
                our_id_items[article_title]=edit_case
    Checkwiki_cases[id]=our_id_items

def run ():
    userdict={}
    for Checkwiki_id in Checkwiki_cases:
        for article_title in Checkwiki_cases[Checkwiki_id]:
            page_history=get_history(article_title)
            userdict=check_history(page_history,Checkwiki_cases[Checkwiki_id][article_title],article_title,Checkwiki_id,userdict)
    user_alarm (userdict)

def main():
    for id in checkwiki_ids:
        pywikibot.output(u'\03{lightpurple}Checkwiki number = '+str(id)+u'\03{default}')
        get_checkwiki_list(id)
    run()

if __name__ == '__main__':
    pywikibot.output(u'\03{lightpurple}      *******************************\03{default}')  
    pywikibot.output(u'\03{lightpurple}      *     Code version is '+version+u'    *\03{default}')
    pywikibot.output(u'\03{lightpurple}      *******************************\03{default}')
    main()