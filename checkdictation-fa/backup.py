#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza(User:reza1615), 2011
#
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/data/project/checkdictation-fa/www/python/src/compat/')


import codecs,os,json,re,io
import query
import wikipedia
from datetime import timedelta,datetime
faSite = wikipedia.getSite('fa')
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
BotAdress=u'/data/project/checkdictation-fa/www/python/src/'
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

add_regex,add_regex2=[],{}
epithet_black_list=[]
Wrong_word_list={}
Json_data={}
fa_wrong_text = codecs.open(BotAdress+u'zz_Wrong_word_dict.txt', 'r', 'utf8')
fa_wrong_text = fa_wrong_text.read()
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

most_words = codecs.open(BotAdress+u'zz_Most_word_dict.txt', 'r', 'utf8')
most_words = most_words.read()
most_words2 = codecs.open(BotAdress+u'zz_users_word_dict.txt', 'r', 'utf8')
most_words2=most_words2.read()
most_words4=most_words2.replace(u'* ',u'').replace(u'*',u'').replace(u'\r',u'').strip()
most_words3 = most_words+u'\n'+most_words4
most_words_list=most_words3.split(u'\n')
Persian_words = codecs.open(BotAdress+u'zz_Persian_word_dict.txt', 'r', 'utf8')
Persian_words = Persian_words.read()
Persian_words_list=Persian_words.split(u'\n')
wiki_titles = codecs.open(BotAdress+u'zz_wiki_titles_dict.txt', 'r', 'utf8')
wiki_titles = wiki_titles.read()
wiki_titles_list=wiki_titles.split(u'\n')



def clean_text(txt,remove_regex):
    txt=re.sub(ur'(\|.*?\=)',u' ',txt)
    txt=re.sub(ur'\[\[رده\:.*?\]\]',u' ',txt)
    txt=re.sub(ur'(\{\{.*?\}\})',u' ',txt)
    txt=re.sub(ur'(\{\{.*?\|)',u' ',txt)
    txt=re.sub(ur'(\<.*?\>)',u' ',txt)
    txt=re.sub(ur"([\^\%\$\#\@\&\,\=\{\[\}\]\'\|۱۲۳۴۵۶۷۸۹۰\?\.\!؟»«،\:؛\(\)\"\/\\\t\'\*\+\–\-\r\n0-9٬٫a-zA-Z\_\ـ])+",u' ',txt)
    txt=re.sub(ur"([ً-ِْٰٔٔ])+",u'',txt)
    txt=re.sub(ur'([^ ‌ء-يٓ-ٕپچژگکكڪﻙﻚیﻱﻲكﮑﮐﮏﮎﻜﻛﻚﻙىﻯيہەھﻰ-ﻴ])+',u'',txt)
    txt=re.sub(ur"[\s]+",u' ',txt)
    txt=re.sub(ur'(\s)'+remove_regex+ur'(\s)',u' ',u' '+txt+u' ')
    txt_list=txt.strip().split(u' ')
    txt_list = list(set(txt_list))
    return txt_list

def regex_maker(list, Correct, faText, correct_dict):
    result = []

    for wrong_word in list:
        if correct_dict:
            Correct = list[wrong_word]

        if u' ' + wrong_word + u' ' in faText:
            result.append([wrong_word, Correct])

    return result

def get_page_id(faTitle):
    faTitle = faTitle.replace(u' ',u'_')
    params = {
        'action': 'query',
        'prop': 'info',
        'titles': faTitle,
    }
    LastRevesion = query.GetData(params,faSite)
    try:
        for Item in LastRevesion[u'query'][u'pages']:
            last_id=LastRevesion[u'query'][u'pages'][Item]['lastrevid']
    except:
        last_id=False
    return str(last_id)

def check_word(case,item,list):
    case_len=len(case)
    if case==item[-case_len:]:
        if item[:-case_len] in list:
            return True
        if item[-case_len-1] ==u'‌':
            if item[:-case_len-1] in list:
                return True
    return False


