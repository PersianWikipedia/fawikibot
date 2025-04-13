#!/usr/bin/python3
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
# Distributed under the terms of the MIT license.
#
#copy
#
#become checkdictation-fa
#cp zz_checkDictation_cmd.py /data/project/checkdictation-fa/www/python/src/
#
#source www/python/venv/bin/activate
#webservice2 uwsgi-python restart
# update
#python /data/project/checkdictation-fa/www/python/src/zz_checkDictation_cmd.py Botupdate
# to get list of wrong pages
#
#jsub -l release=trusty -once -N addbox  -mem 3g  /data/project/checkdictation-fa/www/python/venv/bin/python /data/project/checkdictation-fa/www/python/src/zz_checkDictation_cmd.py -start:!

import sys
# version 7.20

BotAdress = '/data/project/checkdictation-fa/www/python/src/'
BotAdress_main = '/data/project/checkdictation-fa/'
import os, json, re, io,string,time,requests,urllib.request,urllib.error,urllib.parse
from operator import itemgetter
try:
    from hunspell import Hunspell
    hobj = Hunspell('fa_IR', hunspell_data_dir=BotAdress)
except:
    print("Could not import hunspell")

persianPastVerbs = r'('
persianPastVerbs+=r'ارزید|افتاد|افراشت|افروخت|افزود|افسرد|افشاند|افکند|انباشت|انجامید|انداخت|اندوخت|اندود|اندیشید|انگاشت|انگیخت|انگیزاند|اوباشت|ایستاد'
persianPastVerbs+=r'|آراست|آراماند|آرامید|آرمید|آزرد|آزمود|آسود|آشامید|آشفت|آشوبید|آغازید|آغشت|آفرید|آکند|آگند|آلود|آمد|آمرزید|آموخت|آموزاند'
persianPastVerbs+=r'|آمیخت|آهیخت|آورد|آویخت|باخت|باراند|بارید|بافت|بالید|باوراند|بایست|بخشود|بخشید|برازید|برد|برید|بست|بسود|بسیجید|بلعید'
persianPastVerbs+=r'|بود|بوسید|بویید|بیخت|پاشاند|پاشید|پالود|پایید|پخت|پذیراند|پذیرفت|پراکند|پراند|پرداخت|پرستید|پرسید|پرهیزید|پروراند|پرورد|پرید'
persianPastVerbs+=r'|پژمرد|پژوهید|پسندید|پلاسید|پلکید|پناهید|پنداشت|پوسید|پوشاند|پوشید|پویید|پیچاند|پیچانید|پیچید|پیراست|پیمود|پیوست|تاباند|تابید|تاخت'
persianPastVerbs+=r'|تاراند|تازاند|تازید|تافت|تپاند|تپید|تراشاند|تراشید|تراوید|ترساند|ترسید|ترشید|ترکاند|ترکید|تکاند|تکانید|تنید|توانست|جَست|جُست'
persianPastVerbs+=r'|جست|جنباند|جنبید|جنگید|جهاند|جهید|جوشاند|جوشید|جوید|چاپید|چایید|چپاند|چپید|چراند|چربید|چرخاند|چرخید|چرید|چسباند|چسبید'
persianPastVerbs+=r'|چشاند|چشید|چکاند|چکید|چلاند|چلانید|چمید|چید|خاراند|خارید|خاست|خایید|خراشاند|خراشید|خرامید|خروشید|خرید|خزید|خست|خشکاند'
persianPastVerbs+=r'|خشکید|خفت|خلید|خمید|خنداند|خندانید|خندید|خواباند|خوابانید|خوابید|خواست|خواند|خوراند|خورد|خوفید|خیساند|خیسید|داد|داشت|دانست'
persianPastVerbs+=r'|درخشانید|درخشید|دروید|درید|درگذشت|دزدید|دمید|دواند|دوخت|دوشید|دوید|دید|دیدم|راند|ربود|رخشید|رساند|رسانید|رست|رَست|رُست'
persianPastVerbs+=r'|رسید|رشت|رفت|رُفت|رقصاند|رقصید|رمید|رنجاند|رنجید|رندید|رهاند|رهانید|رهید|روبید|روفت|رویاند|رویید|ریخت|رید|ریسید'
persianPastVerbs+=r'|زاد|زارید|زایید|زد|زدود|زیست|سابید|ساخت|سپارد|سپرد|سپوخت|ستاند|ستد|سترد|ستود|ستیزید|سرایید|سرشت|سرود|سرید'
persianPastVerbs+=r'|سزید|سفت|سگالید|سنجید|سوخت|سود|سوزاند|شاشید|شایست|شتافت|شد|شست|شکافت|شکست|شکفت|شکیفت|شگفت|شمارد|شمرد|شناخت'
persianPastVerbs+=r'|شناساند|شنید|شوراند|شورید|طپید|طلبید|طوفید|غارتید|غرید|غلتاند|غلتانید|غلتید|غلطاند|غلطانید|غلطید|غنود|فرستاد|فرسود|فرمود|فروخت'
persianPastVerbs+=r'|فریفت|فشاند|فشرد|فهماند|فهمید|قاپید|قبولاند|کاست|کاشت|کاوید|کرد|کشاند|کشانید|کشت|کشید|کفت|کفید|کند|کوبید|کوچید'
persianPastVerbs+=r'|کوشید|کوفت|گَزید|گُزید|گایید|گداخت|گذارد|گذاشت|گذراند|گذشت|گرازید|گرایید|گرداند|گردانید|گردید|گرفت|گروید|گریاند|گریخت|گریست'
persianPastVerbs+=r'|گزارد|گزید|گسارد|گستراند|گسترد|گسست|گسیخت|گشت|گشود|گفت|گمارد|گماشت|گنجاند|گنجانید|گنجید|گندید|گوارید|گوزید|لرزاند|لرزید'
persianPastVerbs+=r'|لغزاند|لغزید|لمباند|لمدنی|لمید|لندید|لنگید|لهید|لولید|لیسید|ماسید|مالاند|مالید|ماند|مانست|مرد|مکشید|مکید|مولید|مویید'
persianPastVerbs+=r'|نازید|نالید|نامید|نشاند|نشست|نکوهید|نگاشت|نگریست|نمایاند|نمود|نهاد|نهفت|نواخت|نوردید|نوشاند|نوشت|نوشید|نیوشید|هراسید|هشت'
persianPastVerbs+=r'|ورزید|وزاند|وزید|یارست|یازید|یافت'
persianPastVerbs+=r')'

