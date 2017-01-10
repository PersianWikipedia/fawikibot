#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
# Distributed under the terms of the MIT license.
#
#source www/python/venv/bin/activate
#webservice2 uwsgi-python restart
# update
#python /data/project/checkdictation-fa/www/python/src/zz_checkDictation_cmd.py Botupdate
import sys

sys.path.insert(0, '/data/project/checkdictation-fa/www/python/src/compat/')
BotAdress = u'/data/project/checkdictation-fa/www/python/src/'
BotAdress_main = u'/data/project/checkdictation-fa/'
import codecs, os, json, re, io,string,time,requests,wikipedia,pagegenerators
from operator import itemgetter
try:
    import hunspell
    hobj = hunspell.HunSpell(BotAdress+'fa_IR.dic', BotAdress+'fa_IR.aff')
except:
    print "Could not import hunspell"

persianPastVerbs = ur'('
persianPastVerbs+=ur'ارزید|افتاد|افراشت|افروخت|افزود|افسرد|افشاند|افکند|انباشت|انجامید|انداخت|اندوخت|اندود|اندیشید|انگاشت|انگیخت|انگیزاند|اوباشت|ایستاد'
persianPastVerbs+=ur'|آراست|آراماند|آرامید|آرمید|آزرد|آزمود|آسود|آشامید|آشفت|آشوبید|آغازید|آغشت|آفرید|آکند|آگند|آلود|آمد|آمرزید|آموخت|آموزاند'
persianPastVerbs+=ur'|آمیخت|آهیخت|آورد|آویخت|باخت|باراند|بارید|بافت|بالید|باوراند|بایست|بخشود|بخشید|برازید|برد|برید|بست|بسود|بسیجید|بلعید'
persianPastVerbs+=ur'|بود|بوسید|بویید|بیخت|پاشاند|پاشید|پالود|پایید|پخت|پذیراند|پذیرفت|پراکند|پراند|پرداخت|پرستید|پرسید|پرهیزید|پروراند|پرورد|پرید'
persianPastVerbs+=ur'|پژمرد|پژوهید|پسندید|پلاسید|پلکید|پناهید|پنداشت|پوسید|پوشاند|پوشید|پویید|پیچاند|پیچانید|پیچید|پیراست|پیمود|پیوست|تاباند|تابید|تاخت'
persianPastVerbs+=ur'|تاراند|تازاند|تازید|تافت|تپاند|تپید|تراشاند|تراشید|تراوید|ترساند|ترسید|ترشید|ترکاند|ترکید|تکاند|تکانید|تنید|توانست|جَست|جُست'
persianPastVerbs+=ur'|جست|جنباند|جنبید|جنگید|جهاند|جهید|جوشاند|جوشید|جوید|چاپید|چایید|چپاند|چپید|چراند|چربید|چرخاند|چرخید|چرید|چسباند|چسبید'
persianPastVerbs+=ur'|چشاند|چشید|چکاند|چکید|چلاند|چلانید|چمید|چید|خاراند|خارید|خاست|خایید|خراشاند|خراشید|خرامید|خروشید|خرید|خزید|خست|خشکاند'
persianPastVerbs+=ur'|خشکید|خفت|خلید|خمید|خنداند|خندانید|خندید|خواباند|خوابانید|خوابید|خواست|خواند|خوراند|خورد|خوفید|خیساند|خیسید|داد|داشت|دانست'
persianPastVerbs+=ur'|درخشانید|درخشید|دروید|درید|درگذشت|دزدید|دمید|دواند|دوخت|دوشید|دوید|دید|دیدم|راند|ربود|رخشید|رساند|رسانید|رست|رَست|رُست'
persianPastVerbs+=ur'|رسید|رشت|رفت|رُفت|رقصاند|رقصید|رمید|رنجاند|رنجید|رندید|رهاند|رهانید|رهید|روبید|روفت|رویاند|رویید|ریخت|رید|ریسید'
persianPastVerbs+=ur'|زاد|زارید|زایید|زد|زدود|زیست|سابید|ساخت|سپارد|سپرد|سپوخت|ستاند|ستد|سترد|ستود|ستیزید|سرایید|سرشت|سرود|سرید'
persianPastVerbs+=ur'|سزید|سفت|سگالید|سنجید|سوخت|سود|سوزاند|شاشید|شایست|شتافت|شد|شست|شکافت|شکست|شکفت|شکیفت|شگفت|شمارد|شمرد|شناخت'
persianPastVerbs+=ur'|شناساند|شنید|شوراند|شورید|طپید|طلبید|طوفید|غارتید|غرید|غلتاند|غلتانید|غلتید|غلطاند|غلطانید|غلطید|غنود|فرستاد|فرسود|فرمود|فروخت'
persianPastVerbs+=ur'|فریفت|فشاند|فشرد|فهماند|فهمید|قاپید|قبولاند|کاست|کاشت|کاوید|کرد|کشاند|کشانید|کشت|کشید|کفت|کفید|کند|کوبید|کوچید'
persianPastVerbs+=ur'|کوشید|کوفت|گَزید|گُزید|گایید|گداخت|گذارد|گذاشت|گذراند|گذشت|گرازید|گرایید|گرداند|گردانید|گردید|گرفت|گروید|گریاند|گریخت|گریست'
persianPastVerbs+=ur'|گزارد|گزید|گسارد|گستراند|گسترد|گسست|گسیخت|گشت|گشود|گفت|گمارد|گماشت|گنجاند|گنجانید|گنجید|گندید|گوارید|گوزید|لرزاند|لرزید'
persianPastVerbs+=ur'|لغزاند|لغزید|لمباند|لمدنی|لمید|لندید|لنگید|لهید|لولید|لیسید|ماسید|مالاند|مالید|ماند|مانست|مرد|مکشید|مکید|مولید|مویید'
persianPastVerbs+=ur'|نازید|نالید|نامید|نشاند|نشست|نکوهید|نگاشت|نگریست|نمایاند|نمود|نهاد|نهفت|نواخت|نوردید|نوشاند|نوشت|نوشید|نیوشید|هراسید|هشت'
persianPastVerbs+=ur'|ورزید|وزاند|وزید|یارست|یازید|یافت'
persianPastVerbs+=ur')'

