import requests
import re
import json
import csv
import time
import random
import pandas as pd
import traceback
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

fake_ua = UserAgent()
headers = {
    'user-agent':fake_ua.random,
    'cookie': '__cfduid=d813dceed2b4f1201371108fba98bdced1599533490; EUID=c4cc9ca1-6368-4e1a-bb75-fa7572a5f785; has_multiple_organizations=false; id_ab=B:100:8:701c76df-1da8-4a1a-88a2-92513e657af6; utt=f405266b88b64710d9cb904e6534597aaf6dd90; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; __gads=ID=aed21115087b2085:T=1599533496:S=ALNI_MbA50dE0pw_wymipQOzAZ9OlBssbw; mboxes=%5B%7B%22index%22%3A0%2C%22name%22%3A%22article-page-view-only-pdf-server-side-mbox%22%7D%5D; usbls=1; fingerPrintToken=97ac2b8cf0e2f1dd3e4ccab725803e63; sd_session_id=ee3ac9602f214445a03b2ca6c93c1c88844bgxrqa; acw=ee3ac9602f214445a03b2ca6c93c1c88844bgxrqa%7C%24%7CB3F0F3F608F8D01C5C1E016B4C654CEE7554AAE072749DAF85D85A7D0A5C216742637C2A224F20C0BD897E56E275B8FCA75652AE48A06CF13FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; ANONRA_COOKIE=3BF848533EB21B1AAD335803E309E2FC570004E8A67F04B7CF27F8C8E76F26450E2C12DC06BE0D89B7FBF85D00729F5495FC7ADA35E78036; SD_ART_LINK_STATE=%3Ce%3E%3Cq%3Escience%3C%2Fq%3E%3Corg%3Ejrnl_archive%3C%2Forg%3E%3Cz%3Erslt_list_item%3C%2Fz%3E%3Crdt%3E2020%2F09%2F11%2F01%3A25%3A32%3A609%3C%2Frdt%3E%3Cenc%3EN%3C%2Fenc%3E%3C%2Fe%3E; mbox=session%2373b2a177f9f648f0b377e333286a2d5e%231599792987%7CPC%23111599787533312-97508.34_0%231663035927; MIAMISESSION=6b567d5f-7145-4d2f-b072-54053f66490a:3777255400; SD_REMOTEACCESS=eyJhY2NvdW50SWQiOiI1MzU1MiIsImRlcHRJZCI6Ijc1NjM3IiwidGltZXN0YW1wIjoxNTk5ODAyNjAwOTI1fQ==; s_pers=%20v8%3D1599802606734%7C1694410606734%3B%20v8_s%3DFirst%2520Visit%7C1599804406734%3B%20c19%3Dsd%253Abrowse%253Ajournal%253Aarchive%7C1599804406798%3B%20v68%3D1599802605330%7C1599804406861%3B; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=870038026%7CMCIDTS%7C18517%7CMCMID%7C49729833905657570613356864807633985798%7CMCAAMLH-1600407407%7C11%7CMCAAMB-1600407407%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1599809807s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1134298126%7CvVersion%7C5.0.0; s_sess=%20e41%3D1%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsd%25253Asearch%25253Aresults%25253Acustomer%25253Aanon%252C13%252C13%252C599%252C1280%252C599%252C1280%252C800%252C2%252CP%3B%20s_ppv%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C5%252C5%252C605%252C1280%252C599%252C1280%252C800%252C2%252CP%3B'
    }

none_file_name = []

def read_file_names():
    file_names = []
    file_name_list = pd.read_csv('./all_journal.csv')['0']
    for file_name in file_name_list:
        file_name = file_name.replace(' ','-').strip()
        file_names.append(file_name)
    return file_names