persianPresentVerbs = r'('
persianPresentVerbs+=r'ارز|افت|افراز|افروز|افزا|افزای|افسر|افشان|افکن|انبار|انباز|انجام|انداز|اندای|اندوز|اندیش|انگار|انگیز|انگیزان'
persianPresentVerbs+=r'|اوبار|ایست|آرا|آرام|آرامان|آرای|آزار|آزما|آزمای|آسا|آسای|آشام|آشوب|آغار|آغاز|آفرین|آکن|آگن|آلا|آلای'
persianPresentVerbs+=r'|آمرز|آموز|آموزان|آمیز|آهنج|آور|آویز|آی|بار|باران|باز|باش|باف|بال|باوران|بای|باید|بخش|بخشا|بخشای'
persianPresentVerbs+=r'|بر|بَر|بُر|براز|بساو|بسیج|بلع|بند|بو|بوس|بوی|بیز|بین|پا|پاش|پاشان|پالا|پالای|پذیر|پذیران'
persianPresentVerbs+=r'|پر|پراکن|پران|پرداز|پرس|پرست|پرهیز|پرور|پروران|پز|پژمر|پژوه|پسند|پلاس|پلک|پناه|پندار|پوس|پوش|پوشان'
persianPresentVerbs+=r'|پوی|پیچ|پیچان|پیرا|پیرای|پیما|پیمای|پیوند|تاب|تابان|تاران|تاز|تازان|تپ|تپان|تراش|تراشان|تراو|ترس|ترسان'
persianPresentVerbs+=r'|ترش|ترک|ترکان|تکان|تن|توان|توپ|جنب|جنبان|جنگ|جه|جهان|جو|جوش|جوشان|جوی|چاپ|چای|چپ|چپان'
persianPresentVerbs+=r'|چر|چران|چرب|چرخ|چرخان|چسب|چسبان|چش|چشان|چک|چکان|چل|چلان|چم|چین|خار|خاران|خای|خر|خراش'
persianPresentVerbs+=r'|خراشان|خرام|خروش|خز|خست|خشک|خشکان|خل|خم|خند|خندان|خواب|خوابان|خوان|خواه|خور|خوران|خوف|خیز|خیس'
persianPresentVerbs+=r'|خیسان|دار|درخش|درخشان|درو|دزد|دم|ده|دو|دوان|دوز|دوش|ران|ربا|ربای|رخش|رس|رسان'
persianPresentVerbs+=r'|رشت|رقص|رقصان|رم|رنج|رنجان|رند|ره|رهان|رو|روب|روی|رویان|ریز|ریس|رین|زا|زار|زای|زدا'
persianPresentVerbs+=r'|زدای|زن|زی|ساب|ساز|سای|سپار|سپر|سپوز|ستا|ستان|ستر|ستیز|سر|سرا|سرای|سرشت|سز|سگال|سنب'
persianPresentVerbs+=r'|سنج|سوز|سوزان|شاش|شای|شتاب|شکاف|شکف|شکن|شکوف|شکیب|شمار|شمر|شناس|شناسان|شنو|شو|شور|شوران|شوی'
persianPresentVerbs+=r'|طپ|طلب|طوف|غارت|غر|غلت|غلتان|غلط|غلطان|غنو|فرسا|فرسای|فرست|فرما|فرمای|فروش|فریب|فشار|فشان|فشر'
persianPresentVerbs+=r'|فهم|فهمان|قاپ|قبولان|کار|کاه|کاو|کش|کَش|کُش|کِش|کشان|کف|کن|کوب|کوچ|کوش|گا|گای|گداز'
persianPresentVerbs+=r'|گذار|گذر|گذران|گرا|گراز|گرای|گرد|گردان|گرو|گری|گریان|گریز|گز|گزار|گزین|گسار|گستر|گستران|گسل|گشا'
persianPresentVerbs+=r'|گشای|گمار|گنج|گنجان|گند|گو|گوار|گوز|گوی|گیر|لرز|لرزان|لغز|لغزان|لم|لمبان|لند|لنگ|له|لول'
persianPresentVerbs+=r'|لیس|ماس|مال|مان|مک|مول|موی|میر|ناز|نال|نام|نشان|نشین|نکوه|نگار|نگر|نما|نمای|نمایان|نه'
persianPresentVerbs+=r'|نهنب|نواز|نورد|نوش|نوشان|نویس|نیوش|هراس|هست|هل|ورز|وز|وزان|یاب|یار|یاز'
persianPresentVerbs+=r')'


