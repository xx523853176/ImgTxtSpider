# -*-coding:utf-8-*-

import os

import time
import requests
import re
import json

from bs4 import BeautifulSoup as bs

import asyncio #no use



"""
    分析当前文档信息

    :param: text: 文库的 html-text.
    :return: A dict. 包含有文档重要信息的字典.

    VIP免费、其他：可浏览全部
    VIP专享、收费：不可浏览全部

    Returned Dict:
    >>>player: 请求格式【type=?
    isPayDocAndCommented: 文档是否已经评论（付费文档）
    commentStar: 文档已评论的星级
    creater: 贡献者
    createUserId: 贡献者用户ID
    >>>title: 文档标题
    >>>docId: 请求文档ID【doc_id=?
    docType: 文档格式×
    >>>docTypeNum: 文档格式号√
    flag: ？
    can_dump: 文档是否可以转存网盘
    cats: cid1+cid2+cid3+cid4: ？
    price: 文档价格
    size: 文档？
    rateNum: 文档评分
    >>>totalPageNum: 文档页数
    catal: ？
    relateDoc: ？
    otherLikeDoc: ？
    relateAlblum: ？
    sameSeriesDoc: ？
    readerType: ？
    >>>payPrice: +int 【若为"0"或""，则可浏览全部。否则浏览部分。
    isPaymentDoc: +？
    freepagenum: 免费页数+？
    ispaied: +？
    writername: ？
    isdownloaded: +？
    isPrivate: 是否为私有文档
    isInRoomButDeletedByCreater: ？
    goodsPayStatus: ？
    is_vip_free_doc: 是否为VIP免费文档
    hasImage: ？
    org_engName: ？
    vip_price: +？
    vip_type: +？
    edu_vip_type: +？
    jiaoyu_vip_type: +？
    is_edu_doc: +？
    docTicket: +'int' 【需要int张下载券
    is_discount_doc: +？
    JOINVIP_URL: ？
    confirm_price: ？
    professionalDoc: VIP专享文档
    verticalDocType: ppt垂类文档
    isRepeatDown: +？ 付费文档是否已下载
    """
    




class 百度文库下载:

    文档格式字典 = {
                        '0': '',
                        '1': 'doc',
                        '2': 'xls',
                        '3': 'ppt',
                        '4': 'docx',
                        '5': 'xlsx',
                        '6': 'pptx',
                        '7': 'pdf',
                        '8': 'txt',
                        '9': 'wps',
                        '10': 'et',
                        '11': 'dps',
                        '12': 'vsd',
                        '13': 'rtf',
                        '14': 'pot',
                        '15': 'pps',
                        '16': 'epub'
                        }



#headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}



    def __init__( self, 文档网址, 存储目录 ):

        self.文档网址 = 文档网址
        self.文档信息字典 = { "缺省GET网址": "https://wenku.baidu.com/browse/getbcsurl?pn=1&rn=99999" }
        self.请求信息页 = ""

        self.全图字符码 = b""
        self.分图起止点列表 = []

        self.文本请求地址列表 = []
        self.追加存储文本 = ""
        
        self.存储目录 = 存储目录
        self.存储文件夹 = ""

        self.文档信息获取()
        #print( self.文档信息字典 )
        self.文档内容获取()



    def 创建存储文件夹( self ):
        """
        + 更新 self.存储文件夹。
        + 创建 存储文件夹。
        """
        self.存储文件夹 = self.存储目录 \
            +self.文档信息字典[ "标题" ] \
            + time.strftime("-%Y%m%d-%H%M%S", time.localtime()) \
            + "\\"
        if not os.path.exists( self.存储文件夹 ):
            os.mkdir( self.存储文件夹 )


    def 文档信息获取( self ):
        """
        - 网址：需要爬取的百度文库文档的网址。
        - 存储文件夹：下载文件所需保存的文件夹位置，以“\\”结尾。
        """
        网页 = requests.get( self.文档网址 )
        网页.encoding = 网页.apparent_encoding
        self.文档信息分析( 网页.text )

    def 文档信息分析( self, 网页可识别源码 ):
        """
        - 网页可识别源码：人能看懂的网页源代码。
        + 更新 self.文档信息字典。
        """
        锚点 = re.compile( r'(?=WkInfo.DocInfo)[\s\S]+?(?=WkInfo.PaceInfo)' )
        匹配列表 = 锚点.findall( 网页可识别源码 )
        文档原始信息 = 匹配列表[0][16:]
        去除注释后 = re.sub( r'//[\s\S]*?\n', '', 文档原始信息 )
        去除无用函数后 = re.sub( r'\'readerVersion\'[\s\S]*?};', '}', 去除注释后 )
        删除无意义字符后 = 去除无用函数后.replace( '\n', '' ).replace( ' ', '' ).replace( '\'', '\"' ).replace( '+', '' )
        删除无效对比后 = 删除无意义字符后.replace( '||"0-0-0-0"', '' ).replace( '||0', '' ).replace( '||""', '' ).replace( '!!', '' )
        文档json字符串信息 = 删除无效对比后.replace( ',}', '}' )
        文档json信息 = json.loads( 文档json字符串信息 )
        self.文档信息字典[ "标题" ] = 文档json信息[ "title" ]
        self.文档信息字典[ "GET格式" ] = 文档json信息[ "player" ]
        self.文档信息字典[ "文档ID" ] = 文档json信息[ "docId" ]
        self.文档信息字典[ "文档格式" ] = self.文档格式字典[ 文档json信息[ "docTypeNum" ] ]
        self.文档信息字典[ "是否直接获取" ] = True if 文档json信息[ "payPrice" ]=="" or 文档json信息[ "payPrice" ]=="0" else False
        self.文档信息字典[ "总页数" ] = 文档json信息[ "totalPageNum" ]
        print( "文档信息字典建立完毕。。。" )


    def 文档内容获取( self ):
        GET网址 = self.文档信息字典[ "缺省GET网址" ] + "&doc_id=" + self.文档信息字典[ "文档ID" ] + "&type=" + self.文档信息字典[ "GET格式" ]
        #print( GET网址 )
        self.请求信息页 = requests.get( GET网址 )
        if self.请求信息页.status_code == 200:
            self.请求信息页.encoding = self.请求信息页.apparent_encoding
            if self.文档信息字典[ "GET格式" ] == "ppt":
                self.PPT获取()
            elif self.文档信息字典[ "GET格式" ] == "html":
                self.HTML获取()
            else:
                print( self.文档信息字典[ "GET格式" ] + "暂未开发。。。" )
        else:
            print( "错误 >>> 网页无法打开，状态码> " + 网页.status_code )


    def PPT获取( self ):
        self.全图获取()
        self.全图起止点确认()
        if len( self.分图起止点列表 ) == int( self.文档信息字典[ "总页数" ] ):
            self.创建存储文件夹()
            self.分图保存()
            print( "全图保存完毕。。。" )
        else:
            print( "分图页数获取错误？？？\n>>> 应有页数：" + self.文档信息字典[ "总页数" ] \
                + "\n>>> 获取页数：" + str( len(self.分图起止点列表) ) )

    def 全图获取( self, 网页源码 ):
        """
        + 更新 self.全图代码。
        """
        缺省图片下载地址 =  eval(self.请求信息页.text)[0][ "zoom" ].replace("\\/", "/").split("&png=")[0]
        for i in range(0, 100000000, 1000000):
            图片字符码 = requests.get(
                缺省图片下载地址 + "&jpg=" + str(i) + "-" + str(i+999999)
                ).content
            self.全图字符码 += 图片字符码
            if len(图片字符码)<1000:
                print( "全图获取完毕。。。共计字符量：" + str( len(self.全图字符码) ) )
                break

    def 全图起止点确认( self ):
        """
        + 更新 self.分图起止点列表。
        """
        搜索参照点 = 0
        搜索字符码 = self.全图字符码
        while True:
            相对起点 = 搜索字符码.find(b"\xff\xd8\xff\xe0\x00")
            相对终点 = 搜索字符码.find(b"\xff\xd9") + 1
            if 相对起点 == -1 or 相对终点 == 0:
                print( "全图起止点确认完毕。。。" )
                #print(self.分图起止点列表)
                return 0
            else:
                self.分图起止点列表.append( [ 搜索参照点+相对起点, 搜索参照点+相对终点 ] )
                搜索参照点 += 相对终点
                搜索字符码 = 搜索字符码[ 相对终点: ]

    def 分图保存( self ):
        for 序号, 起止点 in enumerate(self.分图起止点列表):
            with open( self.存储文件夹 + str(序号+1) + ".jpg", "wb" ) as 图:
                图.write( self.全图字符码[ 起止点[0]:起止点[1] ] )
                图.close()


    def HTML获取( self ):
        self.全请求获取()
        if len( self.文本请求地址列表 ) == int( self.文档信息字典[ "总页数" ] ):
            #self.创建存储文件夹()
            self.文本保存()
        else:
            print( "文本页数获取错误？？？\n>>> 应有页数：" + self.文档信息字典[ "总页数" ] \
                + "\n>>> 获取页数：" + str( len(self.文本请求地址列表) ) )
            self.文本保存()

    def 全请求获取( self ):
        """
        + 更新 self.文本请求地址列表。
        """
        self.文本请求地址列表 = [ x[ "pageLoadUrl" ].replace("\\/", "/") for x in eval( self.请求信息页.text )[ "json" ] ]
        print( self.文本请求地址列表 )

    def 文本保存( self ):
        文本名 = self.存储目录 + self.文档信息字典[ "标题" ] + ".txt"
        if os.path.exists( 文本名 ):
            os.remove( 文本名 )
        百页循环 = len(self.文本请求地址列表)//10
        百页剩余 = len(self.文本请求地址列表) - 百页循环*10
        for x in range( 百页循环+1 ):
            self.追加存储文本 = ""
            if x<百页循环:
                for y in range(10):
                    self.单页文本分析( x*10+y )
            else:
                for y in range( 百页剩余 ):
                    self.单页文本分析( x*10+y )
            with open( 文本名, "a", encoding='utf-8' ) as 文:
                文.write( self.追加存储文本 )
                文.close()
        print( "文本保存完毕。。。" )
        #print(self.追加存储文本)

    def 单页文本分析( self, 列表序号 ):
        原始接收数据 = requests.get( self.文本请求地址列表[ 列表序号 ] ).content
        编码接收数据 = 原始接收数据.decode('unicode_escape','ignore')
        字典化数据 = re.findall( "{.*}", 编码接收数据 )[0].replace("\"\"\"", "\"\\\"\"")
        #print( json.loads(字典化数据).keys() )
        文本主体数据 = json.loads(字典化数据)[ "body" ]
        文本列表 = [ { "分段":t["ps"], "纵向位置":t["p"]["y"], "文字":t["c"] } for t in 文本主体数据 ]
        #if 列表序号 in [0,1,2]: print( 文本主体数据 )
        #print( 文本列表 )
        for 序号, 部分文本 in enumerate( 文本列表 ):
            if ( 部分文本[ "分段" ] != None ) and ( 序号 == 0 ):
                pass
            elif ( 部分文本[ "分段" ] != None ):
                if ( "_enter" in 部分文本[ "分段" ] ):
                    self.追加存储文本 += 部分文本[ "文字" ] + 部分文本[ "分段" ][ "_enter" ] * "\n"
                else:
                    #print( 部分文本 )
                    pass
            elif ( 部分文本[ "分段" ] == None ):
                self.追加存储文本 += 部分文本[ "文字" ]





if __name__=="__main__":
    文档网址 = "https://wenku.baidu.com/view/7fa86fbb29ea81c758f5f61fb7360b4c2e3f2aca.html?from=search"
    #文档网址 = "https://wenku.baidu.com/view/6636bb78453610661ed9f46e.html?from=search"
    #文档网址 = "https://wenku.baidu.com/view/419933fd26d3240c844769eae009581b6ad9bdd4.html?from=search"
    存储目录 = ".\\"
    测试任务 = 百度文库下载( 文档网址, 存储目录 )