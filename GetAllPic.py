#coding=utf-8
#########################################################################
# file: GetAllPic.py
# author: zhaowei
# mail: 30112737@qq.com
# created Time: 2016年01月11日 星期一 15时39分05秒
#########################################################################

timeout = 5 #超时记为5秒
import requests
import sys
import os
from bs4 import BeautifulSoup
import qcloud_cos as qcloud

qcloud_bucket="test"
qcloud_dirname="pic"
downloadtimeout = 10 #下载图片超时10秒
downloadpath = u'/data/home/icaruszhao/download/'
defaultpath = u'./MovieAllPic.txt'
headers = {"Accept":"image/webp,*/*;q=0.8", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36","Referer":"http://www.id97.com/","Accept-Encoding":"gzip, deflate, sdch","Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"}

def download_pic(url):
    local_filename = url.split('/')[-1] 
    local_path = downloadpath + local_filename
    #首先删除掉
    os.system("rm %s -f" % local_filename)
    try:
        r = requests.get(url, stream=True, timeout=downloadtimeout, headers=headers)
    except BaseException, e:
        msg = "get [%s] error exception:%s" % (url, str(e))
        print msg
        return False,msg,"",""
    if r.status_code != 200:
        msg = "http code is not 200.return:%d" % r.status_code
        return False,msg,"",""
    with open(local_path,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()
    return True,"",local_path,local_filename
       
        
def process_pic_url(url):
    ret,msg,filepath,filename = download_pic(url)
    if ret != True:
        print "process [%s] error.msg:%s" % (url, msg)
        return None
    #已经下载到了filepath路径上了，上传到对象存储系统中
    qcloud_filepath = "%s/%s" % (qcloud_dirname,filename)
    cos = qcloud.Cos()
    obj = cos.upload(filepath, qcloud_bucket, qcloud_filepath)
    if obj["code"]  == 0:
        print "upload [%s] success" % url
    elif obj["code"] == -4018:
        print "upload [%s] success [already upload]"
    else:
        print "upload [%s] failed.code:%d msg:%s" % (url, obj["code"], obj["message"])
    #删除文件
    os.system('rm %s -f' % filepath)
if __name__ == '__main__':
    filepath = defaultpath
    if len(sys.argv) > 1:
        #未传参数
        filepath = sys.argv[1]
    try:
        f = open(filepath)
    except BaseException,e:
        print "open file[%s] error.msg:%s" %(filepath, str(e))
        os._exit(-1)
    
    line = f.readline()
    while line:
        process_pic_url(line.strip('\n'))
        line = f.readline()
    print "process all success"
