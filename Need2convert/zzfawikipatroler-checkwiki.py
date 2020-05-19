#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2017
# Distributed under the terms of the MIT license.
#
import login,string
import re,urllib2,query
import wikipedia,config

wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
faSite = wikipedia.getSite('fa')
msg=u' '
version='4.3'
checkwiki_ids=[8,10,19,28,43,69,70,71,72,73,80,83,90,92,94,105]
#checkwiki_ids=[83,90]
Checkwiki_cases={}

def getRollbackToken():
        params = {
            'action':  'query',
            'meta':    'tokens',
            'type':  'rollback'
        }
        try:
            data = query.GetData(params)
            if 'error' in data:
                raise RuntimeError('%s' % data['error'])
            elif 'warnings' in data:
                raise RuntimeError('%s' % data['warnings'])
            return data['query']['tokens']['rollbacktoken']
        except KeyError:
            raise ServerError(
                "The APIs don't return data, the site may be down")

def revert(user,pagetitle):
    page = wikipedia.Page(site, pagetitle)
    try:
        parameters={'action': 'rollback',
                   'title': pagetitle,
                   'user': user,
                   'token': getRollbackToken(),
                   'markbot': True}
        myrevert = query.GetData(parameters,site)
    except :
        wikipedia.output(u"\03{lightpurple} we couldn't revert the user\03{default}")
        pass



def en2fa(text):
    counti=-1
    for i in u'۰۱۲۳۴۵۶۷۸۹':
        counti+=1
        text=text.replace(str(counti),i)
    return text

def login_fa(bot):
    if bot==u'rezabot':
        password_fa = open("/data/project/rezabot/pywikipedia/passfile", 'r')
    else:
        password_fa = open("/data/project/rezabot/pywikipedia/passfile3", 'r')

    password_fa=password_fa.read().replace('"','').strip()
    passwords=password_fa.split('(')[1].split(',')[1].split(')')[0].strip()
    usernames=password_fa.split('(')[1].split(',')[0].split(')')[0].strip()
    #-------------------------------------------
    botlog=login.LoginManager(password=passwords,username=usernames,site=faSite)
    botlog.login()

def get_history(workpage):
    try:
        page = wikipedia.Page(faSite,workpage)
        text=page.get()
        page_history=page.fullVersionHistory()
    except wikipedia.IsRedirectPage:
        page = page.getRedirectTarget()
        try:
            text=page.get()
            page_history=page.fullVersionHistory(revCount=500)
        except:
            return []
    except:
        return []
    return page_history

def history_result(page_history,case,article_title,Checkwiki_id,userdict,i,extend):
    page_text_1=page_history[i][3].replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'\t',u' ')
    page_id=page_history[i][0]
    username=page_history[i][2]
    case_encode=urllib2.quote(case.encode('utf8'))
    if Checkwiki_id==90:
        if case in page_text_1:
            casewiki=u'<code><nowiki>'+case.replace(u'<',u'&lt;').replace(u'>',u'&gt;')+u'</nowiki></code>'
        else:
            casewiki=u'<code><nowiki>'+case_encode.replace(u'<',u'&lt;').replace(u'>',u'&gt;')+u'</nowiki></code>'
    else:
        casewiki=u'<code><nowiki>'+case.replace(u'<',u'&lt;').replace(u'>',u'&gt;')+u'</nowiki></code>'
    if username in userdict:
        user_list=userdict[username]
        userdict[username]=userdict[username]+[[article_title,page_id,Checkwiki_id,casewiki,extend,i]]
    else:
        userdict[username]=[[article_title,page_id,Checkwiki_id,casewiki,extend,i]]
    wikipedia.output(u'\03{lightpurple}Checkwiki_id='+str(Checkwiki_id)+u'> username= '+username+u' article_title='+article_title+u' page_id='+str(page_id)+u'\03{default}')
    return userdict

