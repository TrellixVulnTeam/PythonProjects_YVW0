
#-*- coding: utf-8 -*-
'''
Created on Mar 6, 2018

@author: 12543
'''
from selenium import webdriver
from mylog import MyLog as mylog
from selenium.webdriver.chrome.options import Options

class Item(object):
    ip=None #代理IP
    port=None #代理端口
    anonymous=None #是否匿名
    type=None #类型
    support=None #֧支持的协议
    local=None #物理地址ַ
    speed=None #代理速度
    
class GetProxy(object):
    def __init__(self):
        self.startUrl='https://www.kuaidaili.com/free/inha/'
        self.log=mylog()
        self.urls=self.getUrls()
        self.proxyList=[]
        self.getProxyList(self.urls)
        self.fileName='proxy.txt'
        self.saveFile(self.fileName)
        
    def getUrls(self):
        urls=[]
        for i in range(1,11):
            url=self.startUrl+str(i)
            urls.append(url)
            self.log.info('get url %s to urls'%url)
        return urls
    
    def getProxyList(self,urls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=(r'D:\Program Files\Python36\seleniumDriver\chromedriver.exe'), chrome_options=chrome_options)
        for url in urls:
            driver.get(url)
            driver.implicitly_wait(5)
            elements=driver.find_elements_by_xpath('//tbody/tr')
            for element in elements:
                item = Item()
                item.ip=element.find_element_by_xpath('./td[1]').text
                item.port=element.find_element_by_xpath('./td[2]').text
                item.anonymous=element.find_element_by_xpath('./td[3]').text
                item.type=element.find_element_by_xpath('./td[4]').text
                item.support=element.find_element_by_xpath('./td[5]').text
                item.local=element.find_element_by_xpath('./td[6]').text
                item.speed=element.find_element_by_xpath('./td[7]').text
                self.proxyList.append(item)
                self.log.info('add proxy %s:%s to list'%(item.ip,item.port))
        driver.quit()
    
    def saveFile(self,fileName):
        self.log.info('add all proxy to %s'%fileName)
        with open(fileName,'w',encoding='utf8') as fp:
            for item in self.proxyList:
                fp.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(item.ip,item.port,item.anonymous,item.type,item.support,item.local,item.speed))
    
if __name__=='__main__':
    GP=GetProxy()    
        