persianPresentVerbs = ur'('
persianPresentVerbs+=ur'ارز|افت|افراز|افروز|افزا|افزای|افسر|افشان|افکن|انبار|انباز|انجام|انداز|اندای|اندوز|اندیش|انگار|انگیز|انگیزان'
persianPresentVerbs+=ur'|اوبار|ایست|آرا|آرام|آرامان|آرای|آزار|آزما|آزمای|آسا|آسای|آشام|آشوب|آغار|آغاز|آفرین|آکن|آگن|آلا|آلای'
persianPresentVerbs+=ur'|آمرز|آموز|آموزان|آمیز|آهنج|آور|آویز|آی|بار|باران|باز|باش|باف|بال|باوران|بای|باید|بخش|بخشا|بخشای'
persianPresentVerbs+=ur'|بر|بَر|بُر|براز|بساو|بسیج|بلع|بند|بو|بوس|بوی|بیز|بین|پا|پاش|پاشان|پالا|پالای|پذیر|پذیران'
persianPresentVerbs+=ur'|پر|پراکن|پران|پرداز|پرس|پرست|پرهیز|پرور|پروران|پز|پژمر|پژوه|پسند|پلاس|پلک|پناه|پندار|پوس|پوش|پوشان'
persianPresentVerbs+=ur'|پوی|پیچ|پیچان|پیرا|پیرای|پیما|پیمای|پیوند|تاب|تابان|تاران|تاز|تازان|تپ|تپان|تراش|تراشان|تراو|ترس|ترسان'
persianPresentVerbs+=ur'|ترش|ترک|ترکان|تکان|تن|توان|توپ|جنب|جنبان|جنگ|جه|جهان|جو|جوش|جوشان|جوی|چاپ|چای|چپ|چپان'
persianPresentVerbs+=ur'|چر|چران|چرب|چرخ|چرخان|چسب|چسبان|چش|چشان|چک|چکان|چل|چلان|چم|چین|خار|خاران|خای|خر|خراش'
persianPresentVerbs+=ur'|خراشان|خرام|خروش|خز|خست|خشک|خشکان|خل|خم|خند|خندان|خواب|خوابان|خوان|خواه|خور|خوران|خوف|خیز|خیس'
persianPresentVerbs+=ur'|خیسان|دار|درخش|درخشان|درو|دزد|دم|ده|دو|دوان|دوز|دوش|ران|ربا|ربای|رخش|رس|رسان'
persianPresentVerbs+=ur'|رشت|رقص|رقصان|رم|رنج|رنجان|رند|ره|رهان|رو|روب|روی|رویان|ریز|ریس|رین|زا|زار|زای|زدا'
persianPresentVerbs+=ur'|زدای|زن|زی|ساب|ساز|سای|سپار|سپر|سپوز|ستا|ستان|ستر|ستیز|سر|سرا|سرای|سرشت|سز|سگال|سنب'
persianPresentVerbs+=ur'|سنج|سوز|سوزان|شاش|شای|شتاب|شکاف|شکف|شکن|شکوف|شکیب|شمار|شمر|شناس|شناسان|شنو|شو|شور|شوران|شوی'
persianPresentVerbs+=ur'|طپ|طلب|طوف|غارت|غر|غلت|غلتان|غلط|غلطان|غنو|فرسا|فرسای|فرست|فرما|فرمای|فروش|فریب|فشار|فشان|فشر'
persianPresentVerbs+=ur'|فهم|فهمان|قاپ|قبولان|کار|کاه|کاو|کش|کَش|کُش|کِش|کشان|کف|کن|کوب|کوچ|کوش|گا|گای|گداز'
persianPresentVerbs+=ur'|گذار|گذر|گذران|گرا|گراز|گرای|گرد|گردان|گرو|گری|گریان|گریز|گز|گزار|گزین|گسار|گستر|گستران|گسل|گشا'
persianPresentVerbs+=ur'|گشای|گمار|گنج|گنجان|گند|گو|گوار|گوز|گوی|گیر|لرز|لرزان|لغز|لغزان|لم|لمبان|لند|لنگ|له|لول'
persianPresentVerbs+=ur'|لیس|ماس|مال|مان|مک|مول|موی|میر|ناز|نال|نام|نشان|نشین|نکوه|نگار|نگر|نما|نمای|نمایان|نه'
persianPresentVerbs+=ur'|نهنب|نواز|نورد|نوش|نوشان|نویس|نیوش|هراس|هست|هل|ورز|وز|وزان|یاب|یار|یاز'
persianPresentVerbs+=ur')'


