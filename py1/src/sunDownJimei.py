# coding:utf-8
import datetime
import os
import urlparse

from bs4 import BeautifulSoup
from lxml import etree, html

from ListHelper import ListHelper
from MailHelper import sendMail
# import commVO
from commVO import *
from common import download


import time;
class Animal(object):
    fieldTb= FieldTb()
    def saveHtml(self,file_name, file_content):
        soup = BeautifulSoup(file_content)
        file_content=soup.prettify()
        with open(file_name, "wb") as f:
            f.write(file_content)

    def scrape(self,htmlText):
        # print htmlText
        lhtml = etree.HTML(htmlText,parser=etree.HTMLParser(encoding='utf-8'))
        # print etree.tostring(lhtml)
        lis=lhtml.xpath(self.fieldTb.pxpath)
        # print len(lis)
        # print lis
        # # lis = lhtml.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/ul/li')
        # print lis.text_content()
        for li in lis:
            # print li.text.strip()
            area = li.xpath(self.fieldTb.xpath)
            # print area
            for m in area:
                if m.strip()!="":
                    print m.strip()

    def readFile(self,fileName):
        # print "read exits file"
        with open(fileName) as file_object:
            html = file_object.read()
            return html

    def downOrExplain(self,aurl):
        fileName = aurl.replace('http://', '').replace('/', '_').replace('?', '_') + ".html"
        # print fileName
        # fileName="m1.html"
        if not os.path.exists(fileName):
            print "down file"
            html = download(aurl)
            self.saveHtml(fileName, html)
        self.html = self.readFile(fileName)
        # self.scrape(html)

    def readUrl(self):
        self.downOrExplain(self.fieldTb.url)

    def getText(self,a):
        ret=""
        for text in a:
            if text.strip() != "":
                ret= ret+text.strip()
        return ret
    def test(self):
        a=self
        a.fieldTb.url="http://www.fzwsrc.com/sydwzk/policy/policy.jsp?TypeID=7"
        a.fieldTb.pxpath='//td[1]/a[@href="javascript:void(null)"]'
        # a.fieldTb.xpath='../../td/text()'
        a.fieldTb.xpath='../a/@onclick'
        a.readUrl()
        a.scrape(a.html)



    def main(self):
        time_start=time.time();
        # qry = session.query(func.max(FieldRsTb.batchid)).all();
        # batchid=qry[0][0]
        # if not batchid:
        #     batchid=0

        # res = session.query(FieldTb).all()
        proj="卫生人才网招考"
        rsMap=self.getOldRs(proj)
        # url="http://www.fzwsrc.com/sydwzk/policy/policy.jsp?TypeID=7"
        res = session.query(FieldTb).filter(FieldTb.tbname == proj)
        listHelper=ListHelper("url",res)
        mailHtml=""
        for url in listHelper.indexList:
            print url
            a = Animal()
            a.downOrExplain(url)
            listHelper2 = ListHelper("tbname", listHelper.getItemList(url))
            for tbname in listHelper2.indexList:
                print tbname
                lhtml = etree.HTML(a.html, parser=etree.HTMLParser(encoding='utf-8'))
                listHelper3 = ListHelper("pxpath", listHelper2.getItemList(tbname))
                for pxpath in listHelper3.indexList:
                    print pxpath
                    lis = lhtml.xpath(pxpath)
                    for li in lis:
                        article = Article()

                        article.url = url
                        article.updatedttm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        for item3 in listHelper3.getItemList(pxpath):
                            # print item3.fieldname
                            area = li.xpath(item3.xpath)
                            rs= a.getText(area).encode("utf-8")
                            article.proj=item3.tbname
                            if item3.fieldname=="title":
                                article.title=rs
                            elif item3.fieldname=="detail_url":
                                rs=rs.replace("javascript:window.open('","")
                                rs = rs.replace("')", "")
                                article.detail_url=rs
                            elif item3.fieldname == "pub_date":
                                article.pub_date = rs

                        titleKey=article.title+"_"+article.pub_date
                        titleKey=titleKey.encode("utf-8")
                        if not rsMap.has_key(titleKey):
                            session.add(article)
                            mailHtml+="<a href='"+urlparse.urljoin(url,article.detail_url)+"'>"+article.title+"</a> "+article.pub_date+"<br/>"
                        else:
                            print "Exist :"+titleKey

        session.commit()
        print mailHtml
        if mailHtml!="":
            sendMail(mailHtml)
        print time.time()-time_start
    def getOldRs(self,proj):
        # proj="卫生人才网招考"
        oldRs = session.query(Article).filter(Article.proj == proj)
        rsMap = {}
        for item in oldRs:
            titleKey = item.title + "_" + item.pub_date
            titleKey=titleKey.encode("utf-8")
            rsMap[titleKey]=item.detail_url
        return rsMap

a = Animal()
a.main()