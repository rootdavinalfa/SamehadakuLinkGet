import urllib.request
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time 

class bcolors:
    CEND = '\033[0m'
    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'
quality = "480p" #Default
linDownload = []
linkDownloadMp4 = []
linkDownloadx = []

def main():
    urlReq = input(bcolors.CYELLOW+"Enter samehadaku.tv URL\n\nEXAMPLE: https://www.samehadaku.tv/toaru-kagaku-no-accelerator-episode-5/\n=============\nEnter your URL: "+bcolors.CEND)
    print("=========")
    qual = input(bcolors.CBEIGE+"Enter quality\n1.360p\n2.480p\n3.720p\n4.1080p\nDefault(480p)\nYour quality? "+bcolors.CEND)
    if qual == 1:
        quality = "360p"
    elif qual == 2:
        quality = "480p"
    elif qual == 3:
        quality = "720p"
    elif qual == 4:
        quality = "1080p"
        
    openSiteSamehadaku(urlReq)
        
#Step 1
def openSiteSamehadaku(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}) 
    con = urllib.request.urlopen( req ).read()
    soup = BeautifulSoup(con,"html.parser")
    for h1name in soup.find_all('h1',{"itemprop":"name"}):
        print("\n"+bcolors.CYELLOW+"You will Download: "+bcolors.CEND+h1name.text)
    # Samehadaku Download Site MAP
    # <div class="download-eps">
    # <ul>
    # <li style = "textal">
    # <strong> <---- Is for determine quality
    # <span> <--- this have link child
    # </li>
    # </ul>
    # </div>    
    print("\nMKV")
    for divTag in soup.find_all('div', {"class": "download-eps"}):
        for ultag in divTag.find_all('ul'):
            for litag in ultag.find_all('li',{"style":"text-align: center;"}):
                for strong in litag.find_all('strong'):
                    s = strong.text
                    if s.find(quality) > -1:
                        print(s+ " Link")
                        for aLinkDownload in litag.find_all('a',{"rel":"nofollow noopener noreferrer",
                                                                 "style":"color: #ff0000;"}):
                            if aLinkDownload.text.find("GD") > -1:
                                print(aLinkDownload.get('href'))
                                linDownload.append(aLinkDownload.get('href'))
    #Other Link
    other = 1
    for divTagOther in soup.find_all('div', {"class": "download-eps",
                                        "style":"text-align: center;"}):
        if other==1:
            print("\nMP4")
        else:
            print("\nx265")
        for ultagOther in divTagOther.find_all('ul'):
            for litagOther in ultagOther.find_all('li'):
                for strongOther in litagOther.find_all('strong'):
                    sOther = strongOther.text
                    if sOther.find(quality) > -1:
                        print(sOther+ " Link")
                        for aLinkDownloadOther in litagOther.find_all('a',{"rel":"nofollow noopener noreferrer",
                                                                 "style":"color: #ff0000;"}):
                            if aLinkDownloadOther.text.find("GD") > -1:
                                print(aLinkDownloadOther.get('href'))
                                if other==1:
                                    linkDownloadMp4.append(aLinkDownloadOther.get('href'))
                                else:                        
                                    linkDownloadx.append(aLinkDownloadOther.get('href'))
        other = other + 1
    videoKind = input("\n"+bcolors.CYELLOW+"Select your desired format:\n1.MKV\n2.MP4\n3.x265 Codec\n(Default Format is MKV)\nWhat do you want?: "+bcolors.CEND)
    kind = []
    print("\nTetew Opener\n")
    if videoKind == '1':
        kind = linDownload
    elif videoKind == '2':
        kind = linkDownloadMp4
    elif videoKind == '3':
        kind = linkDownloadx
    else:
        kind = linDownload
    
    adownlist =[]
    for x in kind :
        adownlist.append(openSiteTetew(x))
    
    
    noerror = True
    while(noerror):
        i = 1
        for d in adownlist:
            #print(adownlist[d])
            print(str(i)+" : "+d+"\n")
            i += i
            
        print("COUNT:"+str(len(adownlist)))    
        reqUrl = input(bcolors.CYELLOW+"Enter link number (eg: 1 if empty,we will auto select 1): "+bcolors.CEND)
        if reqUrl is not "":
            reqNum = int(reqUrl) -1
            if adownlist[reqNum] != "":
                noerror = False
                openSiteToGdrive(adownlist[reqNum])
            else:
                print('Please enter valid number')   
        else:
            noerror = False
            openSiteToGdrive(adownlist[0])                

#Step2
def openSiteTetew(url):
    #adownlist = []
    req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}) 
    con = urllib.request.urlopen( req ).read()
    soup = BeautifulSoup(con,"html.parser")
    for divTagDown in soup.find_all('div',{"style":"text-align:center;font-size:14px;"}):
        for aDown in divTagDown.find_all('a',{'rel':'nofollow'}):
            #print(aDown.get('href')+"\n")
            return aDown.get('href')
            #adownlist.append(aDown.get('href'))
            #openSiteToGdrive(aDown.get('href'))
    #return adownlist
    return None
#Step3
def openSiteToGdrive(url):
    print("Google Drive From Samehadaku -> Gdrive\n")
    print("URL: "+url+"\n"+bcolors.CYELLOW+"Please Wait ETA 10 Seconds on good Internet Connection"+bcolors.CEND+"\n")
    browser = webdriver.PhantomJS("./libs/phantomjs.exe")
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(8)
    for resultDiv in soup.find_all('div',{"class":"result"}):
        click1 = browser.find_element_by_css_selector('.result > a')
        click1.click()
        c1 = click1.text
        
        print(c1)
        time.sleep(2)
        click2 = browser.find_element_by_css_selector('.result > a')
        click2.click()
        c2 = click2.get_attribute("href")
        print(bcolors.CYELLOW+"Here your demanded GDRIVE Link: "+bcolors.CEND+c2)
        print(bcolors.CGREEN+"Thanks for using this tool.Help me and contribute at https://github.com/rootdavinalfa/SamehadakuLinkGet"+bcolors.CEND)
if __name__ == "__main__":
    main()