epithet_black_list,most_words_list,Persian_words_list,wiki_titles_list,slang_list,bad_list=[],[],[],[],[],[]
Wrong_word_list={}

def convert_regex (input,new_matchs,dict):
    if u'?' in input:
        Char_Index=input.find(u'?')
        new_match=input.replace(u'?',u'')
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

    if re.sub(ur'[یک]',u'',input)!= input:
        new_match=input.replace(u'ی',u'ي')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]
        new_match=input.replace(u'ک',u'ك')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]
        new_match=input.replace(u'ک',u'ك').replace(u'ی',u'ي')
        if not new_match in new_matchs:
            try:
                new_matchs.append(new_match)
            except:
                new_matchs[new_match]=dict[input]

        new_match=input.replace(u'ک',u'[کك]').replace(u'ی',u'[یي]')
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
    fa_bad_text = codecs.open(BotAdress+u'zz_bad_words.txt', 'r', 'utf8')
    bad_list = [fa_bad_text.read().strip()]
    fa_wrong_text = codecs.open(BotAdress+u'zz_Wrong_word_dict.txt', 'r', 'utf8')
    fa_wrong_text = fa_wrong_text.read()
    fa_slang_text = codecs.open(BotAdress+u'zz_slang_word_dict.txt', 'r', 'utf8')
    fa_slang_text = fa_slang_text.read()
    #---wrong
    fa_wrong_text=fa_wrong_text.replace(u'\(',u'(').replace(u'\)',u')')
    lines = fa_wrong_text.split(u'\n')
    for line in lines:
        if line.strip().startswith(u'#') or line.strip().startswith(u'=') or line.strip().startswith(u'{'):
            continue
        if line.strip().startswith(u'*'):#القاب
            input=line.split(u'||')[0].replace(u'*',u'').strip()
            add_regex=convert_regex (input,add_regex,False)
            epithet_black_list.append(input)


        if line.startswith(u' ') and u'||' in line:#غلط
            input2=line.split(u'||')[0].strip()
            Wrong_word_list[input2]=line.split(u'||')[1].strip()
            add_regex2=convert_regex (input2,add_regex2,Wrong_word_list)

    for i in add_regex:
        if not i in epithet_black_list:
            epithet_black_list.append(i)
    for i in add_regex2:
        if not i in Wrong_word_list:
            Wrong_word_list[i]=add_regex2[i]
    #--slang
    lines = fa_slang_text.split(u'\n')
    for line in lines:
            if line.strip().startswith(u'#') or line.strip().startswith(u'=') or line.strip().startswith(u'{'):
                continue
            if line.strip().startswith(u'*'):#عامیانه
                line=re.sub(u'^\*',u'',line)
                slang_list.append(line)
    most_words = codecs.open(BotAdress+u'zz_Most_word_dict.txt', 'r', 'utf8')
    most_words = most_words.read()
    most_words2 = codecs.open(BotAdress+u'zz_users_word_dict.txt', 'r', 'utf8')
    most_words2=most_words2.read()
    most_words2=most_words2.replace(u'* ',u'').replace(u'*',u'').replace(u'\r',u'').strip()
    most_words = most_words+u'\n'+most_words2
    most_words=most_words.replace(u'\r',u'')
    most_words_list=most_words.split(u'\n')
    Persian_words = codecs.open(BotAdress+u'zz_Persian_word_dict.txt', 'r', 'utf8')
    Persian_words = Persian_words.read()
    Persian_words=Persian_words.replace(u'\r',u'')
    Persian_words_list=Persian_words.split(u'\n')
    wiki_titles = codecs.open(BotAdress+u'zz_wiki_titles_dict.txt', 'r', 'utf8')
    wiki_titles = wiki_titles.read()
    wiki_titles=wiki_titles.replace(u'\r',u'')
    wiki_titles_list=wiki_titles.split(u'\n')