epithet_black_list,most_words_list,Persian_words_list,wiki_titles_list,slang_list,bad_list=[],[],[],[],[],[]
Wrong_word_list={}

def disambig_get(pagetitle):
    req = requests.get("https://fa.wikipedia.org/wiki/"+urllib.parse.quote(pagetitle))
    return req.text

def checkdisambig(htmltxt):
    disambig_list=[]
    dismbigresults=[]
    
    htmltxt=re.sub(r'<a ?[^>]+? class="mw-disambig" [^>]+?>.*?</a>',u'',htmltxt) # حذف ابهام‌زدایی از طریق الگو (دیگر کاربردها، تغییرمسیر، ...)
    a_list=htmltxt.split('<a ')
    for i in a_list:
        item=i.split('>')[0]
        if ('class="mw-disambig"' in item or 'class="mw-redirect mw-disambig"' in item) and 'title="' in item:
            item=item.split('title="')[1].split('"')[0]
            #print item
            if not item in disambig_list:
                disambig_suggest=get_page_links(redirect_find(item))
                dismbigresults.append({
                    "type": 8,
                    "word": item,
                    "cleaned_word": item,
                    "suggestions": disambig_suggest
                })
                disambig_list.append(item)
                
    return dismbigresults

def redirect_find(page_link):
    page_link=page_link.replace(' ','_')

    params = {
        'action': 'query',
        'redirects':"",
        'titles': page_link,
        "format": 'json'
    }
    try:
        return requests.post('https://fa.wikipedia.org/w/api.php', params).json()['query']['redirects'][0]['to']
    except:
        time.sleep(2)
        try:
            return requests.post('https://fa.wikipedia.org/w/api.php', params).json()['query']['redirects'][0]['to']
        except:
            return page_link
    return page_link

def get_page_links(linktitle):
    txt=''
    items=[]
    items2=[]
    links=[]
    params={
        "action": 'query',
        "prop": 'links',
        "titles": linktitle,
        "pllimit":500,
        "plnamespace":0,
        "format": 'json'
        }
    try:
        links= list(requests.post('https://fa.wikipedia.org/w/api.php', params).json()['query']['pages'].values())[0]['links']
    except:
        time.sleep(2)
        try:
            links= list(requests.post('https://fa.wikipedia.org/w/api.php', params).json()['query']['pages'].values())[0]['links']
        except:
            pass
    for i in links:
        if re.sub(r'[a-zA-Z\:]+','',i['title'])==i['title']:
            item_to_add=i['title']
            if ' ' +linktitle.replace('_',' ')+' ' in ' ' +item_to_add.replace('_',' ')+' ':
                items.append(item_to_add.strip())
                if '(' in item_to_add:
                    items.append(item_to_add+'|'+item_to_add.split('(')[0].strip())
            items2.append(item_to_add)
    if not items:
        items=items2
    return items

def convert_regex (input,new_matchs,dict):
    if '?' in input:
        Char_Index=input.find('?')
        new_match=input.replace('?','')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]

        new_match=input[0:Char_Index-1]+input[Char_Index+1:]
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]

    if re.sub(r'[یک]','',input)!= input:
        new_match=input.replace('ی','ي')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]
        new_match=input.replace('ک','ك')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]
        new_match=input.replace('ک','ك').replace('ی','ي')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]

        new_match=input.replace('ک','[کك]').replace('ی','[یي]')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]
    return new_matchs

