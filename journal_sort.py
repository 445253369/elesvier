import requests
import re
import json
import csv
import time
import random
import pandas as pd
import traceback
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

fake_ua = UserAgent()
headers = {
    'user-agent':fake_ua.random,
    'cookie': '__cfduid=d2afa7f1035d916db0b708a8014d6c8fa1600082676; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; EUID=a529e567-93ab-4325-b768-0abffe18b692; sd_session_id=d737f67420e48740c349b915f3165a5cd4e6gxrqa; acw=d737f67420e48740c349b915f3165a5cd4e6gxrqa%7C%24%7C245E82DB4CC768B934936AC3875200ECB24AAE84B80E512223A8B61327E618F5D67040EF7BFE6E7CAF62716414061E78C859D9078BAB5BA13FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; ANONRA_COOKIE=32FA2161BE824893CC3DDD13F8DE786648DD2AE58629212429064AFADDF6B0734B5EACC68AA78C0DF6A182DAF74C7C401E6C06CC4A93E5EB; has_multiple_organizations=false; MIAMISESSION=a705ab9b-879f-47f8-85ad-ee4a4c344f04:3777535512; SD_REMOTEACCESS=eyJhY2NvdW50SWQiOiI1MzU1MiIsImRlcHRJZCI6Ijc1NjM3IiwidGltZXN0YW1wIjoxNjAwMDgyNzEyMTM2fQ==; id_ab=B:100:8:b8c02ff9-796a-4c8d-9012-24f8e96e2b7f; utt=ea117d5fd4c847150ac6db37b01a308f543397e; fingerPrintToken=97ac2b8cf0e2f1dd3e4ccab725803e63; s_pers=%20c19%3Dsd%253Abrowse%253Ajournal%253Aissue%7C1600084516463%3B%20v68%3D1600082716021%7C1600084516492%3B%20v8%3D1600082716517%7C1694690716517%3B%20v8_s%3DFirst%2520Visit%7C1600084516517%3B; __gads=ID=5629c79b276c2cee-22dbe5c57ec300c6:T=1600082716:S=ALNI_MaDYdThGcUBjzuptcT6pbgjg7r9uA; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=870038026%7CMCIDTS%7C18520%7CMCMID%7C49729833905657570613356864807633985798%7CMCAAMLH-1600687517%7C11%7CMCAAMB-1600687517%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1600089917s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.0%7CMCCIDH%7C1134298126; s_sess=%20s_ppvl%3D%3B%20e41%3D1%3B%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Abrowse%25253Ajournal%25253Aissue%252C19%252C11%252C1175%252C1280%252C204%252C1280%252C800%252C2%252CP%3B'
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
    global none_file_name,headers
    try:
        print('Loading {} now!'.format(file_name))
        dom = requests.get('https://www.sciencedirect.com/journal/{}/issues'.format(file_name),headers = headers,timeout = 20).text
        soup = BeautifulSoup(dom,'lxml')
        # ajax = soup.find('div', class_='js-ad-banner').find('script').get_text()
        # pattern = r""".*?defineSlot\('.*?/ISSN(\d+)'"""
        # pattern = re.compile(pattern, re.S)
        # ISSN = pattern.match(dom).group(1)
        ISSN = soup.find('p',class_ = "u-margin-xs-bottom text-s u-display-block js-issn").string
        ISSN = ISSN.replace('ISSN:','').replace('-','').strip()
        print(ISSN)
        volume = 'https://www.sciencedirect.com/journal/{}/year/2020/issues'.format(ISSN)
        journal_urls = get_journal_url(file_name,volume)
        with open('./Done_File_name.csv','a') as Done_file:
            Done_file.write('{}\n'.format(file_name))
            Done_file.close()
        return journal_urls
    except:
        print('{} not in volume!'.format(file_name))
        none_file_name.append(file_name)
        with open('./none_file_name.csv','a') as f:
            f.write('{}\n'.format(file_name))
            f.close()

def get_journal_url(file_name,volume):
    journal_urls = []
    volume_url = requests.get(volume,headers = headers,timeout = 20).json()
    time.sleep(random.randint(3,4))
    for uriLookup in volume_url['data']:
        url = 'https://www.sciencedirect.com/journal/{}'.format(file_name) + uriLookup['uriLookup']
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
        resp = requests.get(url,headers = headers,timeout = 20).text
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
            article_url = requests.get(url,headers = headers,timeout = 20).text
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
            reference_dict = json.dumps(reference_dict)
            resp_dic['title'] = title_dom
            resp_dic['author'] = author_lists
            resp_dic['title_id'] = title_id
            print(title_dom)
            print(title_id)
            refs.append(resp_dic)
            time.sleep(random.randint(3,4))
            with open ('./every_article_reference/{}.json'.format(title_id),'w',encoding='utf-8') as reference_file:
                json.dump(reference_dict,reference_file)
            print('Craw done!')
        except:
            traceback.print_exc()
    return refs
    
def reference_Process(article_url):
    global headers
    try:
        resps = requests.get(article_url,headers = headers,timeout = 20)
        print(resps.status_code)
        resp = resps.text
        reference_dom = BeautifulSoup(resp,'lxml')
        title_id = reference_dom.find("meta").attrs["content"]
        print(title_id)
        token = reference_dom.find('script',type="application/json").string
        pattern = r'''.*?entitledToken":"(.*?)",".*?'''
        pattern = re.compile(pattern, re.S)
        ISSN = pattern.match(token).group(1)
        print(ISSN)
        reference_url = 'https://www.sciencedirect.com/sdfe/arp/pii/' + title_id + '/references?entitledToken=' + ISSN
        reference_dict = requests.get(reference_url,headers = headers,timeout = 20).text
        print(reference_dict)
        print(title_id)
        return reference_dict,title_id
    except:
        print('none')

def save_json_file(refs,file_name):
    print('start saving_data')
    with open ('./paper_name/{}.json'.format(file_name),'w') as f:
        json.dump(refs,f) 
    print('saving done')

if __name__ == '__main__':
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