import urllib.request
from lxml import etree
import requests
from bs4 import BeautifulSoup
import sys
import io
import tqdm
import pickle as pkl

news_sohu_all=[]

for i in tqdm.tqdm(range(1,10)):
    news_url={}
    url='https://m.k.sohu.com/ch1/'+repr(i)
    html2=requests.get(url)
    soup2=BeautifulSoup(html2.text,'html.parser')
    for j in range(len(soup2.select('.type_txt'))):
        single1_url='https://m.k.sohu.com'+soup2.select('.type_txt')[j]['href']
        single1_title=soup2.select('.type_txt h4')[j].get_text()
        news_url[single1_title]=single1_url
    for j in range(len(soup2.select('.type_pic_txt'))):
        single2_url='https://m.k.sohu.com'+soup2.select('.type_pic_txt')[j]['href']
        single2_title=soup2.select('.type_pic_txt h4')[j].get_text()
        news_url[single2_title]=single2_url
    for k in news_url.keys():
        text_url=news_url[k]
        text_html=requests.get(text_url)
        text_soup=BeautifulSoup(text_html.text,'html.parser')
        news_text=''
        news_temp=[]
        for w in range(3,len(text_soup.select('p'))-3):
            text_single=text_soup.select('p')[w].get_text()
            news_text+=text_single
        news_temp.append(k)
        news_temp.append(news_text)
        news_sohu_all.append(news_temp)
with open('D:/sohu_E.pkl','wb') as f:
    pkl.dump(news_sohu_all,f,pkl.HIGHEST_PROTOCOL)
# print(news_url)
# print(single1_url)
# print(single1_title)
# print(single2_url)
# print(single2_title)
# print(news_sohu_all)