def get_volume(file_name):
    global none_file_name
    try:
        print('Loding {} now!'.format(file_name))
        dom = requests.get('https://www.sciencedirect.com/journal/{}/issues'.format(file_name),headers = headers).text
        soup = BeautifulSoup(dom,'lxml')
        ajax = soup.find('div', class_='js-ad-banner').find('script').get_text()
        pattern = r""".*?defineSlot\('.*?/ISSN(\d+)'"""
        pattern = re.compile(pattern, re.S)
        m = pattern.match(dom).group(1)
        volume = 'https://www.sciencedirect.com/journal/{}/year/2020/issues'.format(m)
        print(volume)
        journal_urls = get_journal_url(file_name,volume)
        with open('./Done_File_name.csv','a') as Done_file:
            Done_file.write('{}/n'.format(file_name))
            Done_file.close()
        return journal_urls
    except:
        print('{} not in volume!'.format(file_name))
        none_file_name.append(file_name)
        with open('./none_file_name.csv','a') as f:
            f.write(file_name)
            f.close()

def get_journal_url(file_name,volume):
    journal_urls = []
    volume_url = requests.get(volume,headers = headers).json()
    time.sleep(random.randint(3,4))
    for uriLookup in volume_url['data']:
        url = './journal/{}'.format(file_name) + uriLookup['uriLookup']
        journal_urls.append(url)
    print(journal_urls)
    return journal_urls

def get_volume_urls(journal_urls):  # 需要修改
    volume_urls = journal_urls 
    return volume_urls
    
def get_article_urls(volume_urls):
    global headers
    article_urls = []
    for url in volume_urls:
        resp = requests.get(url,headers = headers).text
        soup = BeautifulSoup(resp,'lxml')
        article_url = ['https://www.sciencedirect.com' + i.attrs['href'] for i in soup.find_all('a',class_="anchor article-content-title u-margin-xs-top u-margin-s-bottom")]
        article_urls.extend(article_url)
#         time.sleep(random.randint(0,1))
    print('url loading done !')
    return article_urls

def article_urls_Craw(article_urls):
    print('start Craw')
    global headers
    refs = []
    for url in article_urls:
        try:
            resp_dic = {

            }
            article_url = requests.get(url,headers = headers).text
            article_dom = BeautifulSoup(article_url,'lxml')
            title_dom = article_dom.find('span',class_="title-text").get_text()
            author_list = article_dom.find_all('a',class_="author size-m workspace-trigger")
            author_lists = []
            for author in author_list:
                author = author.find('span',class_="content")
                author_xing = author.find('span',class_="text given-name").get_text()
                author_name = author.find('span',class_="text surname").get_text()
                author_full_name = author_xing + author_name
                author_lists.append(author_full_name)
            author_dom = ','.join(author_lists)
            reference_dict,title_id = reference_Process(url)
            resp_dic['title'] = title_dom
            resp_dic['author'] = author_lists
            resp_dic['title_id'] = title_id
            print(title_dom)
            print(title_id)
            refs.append(resp_dic)
            time.sleep(random.randint(1,2))
            with open ('/users/heshuwen/desktop/JCR_JOURNAL/every_article_reference/{}.json'.format(title_id),'w') as reference_file:
                 json.dump(reference_dict,reference_file)
            print('Craw done!')
        except:
            traceback.print_exc()
    return refs
    
def reference_Process(article_url):
    global headers
    try:
        resps = requests.get(article_url,headers = headers)
        print(resps.status_code)
        resp = resps.text
        reference_dom = BeautifulSoup(resp,'lxml')
        title_id = reference_dom.find('meta').attrs['content']
        token = reference_dom.find('script',type = "application/json").get_text()
        entitledToken = dom['article']['entitledToken']
        reference_url = 'https://www.sciencedirect.com/sdfe/arp/pii/' + title_id + '/references?entitledToken=' + entitledToken
        reference_dict = json.loads(requests.get(reference_url,headers = headers).text)
        return reference_dict,title_id
    except:
        print('none')

def save_json_file(refs,file_name):
    print('start saving_data')
    with open ('/users/heshuwen/desktop/JCR_JOURNAL/paper_name/{}.json'.format(file_name),'w') as f:
        json.dump(refs,f) 
    print('saving done')

if __name__ == "__main__":    
    file_names = read_file_names()
    for file_name in file_names:
        journal_urls = get_volume(file_name)
        try:
            volume_urls = get_volume_urls(journal_urls)
            article_urls = get_article_urls(volume_urls)
            refs = article_urls_Craw(article_urls)
            save_json_file(refs,file_name)
        except:
            continue
            