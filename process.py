from function import *

def login():
    global phone_num
    global password
    global url_main
    global _xsrf
    global opener

    op = opener.open(url_main)
    data = op.read()
    data = ungzip(data)
    # 解压
    _xsrf = getXSRF(data.decode())
    print('XSRF is: '+_xsrf+'\n')
    postDict = {
            '_xsrf':_xsrf,
            'phone_num': phone_num,
            'password': password,
            'rememberme': 'y'
    }
    postData = urllib.parse.urlencode(postDict).encode()
    op = opener.open(url_main+'login/phone_num', postData)
    data = op.read()
    data = ungzip(data).decode()
    if r'\u8bf7\u586b\u5199\u9a8c\u8bc1\u7801' in data:
        data = dealWithCaptcha(_xsrf)

    if r'\u767b\u9646\u6210\u529f' in data:
        print('Result of login:\n'+data+'\n')
    else:
        print('Login in failed!')

    return data

def prepare():
    data = getFirstData()
    firstPersonId = getFirstPersonId(data)
    data = getDataFromId(firstPersonId)
    if 'data' not in os.listdir(os.getcwd()):
        os.mkdir('./data')      #新建data文件夹
    print('Preparation finished!\n')
    
    return data

def traverse1(data):
    global MAXNUM
    global MINFOLLOWERS
    toVisit = deque()
    V10k = deque()
    V50k = deque()
    Visited = set()
    count1 = 0    #the num of visited
    count2 = 0    #the num of tovisit
    
    for personId in getIdFromData(data):
        toVisit.append(personId)
        Visited.add(personId)

    f = open('./data/basciData','w')
    while(1):
        try:
            if toVisit != deque():
                personId = toVisit.popleft()
            else:
                break
        except:
            break
        
        Visited.add(personId)
        
        try:
            data = getDataFromId(personId)
        except:
            continue
        
        Nums = getNumsFromData(data)

        followers = int(Nums[3])
        if followers > V10KFOLLOWERS:
            V10k.append(personId)
        if followers > V50kFOLLOWERS:
            V50k.append(personId)
            
        f.write(personId+' '+Nums[0]+' '+Nums[1]+' '+Nums[2]+' '+Nums[3]+'\n')
        print('Numbers({:05d}) finished.\n'.format(count1))
        
##      not need to look at this paragraph
##        
##        try:
##            f = open('./data/{:05d}'.format(count1),'w')
##            f.write(personId+' '+Nums[0]+' '+Nums[1]+' '+Nums[2]+' '+Nums[3]+'\n')
##            print('File{:05d} finished.\n'.format(count1))
##            f.close()
##        except:
##            print('Open Error!')
##            exit(0)

        count1 += 1
        
        if count1 > MAXNUM:
            print('Up to MAXNUM!\n')
            break

        if count2 < MAXNUM:
            for personId in getIdFromData(data):
                if personId not in Visited:
                    toVisit.append(personId)
                    count2 += 1
    f.close()
    
    f = open('./data/V10kId','w')
    for i in V10k:
        f.write(i+'\n')
    f.close()
    
    f = open('./data/V50kId','w')
    for i in V50k:
        f.write(i+'\n')
    f.close()

def traverse2(data,n):
    pass
    
def buildV10kDigraph():
    print('Getting digraph data of V10k......')
    personIds = []
    gender = []
    personFollowees = []
    personTopics = []
    count = 0

    f = open('./data/V10kId','r')
    #此处联网
    for i,line in enumerate(f):
            try:
                line = line.strip()
                data = getDataFromId(line)
                print('Got {num} 10k people.'.format(num = count + 1))
                gender.append(getGenderFromData(data))
                personTopics.append(getTopicsFromId(line))
                personFollowees.append(getIdFromData(data))
                count = count + 1
                personIds.append(line)
            except:
                print('Get {num}th person failed!'.format(num = i + 1))
    f.close()
    #之后该函数无须联网
    
    for i,balabala in enumerate(personIds):
        for personFollowee in personFollowees[i]:
            if personFollowee not in personIds:
                personFollowees[i].remove(personFollowee)
    try:
        f = open('./data/V10kDigraph','w')
        print('\nBuilding 10k digraph......\n')
        for i,eachPerson in enumerate(personFollowees):
            f.write(personIds[i]+'('+gender[i]+'): ')
            for personFollowee in eachPerson:
                f.write(personFollowee+' ')
            f.write('\n')
            for personTopic in personTopics[i]:
                f.write(personTopic+'|')
            f.write('\n\n')
        f.close()
        print('Building 10k digraph successfully!\n')
    except:
        print('Open V10kDigraph failed!\n')

def buildV50kDigraph():
    print('Getting digraph data of V10k......')
    personIds = []
    personFollowees = []
    personTopics = []
    gender = []
    count = 0
    
    f = open('./data/V50kId','r')
    #此处联网
    for i,line in enumerate(f):
        try:
            line = line.strip()
            data = getDataFromId(line)
            print('Got {num} 50k people.'.format(num = count + 1))
            gender.append(getGenderFromData(data))
            personFollowees.append(getIdFromData(data))
            personTopics.append(getTopicsFromId(line))
            count = count + 1
            personIds.append(line)
        except:
            print('Get {num}th person failed!'.format(num = i + 1))
    f.close()
    #之后该函数无须联网

    for i,balabala in enumerate(personIds):
        for personFollowee in personFollowees[i]:
            if personFollowee not in personIds:
                personFollowees[i].remove(personFollowee)
    try:
        f = open('./data/V50kDigraph','w')
        print('\nBuilding 50k digraph......\n')
        for i,eachPerson in enumerate(personFollowees):
            f.write(personIds[i]+'('+gender[i]+'): ')
            for personFollowee in eachPerson:
                f.write(personFollowee+' ')
            f.write('\n')
            for personTopic in personTopics[i]:
                f.write(personTopic+'|')
            f.write('\n\n')
        f.close()
        print('Building 50k digraph successfully!\n')
    except:
        print('Open V50kDigraph failed!\n')