def main(faTitle):

    if u'نظرخواهی' in faTitle and u'ویکی‌پدیا:' in ffaTitle:
        return { "error": "not supposed to work on RfCs" }

    fapage = wikipedia.Page(faSite,faTitle)

    try:
        faText = u'\n' + fapage.get() + u'\n'
    except:
        return { "error": "the page couldn't be retrieved" }

    result = []

    Correct = u'0'
    result = result + regex_maker(epithet_black_list,Correct,faText,False)

    Correct = u'2'
    result = result + regex_maker(Wrong_word_list,Correct,faText,True)

    #--------first step check --------
    remove_regex = u'('+u'|'.join(epithet_black_list)+u'|'+u'|'.join(Wrong_word_list)+u')'
    faText_list = clean_text(faText,remove_regex)
    faNewText = u' ' + u' '.join(faText_list) + u' '
    first_step_words = []

    for item in faText_list:
        if not item in most_words_list:
            if len(item)>5:
                if check_word(u'هایی',item,most_words_list):
                    continue
            if len(item)>4:
                if check_word(u'ها',item,most_words_list):
                    continue
                elif check_word(u'های',item,most_words_list):
                    continue
                elif check_word(u'ام',item,most_words_list):
                    continue
                elif check_word(u'ای',item,most_words_list):
                    continue
                elif check_word(u'است',item,most_words_list):
                    continue
                elif check_word(u'ایم',item,most_words_list):
                    continue
                elif check_word(u'اید',item,most_words_list):
                    continue
                elif check_word(u'اند',item,most_words_list):
                    continue
                elif check_word(u'ات',item,most_words_list):
                    continue
                elif check_word(u'اش',item,most_words_list):
                    continue
                elif check_word(u'مان',item,most_words_list):
                    continue
                elif check_word(u'تان',item,most_words_list):
                    continue
                elif check_word(u'شان',item,most_words_list):
                    continue
                elif check_word(u'ترین',item,most_words_list):
                    continue
                elif check_word(u'تری',item,most_words_list):
                    continue
                elif check_word(u'تر',item,most_words_list):
                    continue
                elif u'م' ==item[-1:]:
                    if item[:-1] in most_words_list:
                        continue
                elif u'ت' ==item[-1:]:
                    if item[:-1] in most_words_list:
                        continue
                elif u'ش' ==item[-1:]:
                    if item[:-1] in most_words_list:
                        continue
                elif u'ی' ==item[-1:]:
                    if item[:-1] in most_words_list:
                        continue
                elif u'غیر' ==item[:3]:
                    if item[3:] in most_words_list:
                        continue
                elif u'‌' in item:
                    if item.replace(u'‌',u'') in most_words_list:
                        continue
                else:
                    pass
            first_step_words.append(item)
    del faText_list
    #--------Second step check --------
    second_step_words=[]

    for item in first_step_words:
        if not item in Persian_words_list:
            second_step_words.append(item)
    del first_step_words
    #--------Third step check --------
    Third_step_words=[]

    for item in second_step_words:
        if not item in wiki_titles_list:
            Third_step_words.append(item)
    del second_step_words

    Correct = u'1'
    return { "result": result + regex_maker(Third_step_words, Correct, faNewText, False) }

def Write_json(faTitle,Finall_result,json_dict):#,page_new_id):
    now = str(datetime.now())
    todaynum=int(now.split('-')[2].split(' ')[0])+int(now.split('-')[1])*30+(int(now.split('-')[0])-2000)*365
    try:
       thedate=json_dict['date']
    except:
       thedate=todaynum+20
    if thedate-todaynum>5:
       del json_dict
       json_dict={}
    mytext={}
    mytext['text']=Finall_result
    #mytext['page_id']=page_new_id
    json_dict['date']=todaynum
    json_dict[faTitle]=mytext
    return json_dict

def run(faTitle):
    if faTitle==u'Botupdate':
        fa_wrong_page=wikipedia.Page(faSite,u'ویکی‌پدیا:اشتباه‌یاب/فهرست.py')
        fa_wrong_text=fa_wrong_page.get().replace(u'\r',u'')
        fa_correct_page=wikipedia.Page(faSite,u'ویکی‌پدیا:اشتباه‌یاب/فهرست موارد درست')
        fa_correct_text=fa_correct_page.get().replace(u'\r',u'').replace(u'{{/بالا}}',u'')

        with codecs.open(BotAdress+u'zz_Wrong_word_dict.txt' ,mode = 'w',encoding = 'utf8' ) as f:
            f.write(fa_wrong_text)
        with codecs.open(BotAdress+u'zz_users_word_dict.txt' ,mode = 'w',encoding = 'utf8' ) as f:
            f.write(fa_correct_text)
        os.system('cd www/python/src/')   
        os.system('webservice2 uwsgi-python restart')
        return u"Update is done"

    return json.dumps(main(faTitle))

    '''
    Cash_result=False

    global Json_data

    #page_new_id=get_page_id(faTitle)
    try:
       thedate = Json_data['date']
       #page_old_id=Json_data[faTitle]['page_id']
    except:
       page_old_id = u'0'

    if faTitle in Json_data:# and page_old_id== page_new_id:
        Cash_result=Json_data[faTitle]['text']

    if not Cash_result:
        Finall_result=main(faTitle)
        Json_data=Write_json(faTitle,Finall_result,Json_data)#,page_new_id)
    else:
        Finall_result=Cash_result
    '''

if __name__ == "__main__":
    print run(unicode(sys.argv[1], 'utf-8'))