def load_dict():
    add_regex2={}
    add_regex=[]
    global epithet_black_list,Wrong_word_list,most_words_list,Persian_words_list,wiki_titles_list,slang_list,bad_list
    epithet_black_list,most_words_list,Persian_words_list,wiki_titles_list,slang_list,bad_list=[],[],[],[],[],[]
    Wrong_word_list={}
    with open(BotAdress+'zz_bad_words.txt', 'r') as f:
        bad_list = [f.read().strip()]
    with open(BotAdress+'zz_Wrong_word_dict.txt', 'r') as f:
        fa_wrong_text = f.read()
    with open(BotAdress+'zz_slang_word_dict.txt', 'r') as f:
        fa_slang_text = f.read()
    #---wrong
    fa_wrong_text=fa_wrong_text.replace('\(','(').replace('\)',')')
    lines = fa_wrong_text.split('\n')
    for line in lines:
        if line.strip().startswith('#') or line.strip().startswith('=') or line.strip().startswith('{'):
            continue
        if line.strip().startswith('*'):#القاب
            input=line.split('||')[0].replace('*','').strip()
            add_regex=convert_regex (input,add_regex,False)
            epithet_black_list.append(input)


        if line.startswith(' ') and '||' in line:#غلط
            input2=line.split('||')[0].strip()
            Wrong_word_list[input2]=line.split('||')[1].strip()
            add_regex2=convert_regex (input2,add_regex2,Wrong_word_list)

    for i in add_regex:
        if not i in epithet_black_list:
            epithet_black_list.append(i)
    for i in add_regex2:
        if not i in Wrong_word_list:
            Wrong_word_list[i]=add_regex2[i]
    #--slang
    lines = fa_slang_text.split('\n')
    for line in lines:
            if line.strip().startswith('#') or line.strip().startswith('=') or line.strip().startswith('{'):
                continue
            if line.strip().startswith('*'):#عامیانه
                line=re.sub('^\*','',line)
                slang_list.append(line)
    with open(BotAdress+'zz_Most_word_dict.txt', 'r') as f:
        most_words = f.read()
    with open(BotAdress+'zz_users_word_dict.txt', 'r') as f:
        most_words2=f.read()
        most_words2=most_words2.replace('* ','').replace('*','').replace('\r','').strip()
    most_words = most_words+'\n'+most_words2
    most_words=most_words.replace('\r','')
    most_words_list=most_words.split('\n')
    with open(BotAdress+'zz_Persian_word_dict.txt', 'r') as f:
        Persian_words = f.read()
        Persian_words=Persian_words.replace('\r','')
        Persian_words_list=Persian_words.split('\n')
    with open(BotAdress+'zz_wiki_titles_dict.txt', 'r') as f:
        wiki_titles = f.read()
        wiki_titles=wiki_titles.replace('\r','')
        wiki_titles_list=wiki_titles.split('\n')

def find_gumeh_base(txt):
    lines=txt.split('\n')
    giumeh_place_finall,giumeh_place,min_giumeh_place=[],[],[]
    for line in lines:
        if line.count("«" )>line.count( "»" ):
            giumeh_place=re.findall(r'(?!«[^»«]+»)(«[^»«]+)',line)
            min_giumeh_place=re.findall(r'(«[^«»]+»)',line)
            for i in giumeh_place:
                if not i in min_giumeh_place:
                    if not i in giumeh_place_finall:
                        giumeh_place_finall.append(i)
        if line.count( "«" )<line.count( "»" ):
            giumeh_place=re.findall(r'([^«»]+»)',line)
            min_giumeh_place=re.findall(r'(«[^«»]+»)',line)
            for i in giumeh_place:
                if not i in min_giumeh_place:
                    if not i in giumeh_place_finall:
                        giumeh_place_finall.append(i)
    return giumeh_place_finall
    
def find_gumeh(txt):
    list=find_gumeh_base(txt)
    new_list=[]
    for i in list:
        if i[0]=="«":
            if len(i)>30:
                ourtxt=i[:29]
            else:
                ourtxt=i
            ourtxt2=re.findall(r"«(?:[^\]\[\'\<»«]+)",ourtxt)
            if ourtxt2:
                if len(ourtxt2[0])>5:
                    ourtxt=ourtxt2[0]
            new_list.append(ourtxt)
        else:
            if len(i)>30:
                ourtxt=i[-29:]
            else:
                ourtxt=i
            ourtxt2=re.findall(r"(?![\]\[\'\<»«]+)(?:[^\]\[\'\<»«]+)»",ourtxt)
            if ourtxt2:
                if len(ourtxt2[0])>5:
                    ourtxt=ourtxt2[0]
            new_list.append(ourtxt)

    return new_list