def clean_text(txt,remove_regex,faTitle):
    Syntaxs_list=[]
    Erab_words=[]
    fa_syntax_text=re.sub(ur'<(nowiki|math|code|pre|source|syntaxhighlight)(?:[^<]|<(?!\/\1>))*?<\/\1>',u'',txt)
    fa_syntax_text=re.sub(ur'%7B%7B',u'{{',fa_syntax_text)
    fa_syntax_text=re.sub(ur'%7D%7D',u'}}',fa_syntax_text)
    fa_syntax_text=re.sub(ur'\<\!\-\-(?:[^-]|-(?!->))*?\-\-\>',u'',fa_syntax_text)

    if string.count( fa_syntax_text,u"{{" )> string.count( fa_syntax_text,u"}}" ):
        Syntaxs_list.append(u'{{')
    if string.count( fa_syntax_text,u"{{" )< string.count( fa_syntax_text,u"}}" ):
        Syntaxs_list.append(u'}}')
    elif string.count( fa_syntax_text,u"[[" )>string.count( fa_syntax_text,u"]]" ):
        Syntaxs_list.append(u'[[')
    elif string.count( fa_syntax_text,u"[[" )<string.count( fa_syntax_text,u"]]" ):
        Syntaxs_list.append(u']]')
    elif string.count( fa_syntax_text,u"<!--" )!=string.count( fa_syntax_text,u"-->" ):
        Syntaxs_list.append(u'<!-- یکی از علامت‌های شروع یا پایان توضیح وجود ندارد -->')
    else:
        pass
    txt=re.sub(ur'<(nowiki|math|code|pre|source|syntaxhighlight)(?:[^<]|<(?!\/\1>))*?<\/\1>',u'',txt)
    txt=re.sub(ur'\[\[[^\[]*?\]\]',u' ',txt)
    txt=re.sub(ur'\{\{(?:عربی|شروع عربی|آغاز عربی)\}\}([\s\S]*?)\{\{(?:پایان عربی)\}\}',u'',txt)
    txt=re.sub(ur'\{\{(?:به .+?|به انگلیسی|انگلیسی|عربی|حدیث|به عربی|به اردو|اردو|lang\-[au]r)[\s\S]*?\}\}',u'',txt)
    txt=re.sub(ur'\[\[[^\]]\]\]',u'',txt)
    txt=re.sub(ur'[  ᠎               　]',u' ',txt)
    txt=re.sub(ur'\/\/.*?(?=[\s\n\|\}\]<]|$)',u' ',txt)#حذف نشانی اینترنتی
    txt=re.sub(ur'(\|.*?\=)',u' ',txt)
    txt=re.sub(ur'\[\[رده\:.*?\]\]',u' ',txt)
    txt=re.sub(ur'(\{\{.*?\}\})',u' ',txt)
    txt=re.sub(ur'(\{\{.*?\|)',u' ',txt)
    txt=re.sub(ur'(\<.*?\>)',u' ',txt)
    txt=re.sub(ur'\r',u'',txt)
    txt=re.sub(ur"([\^\%\$\#\@\&\,\=\{\[\}\]\'\|۱۲۳۴۵۶۷۸۹۰\?\.\!؟،\:؛\"\/\\\t\'\*\+\–\-\n0-9٬٫a-zA-Z\_\ـ])+",u' ',txt)
    isolated_char=u'ﭖﭗﭘﭙﭺﭻﭼﭽﮊﮋﮎﮏﮐﮑﻙﻚﻛﻜﮒﮓﮔﮕﮤﮥﯼﯽﯾﯿﻯﻰﻱﻲﻳﻴﺁﺁﺂﺄﺃﺃﺅﺅﺆﺇﺈﺇﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻫﻭﻮﻰﻲﻵﻶﻸﻷﻹﻺﻻﻼ'
    txt=re.sub(ur'([^ ‌ء-يٓ-ٕپچژگکكڪﻙﻚیﻱﻲكﮑﮐﮏﮎﻜﻛﻚﻙىﻯيہەھﻰ-ﻴ\(\)«»'+isolated_char+u'ً-ِْٰٔٔأإؤئءةٓ])+',u'',txt)
    txt=re.sub(ur"[\s]{2,}",u' ',txt)
    Erab_words_List = re.findall(ur'(?=\S*[أإؤئءةًٌٍَُِْٰٓٓ])\S+\s', txt)
    if Erab_words_List:
        for Eword in Erab_words_List:
            Eword=Eword.strip()
            without_erab_word=re.sub(ur"([ًٌٍَُِّْٰٓ])+",u'',Eword)
            without_erab_word2=re.sub(ur"([أإؤئءةٓ])+",u'',without_erab_word)
            ErabNum=len(Eword)-len(without_erab_word2.strip())
            if ErabNum >2 and (not without_erab_word in Erab_words):
                Erab_words.append(without_erab_word)
    txt=re.sub(ur"([ً-ِْٰٔٔ])+",u'',txt)
    clean_fa_text=txt
    txt=txt.replace(u'»',u' ').replace(u'«',u' ')
    txt=re.sub(ur"[\(\)]",u' ',txt)
    txt=re.sub(ur"[\s]{2,}",u' ',txt)
    txt=re.sub(ur'(\s)'+remove_regex+ur'(\s)',u' ',u' '+txt+u' ')
    #print txt
    txt_list=txt.strip().split(u' ')
    txt_list = list(set(txt_list))

    faTitle2=re.sub(ur"([\(\)\^\%\$\#\@\&\,\=\{\[\}\]\'\|۱۲۳۴۵۶۷۸۹۰\?\.\!؟»«،\:؛\"\/\\\t\'\*\+\–\-\n0-9٬٫a-zA-Z\_\ـ])+",u' ',faTitle)
    faTitle_list=faTitle2.strip()+u' '+faTitle.replace(u'‌',u'')+u' '+faTitle.replace(u'‌',u' ')+u' '
    faTitle_list=faTitle_list.strip().split(u' ')
    txt_list=[x for x in txt_list if x not in Erab_words]
    txt_list=[x for x in txt_list if x not in faTitle_list]
    return txt_list,clean_fa_text,Syntaxs_list,Erab_words