def check_history(page_history,case,article_title,Checkwiki_id,userdict):
    case_old=case.replace(u'\r',u'').replace(u'\n',u'').strip()
    case=case.replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u' ',u' ').replace(u'\t',u' ').strip()
    page_text_0=page_history[0][3]
    for i in range(0, len(page_history)-1):
        if i < len(page_history)-2:
            page_text_1=page_history[i][3].replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'\t',u' ').replace(u' ',u' ')
            page_text_2=page_history[i+1][3].replace(u'\r',u'').replace(u'\n',u'').replace(u'  ',u' ').replace(u'  ',u' ').replace(u'\t',u' ').replace(u' ',u' ')
            comment=page_history[i][4]
            username=page_history[i][2]
            Year_timestamp=int(page_history[i][1].split(u'-')[0].strip())
            if Year_timestamp < 2016:
                continue
            if u'خنثی' in comment or u'واگردان' in comment or u'برگردان' in comment:
                continue
            if username:
                extend=u''
                if Checkwiki_id== 8: # number 8
                    page_text_22=page_history[i+1][3].replace(u'\r',u'')
                    page_text_11=page_history[i][3].replace(u'\r',u'')
                    c1=string.count(page_text_22,u'==\n')
                    c2=string.count(page_text_22,u'\n==')
                    n1=string.count(page_text_11,u'==\n')
                    n2=string.count(page_text_11,u'\n==')
                    if string.count(page_text_0,u'==\n')-string.count(page_text_0,u'\n==')==0:
                        break
                    extend=u' c1 >>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if n2-n1<0:
                        diff_n=n1-n2
                        diff_c=c1-c2
                    else:
                        diff_n=n2-n1
                        diff_c=c2-c1
                    if c2==c1:
                        if n2!=n1 and case in page_text_1:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                    else:
                        if diff_n > diff_c and case in page_text_1:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                elif Checkwiki_id== 10: # number 10
                    c1=string.count(page_text_2,u'[[')
                    c2=string.count(page_text_2,u']]')
                    n1=string.count(page_text_1,u'[[')
                    n2=string.count(page_text_1,u']]')
                    if string.count(page_text_0,u'[[')-string.count(page_text_0,u']]')==0:
                        break
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if c1==c2 and n2!=n1:
                        if case in page_text_1:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                        else:
                            userdict=history_result(page_history,u'',article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                elif Checkwiki_id== 19: # number 19
                    page_text_11=page_history[i][3].replace(u'‌',u' ').replace(u' ',u' ').replace(u'    ',u' ').replace(u'   ',u' ').replace(u'   ',u' ').replace(u'  ',u' ').replace(u'  =',u'=').replace(u' =',u'=').replace(u'=  ',u'=').replace(u'= ',u'=').replace(u'\r',u'').replace(u'\n ',u'\n')+u'\n'
                    page_text_22=page_history[i+1][3].replace(u'‌',u' ').replace(u' ',u' ').replace(u'    ',u' ').replace(u'   ',u' ').replace(u'   ',u' ').replace(u'  ',u' ').replace(u'  =',u'=').replace(u' =',u'=').replace(u'=  ',u'=').replace(u'= ',u'=').replace(u'\r',u'').replace(u'\n ',u'\n')+u'\n'
                    c1=string.count(page_text_22,u'\n=')
                    c2=string.count(page_text_22,u'=\n')
                    n1=string.count(page_text_11,u'\n=')
                    n2=string.count(page_text_11,u'=\n')
                    if string.count(page_text_0,u'\n=')-string.count(page_text_0,u'=\n')==0:
                        break
                    newcase=u'\n'+case.replace(u'‌',u' ').replace(u'    ',u' ').replace(u'   ',u' ').replace(u'   ',u' ').replace(u'  ',u' ').replace(u' =',u'=').replace(u'  =',u'=').replace(u'= ',u'=').replace(u'=  ',u'=')+u'\n'
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if c1==c2:
                        if n2!=n1 and newcase in page_text_11 and not newcase in page_text_22:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                    else:
                        if n2-n1!= c2-c1 and newcase in page_text_11 and not newcase in page_text_22:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                elif Checkwiki_id== 28: # number 28
                    page_text_0=page_text_0.replace(u' ',u' ').replace(u' |}',u'|}').replace(u' |}',u'|}').replace(u'{| ',u'{|').replace(u'{|  ',u'{|').replace(u'\r',u'').replace(u'{{Fb end}}',u'|}').replace(u'{{Fb start}}',u'{|')+u'\n'
                    page_text_11=page_history[i][3].replace(u' ',u' ').replace(u' |}',u'|}').replace(u' |}',u'|}').replace(u'{| ',u'{|').replace(u'{|  ',u'{|').replace(u'\r',u'').replace(u'{{Fb end}}',u'|}').replace(u'{{Fb start}}',u'{|')+u'\n'
                    page_text_22=page_history[i+1][3].replace(u' ',u' ').replace(u' |}',u'|}').replace(u' |}',u'|}').replace(u'{| ',u'{|').replace(u'{|  ',u'{|').replace(u'\r',u'').replace(u'{{Fb end}}',u'|}').replace(u'{{Fb start}}',u'{|')+u'\n'
                    c1=string.count(page_text_22,u'|}')
                    c2=string.count(page_text_22,u'{|')
                    n1=string.count(page_text_11,u'|}')
                    n2=string.count(page_text_11,u'{|')
                    if string.count(page_text_0,u'|}')-string.count(page_text_0,u'{|')==0:
                        break
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if c1==c2 and n2!=n1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict

                elif Checkwiki_id== 43: # number 43
                    for a in [u'nowiki',u'math',u'mapframe',u'ce',u'score',u'source',u'syntaxhighlight']:
                        page_text_2=re.sub(u'\< ?'+a+u' ?(?:.*?)\>(.*?)\< ?\/ ?'+a+u' ?\>',u'',page_text_2)
                        page_text_2=re.sub(u'\<\!\-\-(.*?)\-\-\>',u'',page_text_2)
                        page_text_1=re.sub(u'\< ?'+a+u' ?(?:.*?)\>(.*?)\< ?\/ ?'+a+u' ?\>',u'',page_text_1)
                        page_text_1=re.sub(u'\<\!\-\-(.*?)\-\-\>',u'',page_text_1)
                    c1=string.count(page_text_2,u'}}')
                    c2=string.count(page_text_2,u'{{')
                    n1=string.count(page_text_1,u'}}')
                    n2=string.count(page_text_1,u'{{')
                    if n2-n1<0:
                        diff_n=n1-n2
                        diff_c=c1-c2
                    else:
                        diff_n=n2-n1
                        diff_c=c2-c1
                    if string.count(page_text_0,u'}}')-string.count(page_text_0,u'{{')==0:
                        break
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)#+u', d1>>'+str(d1)+u', d2>>'+str(d2)+u', e1>>'+str(e1)+u', e2>>'+str(e2)
                    if c1==c2:
                        if n2!=n1 and case in page_text_1:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                elif Checkwiki_id> 68 and  Checkwiki_id< 74: # number 69 to 73
                    page_text_2=page_text_2.replace(u'isbn',u'ISBN').replace(u'Isbn',u'ISBN')
                    page_text_1=page_text_1.replace(u'isbn',u'ISBN').replace(u'Isbn',u'ISBN')
                    if re.search(ur'(ISBN[\d _\=\-\:۰۱۲۳۴۵۶۷۸۹]+)[^\}\]\)\(\<a-z-A-Z\/]+', case):
                        case=re.search(ur'(ISBN[\d _\=\-\:۰۱۲۳۴۵۶۷۸۹]+)[^\}\]\)\(\<a-z-A-Z\/]+', case).group()
                    if case in page_text_1 and not case in page_text_2:
                        if Checkwiki_id==69 and  string.count(page_text_1,u'ISBN') > string.count(page_text_2,u'ISBN'):
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                        else:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                elif Checkwiki_id== 80:# number 80
                    c1=string.count(page_text_2,u'[')
                    c2=string.count(page_text_2,u']')
                    n1=string.count(page_text_1,u'[')
                    n2=string.count(page_text_1,u']')
                    if string.count(page_text_0,u'[')-string.count(page_text_0,u']')==0:
                        break
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if n2-n1<0:
                        diff_n=n1-n2
                        diff_c=c1-c2
                    else:
                        diff_n=n2-n1
                        diff_c=c2-c1
                    if c1==c2:
                        if  n2!=n1:
                            if case in page_text_1:
                                userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                                return userdict
                    else:
                        if diff_n>diff_c and case in page_text_1 and diff_n!=0:
                            userdict=history_result(page_history,u'',article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                elif Checkwiki_id== 83: # number 83
                    page_text_11=page_history[i][3].replace(u'‌',u' ').replace(u'    ',u' ').replace(u'   ',u' ').replace(u'   ',u' ').replace(u'  ',u' ').replace(u' =',u'=').replace(u'  =',u'=').replace(u'= ',u'=').replace(u'=  ',u'=').replace(u'\r',u'')
                    page_text_22=page_history[i+1][3].replace(u'‌',u' ').replace(u'    ',u' ').replace(u'   ',u' ').replace(u'   ',u' ').replace(u'  ',u' ').replace(u' =',u'=').replace(u'  =',u'=').replace(u'= ',u'=').replace(u'=  ',u'=').replace(u'\r',u'')
                    c1=string.count(page_text_22,u'===\n')
                    c2=string.count(page_text_22,u'==\n')
                    n1=string.count(page_text_11,u'===\n')
                    n2=string.count(page_text_11,u'==\n')
                    newcase=case.replace(u'‌',u' ').replace(u'    ',u' ').replace(u'   ',u' ').replace(u'   ',u' ').replace(u'  ',u' ').replace(u' =',u'=').replace(u'  =',u'=').replace(u'= ',u'=').replace(u'=  ',u'=').replace(u'\r',u'').strip()
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if n1!=c1 and newcase in page_text_11 and not newcase in page_text_22:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict
                    if n2!=c2 and newcase in page_text_11 and not newcase in page_text_22:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict
                elif Checkwiki_id== 90:# number 90
                    page_text_0=page_text_0.replace(u'fa.m.wikipedia.org',u'fa.wikipedia.org')
                    page_text_1=page_text_1.replace(u'fa.m.wikipedia.org',u'fa.wikipedia.org')
                    page_text_2=page_text_2.replace(u'fa.m.wikipedia.org',u'fa.wikipedia.org')
                    if string.count(page_text_0,u'fa.wikipedia.org')==0:
                        break
                    extend=u' r1>>'+str(string.count(page_text_1,u'fa.wikipedia.org'))+u', r2>>'+str(string.count(page_text_2,u'fa.wikipedia.org'))
                    if string.count(page_text_1,u'fa.wikipedia.org') > string.count(page_text_2,u'fa.wikipedia.org'):
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict
                elif Checkwiki_id== 92: # number 92
                    if string.count(page_text_1,case)>=string.count(page_text_2,case)+1 and case in page_text_1:
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict
                elif Checkwiki_id== 94: # number 94
                    page_text_11=page_history[i][3].replace(u'‌',u' ').replace(u' ',u' ').replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    page_text_22=page_history[i+1][3].replace(u'‌',u' ').replace(u' ',u' ').replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    page_text_1=page_text_1.replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    page_text_2=page_text_2.replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    case=case.replace(u'‌',u' ').replace(u'/ >',u'/>').replace(u'/ >',u'/>').replace(u'< /',u'</')
                    if case in page_text_1 and not case in page_text_2 and (string.count(page_text_11,u'<ref')-string.count(page_text_11,u'/>')-string.count(page_text_11,u'>')+string.count(page_text_11,u'</')!=string.count(page_text_22,u'<ref')-string.count(page_text_22,u'/>')-string.count(page_text_22,u'>')+string.count(page_text_22,u'</')):
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict
                elif Checkwiki_id== 105: # number 105
                    page_text_22=page_history[i+1][3].replace(u'‌',u' ').replace(u' ',u' ').replace(u'\r',u'')
                    page_text_11=page_history[i][3].replace(u'‌',u' ').replace(u' ',u' ').replace(u'\r',u'')
                    c1=string.count(page_text_22,u'==\n')
                    c2=string.count(page_text_22,u'\n==')
                    n1=string.count(page_text_11,u'==\n')
                    n2=string.count(page_text_11,u'\n==')
                    if string.count(page_text_0,u'==\n')-string.count(page_text_0,u'\n==')==0:
                        break
                    extend=u' c1>>'+str(c1)+u', c2>>'+str(c2)+u', n1>>'+str(n1)+u', n2>>'+str(n2)
                    if c2==c1:
                        if n2!=n1 and case.replace(u'‌',u' ') in page_text_1:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict
                    else:
                        if n2-n1 != c2-c1 and case.replace(u'‌',u' ') in page_text_1:
                            userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                            return userdict

                else:
                    if case.replace(u'‌',u' ') in page_text_1 and not case.replace(u'‌',u' ') in page_text_2:
                        comment=page_history[i][4]
                        userdict=history_result(page_history,case_old,article_title,Checkwiki_id,userdict,i,extend)
                        return userdict
    return userdict

def user_alarm (userdict):
    for user in userdict:
        try:
            pageuser = wikipedia.Page(faSite,u'بحث کاربر:'+user)
            text_user=pageuser.get()
        except wikipedia.NoPage:
            text_user=u'\n'
        except wikipedia.IsRedirectPage:
            pageuser = pageuser.getRedirectTarget()
            try:
                text_user=pageuser.get()
            except wikipedia.NoPage:
                text_user=u'\n'
            except:
                wikipedia.output(u"couldn't open user page")
                text_user=u''
                continue
        except:
            wikipedia.output(u"couldn't open user page")
            continue
        user_text_begin=u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۰|'
        user_text_end=u'لطفاً نسبت به رفع خطا اقدام نمائید؛ در صورتی که به اشتباه مخاطب قرار گرفتید لطفاً در اصلاح مشکل مذکور به ویکی‌پدیای فارسی کمک کنید. باتشکر <b>[[ویکی‌پدیا:نگهبانی|<span style="color:#7D053F; font-size:150%; font-family: "Edwardian Script ITC" ; class=texhtml">↺</span>]] [[کاربر:FawikiPatroller|<span style="color:#616D7E">نگهبان ویکی‌پدیا</span>]]</b> ~~~~~'
        user_text=u'\n'
        articles=u' '
        for user_case in userdict[user]:
            if user_case[5]==0:
                if re.sub(ur'[0-9\.]+',u'',user).strip()==u'' or u':' in user:
                    #go to revert
                    #login_fa(u'rezabot2')
                    #revert(user,user_case[0])
                    #login_fa(u'rezabot')
                    wikipedia.output(u"\03{lightblue}Ip revision is reverted:"+user+u'\03{default}')
                    continue
            if re.sub(ur'[0-9\.]+',u'',user).strip()==u'' or u':' in user or 'Bot' in user or 'bot' in user:
                continue
            if u'در مقالهٔ [['+user_case[0]+u']]' in text_user:
                continue
            if not u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۲|'+str(user_case[2])+u'}}' in user_text:
                user_text+=u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۲|'+str(user_case[2])+u'}}\n'
            user_text+=u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۱|'+user_case[0]+u'|'+str(user_case[1])+u'|'+str(user_case[2])+u'|'+user_case[3]+u'|'+user_case[0].replace(u' ',u'%20')+u'|'+user_case[4]+u'}}\n'
            articles+=u'[['+user_case[0]+u']]، '
        if len(userdict[user])>1:
            user_text_begin=user_text_begin+u'خطاهای}}'
        else:
            user_text_begin=user_text_begin+u'خطای}}'
        if not u'{{جا:کاربر:FawikiPatroller/چک‌ویکی۱|' in user_text:
            continue
        alarms=user_text_begin+u'\n'+user_text.strip()+u'\n'+user_text_end
        msg_num=articles.split(u'،')
        if len(msg_num)<6:
            msg=u'ربات-کاربر:ارسال پیام دربارهٔ خطای ویرایشی '+articles.strip()[:-1]
        else:
            msg=u'ربات-کاربر:ارسال پیام دربارهٔ خطای ویرایشی '+en2fa(str(len(msg_num)))+u' مقاله'
        try:
            if not text_user:
                wikipedia.output(u'\03{lightred} user page not found or edit \03{default}')
                continue
            pageuser.put(text_user+u'\n'+alarms.strip(), msg)
            wikipedia.output(u"\03{lightgreen}="+user+u'=\n'+alarms.strip()+u'\03{default}')
            #wikipedia.output(u"\03{lightred} msg= "+msg+u'\03{default}')
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
            try:
                userdict=check_history(page_history,Checkwiki_cases[Checkwiki_id][article_title],article_title,Checkwiki_id,userdict)
            except:
                continue
    user_alarm (userdict)

def main():
    login_fa(u'rezabot')
    for id in checkwiki_ids:
        wikipedia.output(u'\03{lightpurple}Checkwiki number = '+str(id)+u'\03{default}')
        get_checkwiki_list(id)
    run()

if __name__ == '__main__':
    wikipedia.output(u'\03{lightpurple}      *******************************\03{default}')  
    wikipedia.output(u'\03{lightpurple}      *     Code version is '+version+u'    *\03{default}')
    wikipedia.output(u'\03{lightpurple}      *******************************\03{default}')
    main()