def clean_text(txt,remove_regex,faTitle):
    Syntaxs_list=[]
    Syntaxs_list2=[]
    Erab_words=[]
    giumeh_place=[]
    fa_syntax_text=re.sub(r'<(nowiki|math|code|pre|source|syntaxhighlight|blockquote)(?:[^<]|<(?!\/\1>))*?<\/\1>','',txt)
    fa_syntax_text=re.sub(r'%7B%7B','{{',fa_syntax_text)
    fa_syntax_text=re.sub(r'%7D%7D','}}',fa_syntax_text)
    fa_syntax_text=re.sub(r'\<\!\-\-(?:[^-]|-(?!->))*?\-\-\>','',fa_syntax_text)
    fa_syntax_text_old=fa_syntax_text
    fa_syntax_text=re.sub(r'\{\{\{[^\}\{]+\}\}\}','',fa_syntax_text)
    fa_syntax_text=re.sub(r'\{\{\{[^\}\{]+\}\}\}','',fa_syntax_text)
    fa_syntax_text=re.sub(r'\{\{\{[^\}\{]+\}\}\}','',fa_syntax_text)
    if fa_syntax_text_old!=fa_syntax_text:
        Syntaxs_list.append('استفاده از متغییر الگو مانند {{{ }}} در مقاله')
    if fa_syntax_text.count("{{" )> fa_syntax_text.count("}}" ):          
        Syntaxs_list.append('{{')
    if fa_syntax_text.count("{{" )< fa_syntax_text.count("}}" ):
        Syntaxs_list.append('}}')
    if fa_syntax_text.count("[[" )>fa_syntax_text.count("]]" ):
        Syntaxs_list.append('[[')
    if fa_syntax_text.count("[[" )<fa_syntax_text.count("]]" ):
        Syntaxs_list.append(']]')
    if fa_syntax_text.count("«" )>fa_syntax_text.count("»" ):
        Syntaxs_list2.append('»')
        giumeh_place.append(find_gumeh(fa_syntax_text_old))
    if fa_syntax_text.count("«" )<fa_syntax_text.count("»" ):
        Syntaxs_list2.append('«')
        giumeh_place.append(find_gumeh(fa_syntax_text_old))
    if fa_syntax_text.count("<!--" )!=fa_syntax_text.count("-->" ):
        Syntaxs_list.append('<!-- یکی از علامت‌های شروع یا پایان توضیح وجود ندارد -->')

    txt=re.sub(r'<(nowiki|math|code|pre|source|syntaxhighlight|blockquote)(?:[^<]|<(?!\/\1>))*?<\/\1>','',txt)
    txt=re.sub(r'\[\[[^\[]*?\]\]',' ',txt)
    txt=re.sub(r'\{\{(?:عربی|شروع عربی|آغاز عربی)\}\}([\s\S]*?)\{\{(?:پایان عربی)\}\}','',txt)
    txt=re.sub(r'\{\{(?:به .+?|به انگلیسی|انگلیسی|عربی|حدیث|به عربی|به اردو|اردو|lang\-[au]r)[\s\S]*?\}\}','',txt)
    txt=re.sub(r'\[\[[^\]]\]\]','',txt)
    txt=re.sub(r'[  ᠎             　]',' ',txt)
    txt=re.sub(r'\/\/.*?(?=[\s\n\|\}\]<]|$)',' ',txt)#حذف نشانی اینترنتی
    txt=re.sub(r'(\|.*?\=)',' ',txt)
    txt=re.sub(r'\[\[رده\:.*?\]\]',' ',txt)
    txt=re.sub(r'(\{\{.*?\}\})',' ',txt)
    txt=re.sub(r'(\{\{.*?\|)',' ',txt)
    txt=re.sub(r'(\<.*?\>)',' ',txt)
    txt=re.sub(r'\r','',txt)
    txt=re.sub(r"([\^\%\$\#\@\&\,\=\{\[\}\]\'\|۱۲۳۴۵۶۷۸۹۰\?\.\!؟،\:؛\"\/\\\t\'\*\+\–\-\n0-9٬٫a-zA-Z\_\ـ])+",' ',txt)
    isolated_char='ﭖﭗﭘﭙﭺﭻﭼﭽﮊﮋﮎﮏﮐﮑﻙﻚﻛﻜﮒﮓﮔﮕﮤﮥﯼﯽﯾﯿﻯﻰﻱﻲﻳﻴﺁﺁﺂﺄﺃﺃﺅﺅﺆﺇﺈﺇﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻫﻭﻮﻰﻲﻵﻶﻸﻷﻹﻺﻻﻼ'
    txt=re.sub(r'([^ ‌ء-يٓ-ٕپچژگکكڪﻙﻚیﻱﻲكﮑﮐﮏﮎﻜﻛﻚﻙىﻯيہەھﻰ-ﻴ\(\)«»'+isolated_char+'ً-ِْٰٔٔأإؤئءةٓ])+','',txt)
    txt=re.sub(r"[\s]{2,}",' ',txt)
    Erab_words_List = re.findall(r'(?=\S*[أإؤئءةًٌٍَُِْٰٓٓ])\S+\s', txt)
    if Erab_words_List:
        for Eword in Erab_words_List:
            Eword=Eword.strip()
            without_erab_word=re.sub(r"([ًٌٍَُِّْٰٓ])+",'',Eword)
            without_erab_word2=re.sub(r"([أإؤئءةٓ])+",'',without_erab_word)
            ErabNum=len(Eword)-len(without_erab_word2.strip())
            if ErabNum >2 and (not without_erab_word in Erab_words):
                Erab_words.append(without_erab_word)
    txt=re.sub(r"([ً-ِْٰٔٔ])+",'',txt)
    clean_fa_text=txt
    txt=txt.replace('»',' ').replace('«',' ')
    txt=re.sub(r"[\(\)]",' ',txt)
    txt=re.sub(r"[\s]{2,}",' ',txt)
    txt=re.sub(r'(\s)'+remove_regex+r'(\s)',' ',' '+txt+' ')
    #print txt
    txt_list=txt.strip().split(' ')
    txt_list2=txt_list
    txt_list = list(set(txt_list))

    faTitle2=re.sub(r"([\(\)\^\%\$\#\@\&\,\=\{\[\}\]\'\|۱۲۳۴۵۶۷۸۹۰\?\.\!؟»«،\:؛\"\/\\\t\'\*\+\–\-\n0-9٬٫a-zA-Z\_\ـ])+",' ',faTitle)
    faTitle_list=faTitle2.strip()+' '+faTitle.replace('‌','')+' '+faTitle.replace('‌',' ')+' '+faTitle+'‌ها'+' '+faTitle+'‌های'+' '+faTitle+'‌هایی'+' '+faTitle+'ی'+' '
    faTitle_list=faTitle_list.strip().split(' ')
    txt_list=[x for x in txt_list if x not in Erab_words]
    txt_list=[x for x in txt_list if x not in faTitle_list]
    return txt_list,clean_fa_text,Syntaxs_list,Syntaxs_list2,Erab_words,giumeh_place,txt_list2

