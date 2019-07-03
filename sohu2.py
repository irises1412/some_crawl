import urllib.request
from lxml import etree
import requests
from bs4 import BeautifulSoup
import sys
import io
import tqdm
import pickle as pkl

#news_sohu_all=[]
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
news_url_all={}
try:
    for i in tqdm.tqdm(range(1,50000)):
        if (i%5000==1):
            news_sohu_all=[]
        news_url={}
        news_temp_url=[]
        url='https://m.k.sohu.com/ch1/'+repr(i)
        html2=requests.get(url,headers=headers)
        soup2=BeautifulSoup(html2.text,'html.parser')
        if (i==1):
            start=0
        else:
            start=1
        for j in range(start,len(soup2.select('.type_txt'))):
            single1_url='https://m.k.sohu.com'+soup2.select('.type_txt')[j]['href']
            single1_title=soup2.select('.type_txt h4')[j].get_text()
            if news_url_all[single1_title]!=single1_url:
                news_url[single1_title]=single1_url
                news_url_all[single1_title]=single1_url
        for w in range(len(soup2.select('.type_pic_txt'))):
            single2_url='https://m.k.sohu.com'+soup2.select('.type_pic_txt')[w]['href']
            single2_title=soup2.select('.type_pic_txt h4')[w].get_text()
            if news_url_all[single2_title]!=single2_url:
                news_url[single2_title]=single2_url
                news_url_all[single2_title] = single2_url
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
        if (i%5000==0):
            count=i/5000
            print('this is the '+repr(count)+' package')
            print('the url sum is '+repr(len(news_url_all)))
            out_path='/root/Desktop/fxl/org_data/sohu_news_'+repr(count)+'.pkl'
            with open(out_path,'wb') as f:
                pkl.dump(news_sohu_all,f,pkl.HIGHEST_PROTOCOL)
except:
    print(news_sohu_all)
    with open('/root/Desktop/fxl/org_data/except_sohu.pkl', 'wb') as f:
        pkl.dump(news_sohu_all, f, pkl.HIGHEST_PROTOCOL)
# print(news_url)
# print(single1_url)
# print(single1_title)
# print(single2_url)
# print(single2_title)
# print(news_sohu_all)
