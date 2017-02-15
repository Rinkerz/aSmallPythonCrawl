import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse
from collections import deque
from PIL import Image
import os

MAXNUM = 50             #MAXNUM是设定的最大抓取人数
V10KFOLLOWERS = 10000
V50kFOLLOWERS = 50000
phone_num = '18225695145'
password = '19981016rk'
url_main = 'https://www.zhihu.com/'
header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.zhihu.com',
    'DNT': '1'
}