def regex_maker(list, Correct, faText, correct_dict,my_suggestions,faTitle):
    result = []
    suggestions=[]
    for wrong_word in list:
        if correct_dict:
            suggestions = [list[wrong_word]]

        if not correct_dict and my_suggestions:
            suggestions=my_suggestions.get(wrong_word, [])
        if ' ' + wrong_word + ' ' in faText and not ' ' + wrong_word + ' ' in ' ' +faTitle+ ' ':
            clean_wrong_word=clean_word(wrong_word)
            if '|' in clean_wrong_word:
                clean_wrong_word=clean_wrong_word.split('|')[1]
            result.append({
                "type": Correct,
                "word": wrong_word,
                "cleaned_word":clean_wrong_word,
                "suggestions": suggestions
            })
    return result

def regex_maker_slang(regex_list,Correct, faText):
    result = []
    suggestions=[]
    hun_list=[]
    slang_ok=[]
    for myregex in regex_list:
        myregex = re.compile(myregex, re.MULTILINE | re.UNICODE)
        slang_results = re.findall(myregex, faText)
        if slang_results: 
            for slangs in slang_results:
                if slangs:
                    hun_list=[]
                    try:
                        slangs=slangs.strip()
                    except:
                        slangs=slangs[0]
                    if slangs in slang_ok:
                        continue
                    try:
                        if not hobj.spell(slangs):
                            hun_list=hobj.suggest(slangs)
                    except:
                        #print('some problems in hunspell')
                        pass
                    if ' ' + slangs + ' ' in faText:
                        clean_wrong_word=clean_word(slangs)
                        if '|' in clean_wrong_word:
                            clean_wrong_word=clean_wrong_word.split('|')[1]
                        slang_ok.append(slangs)
                        result.append({
                            "type": Correct,
                            "word": slangs,
                            "cleaned_word":clean_wrong_word,
                            "suggestions": hun_list
                        })
    return result,slang_ok

def clean_word(txt):
    txt2=''
    txt1=txt
    txt=re.sub(r'‌?تر(ها|ین‌?ها|ین|)(ی|)$','',txt)
    txt=re.sub(r'‌?های(م|ت|ش|مان|تان|شان)$','',txt)
    txt=re.sub(r'‌?های?ی?$','',txt)
    txt=re.sub(r'‌?(است|بود|شد|گذاری)$','',txt)
    txt=re.sub(r'‌?(ای|ام|ات|اید|اش|مان|تان|شان|گاه)$','',txt)
    if txt1==txt:
        txt=re.sub(r'‌?(یی|ست|ند)$','',txt)
    if txt1==txt:
        txt2=txt
        txt=re.sub(r'(م|ت|ش|ان|ی|یم|ید)$','',txt)
    if txt1==txt:
        txt=re.sub(r'^(نا|غیر|بی|با|در|بر|پر)‌?','',txt)
    txt=txt.strip()
    if txt2:
       txt=txt+"|"+txt2.strip()
    return txt

