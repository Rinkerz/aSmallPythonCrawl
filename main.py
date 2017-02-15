from process import *

def main():
    login()                 #登录
    data = prepare()        #预备工作
#   traverse1(data)         #第一种遍历
#   traverse2(data,n)       #第二种遍历

    buildV10kDigraph()   #获取10k有向图
#   buildV50kDigraph()   #获取50k有向图

if __name__ == '__main__':
    main()