def regex_maker(list, Correct, faText, correct_dict,my_suggestions):
    result = []
    suggestions=[]
    for wrong_word in list:
        if correct_dict:
            suggestions = [list[wrong_word]]

        if not correct_dict and my_suggestions:
            suggestions=my_suggestions.get(wrong_word, [])
        if u' ' + wrong_word + u' ' in faText:
            clean_wrong_word=clean_word(wrong_word)
            if u'|' in clean_wrong_word:
                clean_wrong_word=clean_wrong_word.split(u'|')[1]
            result.append({
                u"type": Correct,
                u"word": wrong_word,
                u"cleaned_word":clean_wrong_word,
                u"suggestions": suggestions
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
                    hun_list2=[]
                    try:
                        slangs=slangs.strip()
                    except:
                        slangs=slangs[0]
                    if slangs in slang_ok:
                        continue
                    try:
                        if not hobj.spell(slangs):
                            hun_list=hobj.suggest(slangs)
                            for a in hun_list:
                                hun_list2.append(unicode(a,'UTF-8'))
                    except:
                        pass
                    if u' ' + slangs + u' ' in faText:
                        clean_wrong_word=clean_word(slangs)
                        if u'|' in clean_wrong_word:
                            clean_wrong_word=clean_wrong_word.split(u'|')[1]
                        slang_ok.append(slangs)
                        result.append({
                            u"type": Correct,
                            u"word": slangs,
                            u"cleaned_word":clean_wrong_word,
                            u"suggestions": hun_list2
                        })
    return result,slang_ok

def clean_word(txt):
    txt2=u''
    txt1=txt
    txt=re.sub(ur'‌?تر(ها|ین‌?ها|ین|)(ی|)$',u'',txt)
    txt=re.sub(ur'‌?های(م|ت|ش|مان|تان|شان)$',u'',txt)
    txt=re.sub(ur'‌?های?ی?$',u'',txt)
    txt=re.sub(ur'‌?(است|بود|شد|گذاری)$',u'',txt)
    txt=re.sub(ur'‌?(ای|ام|ات|اید|اش|مان|تان|شان|گاه)$',u'',txt)
    if txt1==txt:
        txt=re.sub(ur'‌?(یی|ست|ند)$',u'',txt)
    if txt1==txt:
        txt2=txt
        txt=re.sub(ur'(م|ت|ش|ان|ی|یم|ید)$',u'',txt)
    if txt1==txt:
        txt=re.sub(ur'^(نا|غیر|بی|با|در|بر|پر)‌?',u'',txt)
    txt=txt.strip()
    if txt2:
       txt=txt+u"|"+txt2.strip()
    return txt

def get_page(title):
    txt=u''
    try:
        txt= requests.get('https://fa.wikipedia.org/w/api.php', params={"titles": title,"action": "query", "prop": "revisions",
             "rvprop": "content", "format": "json"}).json()['query']['pages'].values()[0]['revisions'][0]['*']
    except:
        time.sleep(2)
        try:
            txt= requests.get('https://fa.wikipedia.org/w/api.php', params={"titles": title,"action": "query", "prop": "revisions",
                 "rvprop": "content", "format": "json"}).json()['query']['pages'].values()[0]['revisions'][0]['*']
        except:
            pass
    return txt

def check_grammer(faText_list,words_text_list):
    first_step_words = []
    for item in faText_list:
        if item in words_text_list:
            continue
        item2=re.sub(ur'(ب|ن|م|می|نمی|)‌?'+persianPastVerbs+u'(ه|)‌?(بوده?|شده?|می‌شود?|)(م|ی|یم|ید|ند|ام|ای|است|ایم|اید|اند|)',u'',item)
        if not item2.replace(u'‌',u'').strip():
            continue
        item2=re.sub(ur'(ب|ن|م|می|نمی|)‌?'+persianPresentVerbs+ur'(م|ی|یم|ید|ند|)',u'',item)
        if not item2.replace(u'‌',u'').strip():
            continue

        item1=clean_word(item).split(u'|')[0]
        if item!=item1:
            if item1 in words_text_list:
                continue
            if item1+u'ن' in words_text_list:
                continue
        item1 = item.replace(u'‌',u'').strip()
        if item!=item1:
            if item1 in words_text_list:
                continue
        first_step_words.append(item)
    return first_step_words

def connected_word(pre,word,my_list):
    try:
        if word[0:len(pre)]==pre:
            my_list=[word.replace(pre,pre+u' ',1)] + my_list
        if word[-len(pre):]==pre:
            my_list=[word[:-len(pre)]+u' '+pre]+ my_list
    except:
        pass
    return my_list

def main(faTitle,word):
    if (u'نظرخواهی' in faTitle or u'قهوه‌خانه' in faTitle or u'تابلو' in faTitle or u'/' in faTitle) and u'ویکی‌پدیا:' in faTitle:
        if faTitle!=u'ویکی‌پدیا:اشتباه‌یاب/تست' and faTitle!=u'ویکی‌پدیا:اشتباه‌یاب/تمرین':
            return { "error": "not supposed to work on RfCs" }
    if faTitle:
        try:
            faText =u'\n' +get_page(faTitle)+ u'\n'
            if not faText.strip():
                return { "error": "the page couldn't be retrieved" }
        except:
            return { "error": "the page couldn't be retrieved" }
        result = []
        remove_regex = u'('+u'|'.join(epithet_black_list)+u'|'+u'|'.join(Wrong_word_list)+u')'
        faText_list,clean_fa_text,Syntaxs_list,Erab_words = clean_text(faText,remove_regex,faTitle)
        faNewText = u' ' + u' '.join(faText_list) + u' '
        clean_fa_text2=re.sub(ur'«[^»]+»',u' ',clean_fa_text)
        result = result + sorted(regex_maker(epithet_black_list,0,clean_fa_text2,False,{}), key=itemgetter('word'))
        result_slang,slang_ok=regex_maker_slang(slang_list,5,clean_fa_text2)
        result = result + sorted(result_slang, key=itemgetter('word'))
        result_bad,bad_ok=regex_maker_slang(bad_list,6,clean_fa_text2)
        result = result + sorted(result_bad, key=itemgetter('word'))
        clean_fa_text=clean_fa_text.replace(u'»',u' ').replace(u'«',u' ')
        result = result + sorted(regex_maker(Wrong_word_list,2,clean_fa_text,True,{}), key=itemgetter('word'))
        del clean_fa_text
    if word:
        result ,Syntaxs_list= [],[]
        faNewText=u' '+word+u' '
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
                u"type": 3,
                u"word": Syntaxs,
                u"suggestions":[]
            }]
    hun_suggest={}
    isolated_char=u'ﭖﭗﭘﭙﭺﭻﭼﭽﮊﮋﮎﮏﮐﮑﻙﻚﻛﻜﮒﮓﮔﮕﮤﮥﯼﯽﯾﯿﻯﻰﻱﻲﻳﻴﺁﺁﺂﺄﺃﺃﺅﺅﺆﺇﺈﺇﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻫﻭﻮﻰﻲﻵﻶﻸﻷﻹﻺﻻﻼ'
    similar_char=u'كﮑﮐﮏﮎﻜﻛﻚﻙىﻯيہەھﻰ'
    Fourth_step_words=Third_step_words
    Fifth_step_words=[]
    for item in Third_step_words:
        if item!=re.sub(ur'['+isolated_char+similar_char+ur'\u200e\u200f]',u'',item):
            Fifth_step_words.append(item)
            Fourth_step_words.remove(item)
    result = result + sorted(regex_maker(Fifth_step_words,4,faNewText,False,{}), key=itemgetter('word'))
    Fourth_step_words=[x for x in Fourth_step_words if x not in slang_ok]
    Fourth_step_words=[x for x in Fourth_step_words if x not in bad_ok]
    try:
        for wo in Fourth_step_words:
            if not hobj.spell(wo):
                hun_list=hobj.suggest(wo)
                hun_list2=[]
                for a in hun_list:
                    hun_list2.append(unicode(a,'UTF-8'))
                hun_list2=connected_word(u'و',wo,hun_list2)
                hun_list2=connected_word(u'در',wo,hun_list2)
                hun_list2=connected_word(u'با',wo,hun_list2)
                hun_list2=connected_word(u'هم',wo,hun_list2)
                hun_list2=connected_word(u'از',wo,hun_list2)
                hun_list2=connected_word(u'که',wo,hun_list2)
                hun_list2=connected_word(u'هزار',wo,hun_list2)
                hun_suggest[wo]=hun_list2
            else:
                Fourth_step_words.remove(wo)
    except:
        pass
    Finall_rexult={u"result": result + sorted(regex_maker(Fourth_step_words, 1, faNewText, False,hun_suggest), key=itemgetter('word')) ,
                  u"types": {u"0": { u"color": u'#9191ff', u"title": u'القاب ممنوع', u"autofix": True ,u"syntax": False},
                            u"1": { u"color": u'#ffc891', u"title": u'اشتباه تایپی', u"autofix": True ,u"syntax": False},
                            u"2": { u"color": u'#ff9191', u"title": u'غلط املائی', u"autofix": True ,u"syntax": False},
                            u"3": { u"color": u'#ff00e7', u"title": u'ویکی‌کد اشتباه', u"autofix": False , u"syntax": True},
                            u"4": { u"color": u'#68ff00', u"title": u'نویسهٔ غیراستاندارد (نیازمند ابرابزار)', u"autofix": True , u"syntax": False},
                            u"5": { u"color": u'#fff300', u"title": u'عبارت غیررسمی', u"autofix": True , u"syntax": False},
                            u"6": { u"color": u'#a4a4a4', u"title": u'مشکوک به فحاشی', u"autofix": False , u"syntax": False},
                            }
                  }
    del Third_step_words
    del Fourth_step_words
    del hun_suggest
    del faNewText
    return Finall_rexult