def get_page(title):
    txt=''
    try:
        txt= list(requests.get('https://fa.wikipedia.org/w/api.php', params={"titles": title,"action": "query", "prop": "revisions",
             "rvprop": "content", "format": "json", "rvslots": "main"}).json()['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
    except:
        time.sleep(2)
        try:
            txt= list(requests.get('https://fa.wikipedia.org/w/api.php', params={"titles": title,"action": "query", "prop": "revisions",
                 "rvprop": "content", "format": "json", "rvslots": "main"}).json()['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
        except:
            pass
    return txt

def check_grammer(faText_list,words_text_list):
    first_step_words = []
    for item in faText_list:
        if item in words_text_list:
            continue
        item2=re.sub(r'(ب|ن|م|می|نمی|)‌?'+persianPastVerbs+'(ه|)‌?(بوده?|شده?|می‌شود?|)(م|ی|یم|ید|ند|ام|ای|است|ایم|اید|اند|)','',item)
        if not item2.replace('‌','').strip():
            continue
        item2=re.sub(r'(ب|ن|م|می|نمی|)‌?'+persianPresentVerbs+r'(م|ی|یم|ید|ند|)','',item)
        if not item2.replace('‌','').strip():
            continue

        item1=clean_word(item).split('|')[0]
        if item!=item1:
            if item1 in words_text_list:
                continue
            if item1+'ن' in words_text_list:
                continue
        item1 = item.replace('‌','').strip()
        if item!=item1:
            if item1 in words_text_list:
                continue
        first_step_words.append(item)
    return first_step_words

def connected_word(pre,word,my_list):
    try:
        if word[0:len(pre)]==pre:
            my_list=[word.replace(pre,pre+' ',1)] + my_list
        if word[-len(pre):]==pre:
            my_list=[word[:-len(pre)]+' '+pre]+ my_list
    except:
        pass
    return my_list

def main(faTitle,word):
    if ('نظرخواهی' in faTitle or 'قهوه‌خانه' in faTitle or 'تابلو' in faTitle or '/' in faTitle) and 'ویکی‌پدیا:' in faTitle:
        if faTitle!='ویکی‌پدیا:اشتباه‌یاب/تست' and faTitle!='ویکی‌پدیا:اشتباه‌یاب/تمرین':
            return { "result":[],"error": "not supposed to work on RfCs" }
    if faTitle:
        try:
            faText ='\n' +get_page(faTitle)+ '\n'
            faText=faText.replace('[[ ','[[').replace('[[ ','[[').replace(' ]]',']]').replace(' ]]',']]')
            faText=faText.replace(' |','|').replace(' |','|')
            if not faText.strip():
                return { "result":[],"error": "the page couldn't be retrieved" }
        except:
            return { "result":[],"error": "the page couldn't be retrieved" }
        result = []
        remove_regex = '('+'|'.join(epithet_black_list)+'|'+'|'.join(Wrong_word_list)+')'
        faText_list,clean_fa_text,Syntaxs_list,Syntaxs_list2,Erab_words,giumeh_place,txt_list2 = clean_text(faText,remove_regex,faTitle)
        faNewText = ' ' + ' '.join(faText_list) + ' '
        clean_fa_text2=re.sub(r'«[^»]+»',' ',clean_fa_text)
        result = result + sorted(regex_maker(epithet_black_list,0,clean_fa_text2,False,{},faTitle), key=itemgetter('word'))
        result_slang,slang_ok=regex_maker_slang(slang_list,5,clean_fa_text2)
        result = result + sorted(result_slang, key=itemgetter('word'))
        result_bad,bad_ok=regex_maker_slang(bad_list,6,clean_fa_text2)
        result = result + sorted(result_bad, key=itemgetter('word'))
        clean_fa_text=clean_fa_text.replace('»',' ').replace('«',' ')
        result = result + sorted(regex_maker(Wrong_word_list,2,clean_fa_text,True,{},faTitle), key=itemgetter('word'))
        del clean_fa_text
    if word:
        result ,Syntaxs_list,Syntaxs_list2= [],[],[]
        faNewText=' '+word+' '
        faText_list=[word]
    #--------first step check --------
    first_step_words=check_grammer(faText_list,most_words_list)
    del faText_list
    #--------Second step check --------
    second_step_words=check_grammer(first_step_words,Persian_words_list)
    del first_step_words
    #--------Third step check --------

    Third_step_words=[]
    for item in second_step_words:
        if not item in wiki_titles_list:
            Third_step_words.append(item)
    del second_step_words
    for Syntaxs in Syntaxs_list:
        result= result+ [{
                "type": 3,
                "word": Syntaxs,
                "suggestions":[]
            }]
    #for Syntaxs in Syntaxs_list2:
    if giumeh_place:
        for Syntaxs in giumeh_place[0]:
            result= result+ [{
                    "type": 7,
                    "word": Syntaxs,
                    "suggestions":[]
                }]
    hun_suggest={}
    isolated_char='ﭖﭗﭘﭙﭺﭻﭼﭽﮊﮋﮎﮏﮐﮑﻙﻚﻛﻜﮒﮓﮔﮕﮤﮥﯼﯽﯾﯿﻯﻰﻱﻲﻳﻴﺁﺁﺂﺄﺃﺃﺅﺅﺆﺇﺈﺇﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻫﻭﻮﻰﻲﻵﻶﻸﻷﻹﻺﻻﻼ'
    similar_char='كﮑﮐﮏﮎﻜﻛﻚﻙىﻯيہەھﻰ'
    Fourth_step_words=Third_step_words
    Fifth_step_words=[]
    for item in Third_step_words:
        if item!=re.sub(r'['+isolated_char+similar_char+r'\u200e\u200f]','',item):
            Fifth_step_words.append(item)
            Fourth_step_words.remove(item)
    result = result + sorted(regex_maker(Fifth_step_words,4,faNewText,False,{},faTitle), key=itemgetter('word'))
    Fourth_step_words=[x for x in Fourth_step_words if x not in slang_ok]
    Fourth_step_words=[x for x in Fourth_step_words if x not in bad_ok]

    Six_step_words=[]
    for aitem in Fourth_step_words:
        if not aitem.strip():
            continue
        if txt_list2.count(aitem)>4:
            continue
        if '‌' in aitem:# if the word has zwnj
            if (not '‌‌' in aitem) and (aitem[0]!='‌') and (aitem[-1]!='‌'):
                aitemlist=aitem.split('‌')
                if check_grammer(aitemlist,most_words_list):
                    if not check_grammer(aitemlist,Persian_words_list):
                        continue
                else:
                    continue
        Six_step_words.append(aitem)
    Fourth_step_words=Six_step_words
    del Six_step_words
    try:
        for wo in Fourth_step_words:
            if not hobj.spell(wo):
                hun_list=hobj.suggest(wo)
                hun_list=connected_word('و',wo,hun_list)
                hun_list=connected_word('در',wo,hun_list)
                hun_list=connected_word('با',wo,hun_list)
                hun_list=connected_word('هم',wo,hun_list)
                hun_list=connected_word('از',wo,hun_list)
                hun_list=connected_word('که',wo,hun_list)
                hun_list=connected_word('هزار',wo,hun_list)
                hun_suggest[wo]=hun_list
            else:
                Fourth_step_words.remove(wo)
    except:
        pass
    # if a wrong word is repaeted at the article more than 2 times

    htmltxt=disambig_get(faTitle)
    result = result + checkdisambig(htmltxt)
    Finall_rexult={"result": result + sorted(regex_maker(Fourth_step_words, 1, faNewText, False,hun_suggest,faTitle), key=itemgetter('word')) ,
                  "types": {"0": { "color": '#9191ff', "title": 'القاب ممنوع', "autofix": True ,"syntax": False},
                            "1": { "color": '#ffc891', "title": 'اشتباه تایپی', "autofix": True ,"syntax": False},
                            "2": { "color": '#ff9191', "title": 'غلط املائی', "autofix": True ,"syntax": False},
                            "3": { "color": '#ff00e7', "title": 'ویکی‌کد اشتباه', "autofix": False , "syntax": True},
                            "4": { "color": '#68ff00', "title": 'نویسهٔ غیراستاندارد (نیازمند ابرابزار)', "autofix": True , "syntax": False},
                            "5": { "color": '#fff300', "title": 'عبارت غیررسمی', "autofix": True , "syntax": False},
                            "6": { "color": '#a4a4a4', "title": 'مشکوک به فحاشی', "autofix": False , "syntax": False},
                            "7": { "color": '#bafce9', "title": 'نویسهٔ « یا » ناموجود', "autofix": False , "syntax": True},
                            "8": { "color": '#fadbd8', "title": 'پیوند ابهام‌دار', "autofix": "D" , "syntax": False},
                            }
                  }
    del Third_step_words
    del Fourth_step_words
    del hun_suggest
    del faNewText
    return Finall_rexult

def run(faTitle):
    faTitle=faTitle.replace('_',' ')
    if faTitle=='Botupdate':
        fa_wrong_text=get_page('ویکی‌پدیا:اشتباه‌یاب/فهرست')
        fa_wrong_text=fa_wrong_text.replace('\r','').replace('{{/بالا}}','')
        fa_slang_text=get_page('ویکی‌پدیا:اشتباه‌یاب/فهرست/غیررسمی')
        fa_slang_text=fa_slang_text.replace('\r','').replace('{{/بالا}}','')
        fa_correct_text=get_page('ویکی‌پدیا:اشتباه‌یاب/فهرست موارد درست')
        fa_correct_text=fa_correct_text.replace('\r','').replace('{{/بالا}}','')
        with open(BotAdress+'zz_slang_word_dict.txt' ,mode = 'w') as f:
            f.write(fa_slang_text)
        with open(BotAdress+'zz_Wrong_word_dict.txt' ,mode = 'w') as f:
            f.write(fa_wrong_text)
        with open(BotAdress+'zz_users_word_dict.txt' ,mode = 'w') as f:
            f.write(fa_correct_text)
        load_dict()
        os.system('webservice2 uwsgi-python restart')
        return "Update is done"
    elif 'Word:' in faTitle or 'word:' in faTitle:
        word=faTitle.replace('Word:','').replace('word:','')
        faTitle=''
        return json.dumps(main(faTitle,word), ensure_ascii=False)
    else:
        word=''
        return json.dumps(main(faTitle,word), ensure_ascii=False)

def Open_json(OurResult,title):
    try:
        OurResult=OurResult['result']
    except:
        return ''
    list0,list1,list2,list3,list4,list5,list6,list7=[],[],[],[],[],[],[],[]
    for i in OurResult:
        if i['type']==0:
           list0.append(i['word'])
        elif i['type']==1:
           list1.append(i['word'])
        elif i['type']==2:
           list2.append(i['word'])
        elif i['type']==3:
           list3.append(i['word'])
        elif i['type']==4:
           list4.append(i['word'])
        elif i['type']==5:
           list5.append(i['word'])
        elif i['type']==6:
           list6.append(i['word'])
        elif i['type']==7:
           list7.append(i['word'])
        else:
           pass
    title_error_num=check_error_num(title)
    error_num=len(list0)+len(list1)+len(list2)+len(list3)+len(list4)+len(list5)+len(list6)+len(list7)-title_error_num
    if error_num>1:
        ourresult='* [['+title+']]  -> '+str(error_num)
        return ourresult
    else:
        return ''

def check_error_num(title):
    fatext=get_page('ویکی‌پدیا:اشتباه‌یاب/موارد درست/'+title)
    if fatext:
        return len(fatext.strip().split('\n'))
    else:
        return 0

load_dict()
if __name__ == "__main__":
    print(run(sys.argv[1]))

