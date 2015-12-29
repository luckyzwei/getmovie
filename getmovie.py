#coding=utf-8
#########################################################################
# file: getmovie.py
# author: zhaowei
# mail: 30112737@qq.com
# created Time: 2015年12月29日 星期二 10时03分47秒
#########################################################################

timeout = 5 #超时记为5秒
import requests
from bs4 import BeautifulSoup

def getmoviepage(pageindex):
    url = u"http://www.id97.com/videos/movie?page=%d" % pageindex
    try:
        r = requests.get(url, timeout=timeout)
    except BaseException,e:
        msg = "get [%s] error exception:%s" % (url, str(e))
        print msg
        return False, msg
    if r.status_code != 200 :
        msg =  "http code is not 200.return: %d" % r.status_code
        return False, msg 
    #print r.text
    soup = BeautifulSoup(r.text)
    #find all item
    itemlist = soup.find_all('div', class_='movie-item')
    for oneitem in itemlist:
        oneurl = oneitem.find('a')['href']
        title = oneitem.find('a')['title']
        print "name:%s url:%s" % (title, oneurl)

def resolve_alla(soups):
    result = []
    for onetag_a in soups.find('a'):
        result.append(onetag_a.text)
    return result
def resolve_director(directors_soup):
    return resolve_alla(directors_soup)

def resolve_bianju(bianju_soup):
    return resolve_alla(bianju_soup) 

def resolve_actor(actor_soup):
    return resolve_alla(actor_soup)

def resolve_type(type_soup):
    return resolve_alla(type_soup)

def resolve_country(country_soup):
    return resolve_alla(country_soup)

def resolve_douban_score(score_soup):
    return score_soup.find('a').text.replace(' ','') 

def resolve_pic(soup):
    urllist = []
    allpicitem = soup.find_all(class_='movie-screenshot')
    for oneitem in allpicitem:
        picurl = oneitem.find('a')['href']
        urllist.append(picurl)
    return urllist
def resolve_magnet():
    magnet = []
    magnetsouplist = soup.select('a[href^=magnet:"]')
    for onemagnet in magnetsouplist:
        magnet.append(onemagnet['href'])
    magnet_norepeat = list(set(magnet))
    return magnet_norepeat

def getmoviedetail(oneurl):
    try:
        r = requests.get(oneurl, timeout=timeout)
    except BaseException,e:
        msg = "get [%s] error exception:%s" % (oneurl, str(e))
        return False,msg 
    if r.status_code != 200:
        msg = 'http code is not 200. return: %d' % r.status_code
        return False, msg
    soup = BeautifulSoup(r.text)
    info_totle_title = soup.find(class_="movie-title").text.split('(')[0]
    info_year = soup.find(class_="movie-year").text.replace('(','').replace(')','')

    #read movie info
    infotds = soup.find(class_='col-md-8').select("tr td")
    info_director     = resolve_director(infotds[1])
    info_bianju       = resolve_bianju(infotds[3])
    info_actor        = resolve_actor(infotds[5])
    info_type         = resolve_type(infotds[7])
    info_country      = resolve_country(infotds[9])
    info_language     = infotds[11].text
    info_uptime       = infotds[13].text
    info_movietime    = infotds[15].text
    info_altername    = infotds[17].text
    info_douban_score = resolve_douban_score(infotds[19])

    #read summay
    info_summary = soup.find(class_='summary').text.replace(u'展开全部','')

    #read pictures
    info_pic_urls = resolve_pic(soup)

    #get resource
    baiduyunlink = ""
    baiduyunpwd  = ""
    baidulinklist = soup.select('a[href^="http://pan.baidu.com/"]')
    if len(baidulinklist) != 0:
        baiduyunlink = baidulinklist[0]['href']
    baidupwdlist = soup.select('strong[style="color:red;"]')
    if len(baidupwdlist) != 0:
        baiduyunpwd = baidupwdlist[0].text
    
    #get cili
    magnetlist = resolve_magnet()
if __name__ == '__main__':
    getmoviepage(1)