def run(faTitle):
    faTitle=faTitle.replace(u'_',u' ')
    if faTitle==u'Botupdate':
        fa_wrong_text=get_page(u'ویکی‌پدیا:اشتباه‌یاب/فهرست')
        fa_wrong_text=fa_wrong_text.replace(u'\r',u'').replace(u'{{/بالا}}',u'')
        fa_slang_text=get_page(u'ویکی‌پدیا:اشتباه‌یاب/فهرست/غیررسمی')
        fa_slang_text=fa_slang_text.replace(u'\r',u'').replace(u'{{/بالا}}',u'')
        fa_correct_text=get_page(u'ویکی‌پدیا:اشتباه‌یاب/فهرست موارد درست')
        fa_correct_text=fa_correct_text.replace(u'\r',u'').replace(u'{{/بالا}}',u'')
        with codecs.open(BotAdress+u'zz_slang_word_dict.txt' ,mode = 'w',encoding = 'utf8' ) as f:
            f.write(fa_slang_text)
        with codecs.open(BotAdress+u'zz_Wrong_word_dict.txt' ,mode = 'w',encoding = 'utf8' ) as f:
            f.write(fa_wrong_text)
        with codecs.open(BotAdress+u'zz_users_word_dict.txt' ,mode = 'w',encoding = 'utf8' ) as f:
            f.write(fa_correct_text)
        load_dict()
        os.system('webservice2 uwsgi-python restart')
        return u"Update is done"
    elif u'Word:' in faTitle or u'word:' in faTitle:
        word=faTitle.replace(u'Word:',u'').replace(u'word:',u'')
        faTitle=u''
        return json.dumps(main(faTitle,word), ensure_ascii=False)
    else:
        word=u''
        return json.dumps(main(faTitle,word), ensure_ascii=False)

