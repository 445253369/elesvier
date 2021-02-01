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
    'cookie': '__cfduid=d6f0fce2f5fd47973da4bc764cee410641599569023; EUID=cc049802-0152-4767-b75b-79af5110c0b2; id_ab=B:100:8:69285b1c-17a6-48b1-afa6-d2d54e467638; utt=aed7ae2437d64719d80de30acce8d7c439af05-Ih8U; __gads=ID=c23a06ff53f75623:T=1599569029:S=ALNI_MbMGOJBNA0KaSGuSNxtzL33tNbQgw; mboxes=%5B%7B%22index%22%3A0%2C%22name%22%3A%22article-page-view-only-pdf-server-side-mbox%22%7D%5D; sd_session_id=aed138028495a543ca49f549609662b3af23gxrqa; acw=aed138028495a543ca49f549609662b3af23gxrqa%7C%24%7C9E221343D53F67E15F74955E23A516BA5B91D204ECD4D89D9215D068BD8DA2E1E8E00F7C3E8EFC42FB48EF432DB1177A02B2002251E7669F3FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; ANONRA_COOKIE=7E99CB90ABBE0A18220E9EE544701CAF325D4445EA94CC2D4E1EF6347CE6F65FCAA77934C69240C4F96B473ECE15B2E78053F3E6F5170B73; has_multiple_organizations=false; fingerPrintToken=42fa3eb1533f063c9b2d630227a48660; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=870038026%7CMCIDTS%7C18518%7CMCMID%7C67861318124052777113594842155020358020%7CMCAAMLH-1600519048%7C11%7CMCAAMB-1600519048%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1599921448s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1134298126%7CMCSYNCSOP%7C411-18521%7CvVersion%7C5.0.0; mbox=session%232aeddc00315b420e82b20fda9dda6c30%231599917065%7CPC%23111599569327586-830640.37_0%231663160005; s_pers=%20c19%3Dsd%253Aproduct%253Ajournal%253Aarticle%7C1599916932785%3B%20v68%3D1599915204260%7C1599916932802%3B%20v8%3D1599915133265%7C1694523133265%3B%20v8_s%3DLess%2520than%25207%2520days%7C1599916933265%3B; s_sess=%20s_cpc%3D0%3B%20s_ppvl%3Dsd%25253Abrowse%25253Ajournal%25253Ahome%252C29%252C29%252C937%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20e41%3D1%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C100%252C100%252C2043%252C1175%252C937%252C1920%252C1080%252C1%252CP%3B; MIAMISESSION=23431e25-d8ea-4499-966f-ef999413457c:3777368235; SD_REMOTEACCESS=eyJhY2NvdW50SWQiOiI1MzU1MiIsImRlcHRJZCI6Ijc1NjM3IiwidGltZXN0YW1wIjoxNTk5OTE1NDM2MDM0fQ=='
    }

none_file_name = []


article_url = 'https://www.sciencedirect.com/science/article/pii/S2157171619300140#cebib0010'
resps = requests.get(article_url,headers = headers)
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
reference_dict = requests.get(reference_url,headers = headers).text
print(type(reference_dict))
print(title_id)