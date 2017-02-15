from head import *

def ungzip(data):
    try:
        # 尝试解压
        #print('Ungzipping......')
        data = gzip.decompress(data)
        #print('Finished!')
    except:
        print('No need to zip.')
    return data

def getXSRF(data):
    print('Getting XSRF......')
    
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"', flags = 0)
    strlist = cer.findall(data)
    return strlist[0]

def getOpener(head):
    # deal with the Cookies
    print('Getting opener......')
    
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

opener = getOpener(header)

def dealWithCaptcha(_xsrf):
    #deal with captcha
    print('Dealing with captcha......')
    url_captha = 'https://www.zhihu.com/captcha.gif?r=1461467332441&type=login'
    picture = opener.open(url_captha).read()
    try:
        local = open('./captcha.jpg', 'wb')
        local.write(picture)
        local.close()
    except:
        print('Open captcha.jpg failed!')
        exit()
    picture = Image.open('./captcha.jpg','r')
    picture.show(title='lalalala~~')
    capctha = input('Input captcha： ')
    postDict = {
            '_xsrf':_xsrf,
            'phone_num': phone_num,
            'password': password,
            'remember_me': 'true',
            'captcha':capctha
    }
    postData = urllib.parse.urlencode(postDict).encode()
    op = opener.open(url_main+'login/phone_num', postData)
    data = op.read()
    data = ungzip(data).decode()
    
    return data

def getFirstData():
    global opener
    print('Getting first data......')

    data = opener.open(url_main).read()
    data = ungzip(data).decode()
    
    return data

def getFirstPersonId(data):
    print('Getting first person\'s id......')
    
    cer = re.compile('/people/(.*)\" class=\"zu-top-nav-userinfo \"\>', flags = 0)
    strlist = cer.findall(data)
    
    print('First person\'s id is '+strlist[0])
    return strlist[0]
    
def getDataFromId(pesronId):
    global opener
    print('Getting data from id......')

    url = url_main+'people/'+pesronId+'/followees'
    urlop = opener.open(url,timeout=2)
    data = urlop.read()
    data = ungzip(data).decode()

    return data

def getIdFromData(data):
    print('Getting id from data......')
    
    cer = re.compile('\<h2 class.* href=\"https://www.zhihu.com/people/(.*)\" class=', flags = 0)
    strlist = cer.findall(data)
    return strlist

def getTopicsFromId(personId):
    global opener
    print('Getting topics from id......')
    
    url = url_main+'people/'+personId+'/topics'
    urlop = opener.open(url,timeout=2)
    data = urlop.read()
    data = ungzip(data).decode()
    
    cer = re.compile(r'<strong>(.*)</strong></a>\n<div', flags = 0)
    strlist = cer.findall(data)
    return strlist

def getNumsFromData(data):
    print('Getting numbers......') #赞同，感谢，关注数，被关注数

    cer = re.compile('<strong>(.*?)<\/', flags = 0)
    Nums = cer.findall(data)
    Nums = Nums[0:4]
    return Nums

def getGenderFromData(data):
    print('Getting gender from data......')
    
    cer = re.compile('>(.*)</button>', flags = 0)
    strlist = cer.findall(data)
    if strlist[0] == '关注他':
        gender = 'm'
    else:
        gender = 'w'
    return gender




        