def Open_json(OurResult,title):
    OurResult=OurResult['result']
    list0,list1,list2,list3,list4,list5,list6=[],[],[],[],[],[],[]
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
        else:
           pass
    ourresult=u'-'.join(list0)+u'\t'+u'-'.join(list1)+u'\t'+u'-'.join(list2)+u'\t'+u'-'.join(list3)+u'\t'+u'-'.join(list4)+u'\t'+u'-'.join(list5)+u'\t'+u'-'.join(list6)
    if len(list0)+len(list1)+len(list2)+len(list3)+len(list4)+len(list5)+len(list6)>0:
        ourresult=str(len(list0)+len(list1)+len(list2)+len(list3)+len(list4)+len(list5)+len(list6))+u'\t\t'+str(len(list0))+u'\t'+str(len(list1))+u'\t'+str(len(list2))+u'\t'+str(len(list3))+u'\t'+str(len(list4))+u'\t'+str(len(list5))+u'\t'+str(len(list6))+u'\t@\t'+ourresult
        ourresult=u'*'+title+u'\t'+ourresult
        return ourresult
    else:
        return u''

def Manual_main():
    wikipedia.config.put_throttle = 0
    wikipedia.put_throttle.setDelay()
    gen= None
    word=u''
    PageTitles = []
    genFactory = pagegenerators.GeneratorFactory()
    for arg in wikipedia.handleArgs():
        if arg.startswith( '-page' ):
            PageTitles.append( arg[6:] )
            break
        else:
            generator = genFactory.handleArg( arg )
            if generator:
                gen = generator
    if PageTitles:
        pages = [wikipedia.Page(wikipedia.getSite(),PageTitle) for PageTitle in PageTitles]
        gen = iter( pages )
    if not gen:
        wikipedia.stopme()    
        sys.exit()
    preloadingGen = pagegenerators.PreloadingGenerator(gen,pageNumber = 60)
    for faTitle in preloadingGen:
        wikipedia.output(u'---'+faTitle.title()+u'-----')
        OurResult=main(faTitle.title(),word)
        OurResult=Open_json(OurResult,faTitle.title())
        if OurResult.strip():
            wikipedia.output(OurResult)
            with codecs.open(BotAdress_main+u'zz_most_miss_result.txt' ,mode = 'a',encoding = 'utf8' ) as f:
                f.write(OurResult.strip()+u'\n')
            with codecs.open(BotAdress_main+u'zz_most_miss_result_number.txt' ,mode = 'a',encoding = 'utf8' ) as f:
                f.write(OurResult.split(u'@')[0].strip()+u'\n')

load_dict()
if __name__ == "__main__":
    if '-' in sys.argv[1]:
        Manual_main()
    else:
        print run(unicode(sys.argv[1], 'utf-8'))
