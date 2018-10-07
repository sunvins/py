#coding:utf-8
class ListHelper:
    def __init__(self, index_namme, srclist):
        self.index_namme=index_namme
        self.indexList=[]
        self.map={}
        for item in srclist:
            index_value=getattr(item, self.index_namme)
            if not self.map.has_key(index_value):
                self.indexList.append(index_value)
                itemList=[item]
                self.map[index_value]=itemList
            else:
                itemList=self.map[index_value]
                itemList.append(item)
            self.indexList.sort()

    def getItemList(self,index_value):
        return self.map[index_value]

class FieldTb:
    def __init__(self):
        pass

# m1=FieldTb()
# m1.url="www.163.com"
# m1.tbname="nice1"
#
# m2=FieldTb()
# m2.url="www.sina.com"
# m2.tbname="hao1"
#
# m21=FieldTb()
# m21.url="www.sina.com"
# m21.tbname="hao2"
#
# m22=FieldTb()
# m22.url="www.sina.com"
# m22.tbname="hao1"
#
# m3=FieldTb()
# m3.url="www.163.com"
# m3.tbname="nice2"
#
# m4=FieldTb()
# m4.url="www.baidu.com"
# m4.tbname="good2"
#
# m41=FieldTb()
# m41.url="www.baidu.com"
# m41.tbname="good3"
#
# m42=FieldTb()
# m42.url="www.baidu.com"
# m42.tbname=""
#
# m5=FieldTb()
# m5.url="www.sina.com"
# m5.tbname="hao0"
#
# # print m1.tbname
# # print m2.url
# fieldList=[m1,m2,m3,m4]
# fieldList.extend([m5,m21,m22,m41,m42])
# # print len(fieldList)
# #
# listHelper=ListHelper("url",fieldList)
# for url in listHelper.indexList:
#     # for item in listHelper.getItemList(url):
#     #     print url,item.tbname
#     #   下载这个url
#         listHelper2 = ListHelper("tbname", listHelper.getItemList(url))
#         for tbname in listHelper2.indexList:
#             for item2 in listHelper2.getItemList(tbname):
#                 print url,tbname
