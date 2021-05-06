#! /usr/bin/python3
#-*-coding:utf-8-*- 
'''
批量下载豆瓣首页的图片

采用伪装浏览器的方式爬取豆瓣网站首页的图片，保存到指定路径文件夹下
'''

#导入所需的库
import urllib.request.request,socket,re,sys,os

#定义文件保存路径
targetPath = "./images"

def saveFile(path):
    #检测当前路径的有效性
    if not os.path.isdir(targetPath):
        os.mkdir(targetPath)

    #设置每个图片的路径
    pos = path.rindex('/')
    t = os.path.join(targetPath,path[pos+1:])
    print(t)
    return t

#用if __name__ == '__main__'来判断是否是在直接运行该.py文件


# 网址
url = "https://www.douban.com/"
#headers = {
 #       'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
 #       }

headers = {
        'User-Agent':'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
req = urllib.request.Request(url=url, headers=headers)

res = urllib.request.urlopen(req)

data = res.read()

for link,t in set(re.findall(r'(https:[^s]*?(jpg|png|gif))', str(data))):

    #link = 'http://img.jandan.net/news'+link
    #link = link[:-7]
    print(link)
    try:
        urllib.request.urlretrieve(link,saveFile(link))
        #urllib.request.urlretrieve(link)
    except:
        print('失败')
