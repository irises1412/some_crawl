import re
from selenium import webdriver
import time
import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
import tqdm
import pickle as pkl
from selenium.webdriver.firefox.options import Options

url = 'https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page='
# https://news.sina.com.cn/roll/#pageid=153&lid=2974&k=&num=50&page= #国内国际社会 推荐至620
# https://news.sina.com.cn/roll/#pageid=153&lid=2515&k=&num=50&page= #科技
# r'https://news.sina.com.cn/roll/#pageid=153&lid=2513&k=&num=50&page=' #娱乐

news = []
it_url_list = []
news_pkl_count = 0
url_pkl_count = 0
pages_to_crawl = 500

firefox_options = Options()
firefox_options.set_headless()
driver = webdriver.Firefox(firefox_options=firefox_options)

for i in tqdm.tqdm(range(1, 1 + pages_to_crawl)):
    # url section
    driver = webdriver.Firefox(firefox_options=firefox_options)
    driver.get(url + str(eval('i')))
    driver.implicitly_wait(3)
    # time.sleep(1)
    html = driver.page_source
    tree = fromstring(html)
    orgnl_list = tree.xpath('//a/@href')
    re_string = ','.join(orgnl_list)
    url_list = re.findall(r'(https://.+?shtml),', re_string)
    time.sleep(1)
    driver.close()

    # print(url_list)
    it_url_list = it_url_list + url_list
    # content section
    for item in url_list:
        news_page = requests.get(item)
        news_page.encoding = 'utf-8'
        news_html = news_page.text
        soup = BeautifulSoup(news_html, 'html.parser')
        try:
            title = soup.select('.main-title')[0].text
        except:
            title = ''
        try:
            content = soup.select('.article')[0].text
        except:
            content = ''
        news_temp = [title, content]
        news.append(news_temp)

    # print(len(it_url_list))
    # print(len(news))
    if (len(it_url_list) >= 5000):
        with open(r'/root/Desktop/fxl/org_data/sina_roll_society/sina_rolling_society_url_' + str(eval('url_pkl_count')) + '.pkl', 'wb') as f:
            pkl.dump(it_url_list, f, pkl.HIGHEST_PROTOCOL)
        with open(r'/root/Desktop/fxl/org_data/sina_roll_society/sina_rolling_society_news_' + str(eval('news_pkl_count')) + '.pkl', 'wb') as f:
            pkl.dump(news, f, pkl.HIGHEST_PROTOCOL)
        news_pkl_count = news_pkl_count + 1
        url_pkl_count = url_pkl_count + 1
        it_url_list = []
        news = []

with open(r'/root/Desktop/fxl/org_data/sina_roll_society/sina_rolling_society_url_' + str(eval('url_pkl_count')) + '.pkl', 'wb') as f:
    pkl.dump(it_url_list, f, pkl.HIGHEST_PROTOCOL)
with open(r'/root/Desktop/fxl/org_data/sina_roll_society/sina_rolling_society_news_' + str(eval('news_pkl_count')) + '.pkl', 'wb') as f:
    pkl.dump(news, f, pkl.HIGHEST_PROTOCOL)
