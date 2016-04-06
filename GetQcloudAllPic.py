#coding=utf-8
#########################################################################
# file: GetQcloudAllPic.py
# author: zhaowei
# mail: 30112737@qq.com
# created Time: 2016年03月28日 星期一 09时34分19秒
#########################################################################

timeout = 5 #超时标记为5秒
import requests
import sys
import os
import time
from bs4 import BeautifulSoup
import qcloud_cos as qcloud

qcloud_bucket = "test"
qcloud_dirname = "pic"
downloadtimeout = 10 #下载图片超时10秒
downloadpath = u'/data/home/icaruszhao/qcloud_down/'
defaultpath = u'./qcloud_logs.txt'

def download_pic(url):
    local_filename = url.split('/')[-1] 
    local_path = downloadpath + local_filename
    #首先删除掉
    os.system("rm %s -f" % local_filename)
    try:
        r = requests.get(url, stream=True, timeout=downloadtimeout)
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

def ListAllPic():
    allcount = 0
    cos = qcloud.Cos()
    page_str = ''
    while True:
        obj = cos.list(qcloud_bucket, "/pic/", 199, "eListBoth", 1, page_str)
        if obj["code"] != 0:
            print "code is not 0 code:[%d] errmsg:[%s]" % (obj["code"],obj["message"])
            return None
        datas = obj["data"]
        infos = datas["infos"]
        print "len(infos):%d" % len(infos)
        allcount += len(infos)
        page_str = datas["context"]
        for item in infos:
            #print item["access_url"]
            ret,msg, localpath,localname = download_pic(item["access_url"])
            time.sleep(0.5)
            if ret:
                print "process [%s] success" % item["access_url"]
            else:
                print "process [%s] failed" % item["access_url"]
        if datas["has_more"] == False:
            break
    print "totle count:%d" % allcount

if __name__ == '__main__':
    ListAllPic()
