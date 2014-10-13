# -*-coding:utf-8-*-
__author__ = 'wujiangwei'

import json
import re
import os
import urllib2
import sys

#config file,your can change anything here
yourProjectPrefix = 'JF'        #default
yourModelBaseClassName = 'JSONModel'    #default

#here just for Baidu Nuomi
isBaiduNuomi = 0
if(isBaiduNuomi > 0):
    yourProjectPrefix = 'BDN'
    yourModelBaseClassName = 'BDNBaseJSONModel'

#not support now
ignoreKeys = ['serverstatus', 'serverlogid']

#default key for list object
#warning,if your use JFNetworkingClient,do not change this default key
defaultListKey = 'kJFObjectDefaultArrayKey'

#config file name list
jsonFileList = []   #废弃，使用实时请求的方式

#parse by get request url

def getKeyWordByUrl(url):
    ret = ''
    retList = url.split('?')
    if(len(retList) > 0):
        newStr = retList[0]
        retList = newStr.split('/')
        ret = retList[len(retList) - 1]
    return ret

def generateModelByHttpGet():
    rootPath = os.getcwd()
    content = ''
    keyWord = ''
    flag = 0
    flag = raw_input("选择输入的内容类型\n HTTP GET Url【1】\n 或者\n 返回的数据内容【2】\n")
    while (cmp('\n', flag) == 0 or len(flag) == 0):
        flag = raw_input("输入【1 == URL】【2 == JSON内容】")
    while(int(flag) != 1 and int(flag) != 2):
        flag = raw_input("类型错误，重新输入")

    flag = int(flag)
    if(flag == 1):
        getUrl = raw_input("输入完整的GET Request Url: ")
        while(len(getUrl) == 0):
            getUrl = raw_input("url为空，请重新输入")
        keyWord = getKeyWordByUrl(getUrl)
    else:
        keyWord = raw_input("输入Model名称: ")
        while(len(keyWord) == 0):
            keyWord = raw_input("model名词为空，请重新输入")
        print "输入Json内容: \n 完成后以回车结束"
        while 1:
            # 获得用户输入
            line = sys.stdin.readline()
            if (len(content) > 0 and cmp('\n', line) == 0):
                break
            else:
                line = cleanLineForJsonDecode(line)
                content = content + line

    if(len(keyWord) > 0):
        os.chdir(rootPath)


        resData = ''
        if(flag == 1):
            req = urllib2.Request(getUrl)
            res_data = urllib2.urlopen(req)
            resData = res_data.read()
        else:
            resData = content

        decodejson = json.loads(resData)

        rootPath = os.getcwd()
        try:
            os.makedirs(keyWord)
        except:
            tt = ''
        os.chdir(keyWord)

        generationFileByDict(keyWord, transferJsonToDic(decodejson), 0, 1)
        print '脚本执行结束，请复制model文件夹到您需要的地方'
    else:
        print 'model名词为空，无法从 url解析或者 未手动输入'

def cleanLineForJsonDecode(line):
    lineStr = line.strip('\n')
    lineStr = line.strip()
    if(lineStr.count(':') >= 1):
        #踢出““数据
        mLocation = lineStr.find('"')
        if(mLocation != 0):
            Location = lineStr.find(':')
            sufStr = lineStr[Location :]
            dealStr = lineStr[: Location]
            #TODO:"如果这边key已经带了""就不要加了
            dealStr = "\"" + dealStr + "\""
            lineStr = dealStr + sufStr
        lineStr.replace("'", "\"")
    return lineStr

#parse by file content
#废弃，使用generateModelByHttpGet
def startParseFiles():
    #read file content

    rootPath = os.getcwd()

    for fileName in jsonFileList:
        try:
            os.chdir(rootPath)

            fileFo = open(fileName, 'r')
            easyFileContent = ''
            for line in fileFo.readlines():
                lineStr = cleanLineForJsonDecode(line)
                easyFileContent = easyFileContent + lineStr

            decodejson = json.loads(easyFileContent)
            fileFo.close()

            childPath = 'AutoModel://' + fileName
            try:
                os.makedirs(childPath)
            except:
                tt = ''
            os.chdir(childPath)

            generationFileByDict(fileName, transferJsonToDic(decodejson), 0, 1)
        except IOError:
            print 'can not find your file named' + fileName + IOError.message

def FirstStrBigger(str):
    firStr = str[:1]
    bodyStr = str[1:]
    return firStr.title() + bodyStr

def generationFileByDict(fileName, aDict, needDicKey, needGenFile):
    print u'生成' + fileName + u'model中'
    className = ''
    if(needDicKey != 2):
        className = yourProjectPrefix + FirstStrBigger(fileName).strip() + 'JsonModel'
    else:
        className = yourProjectPrefix + FirstStrBigger(fileName).strip() + 'ItemJsonModel'

    fileName = className + '.h'

    if(needGenFile > 0):
        OjectCFile = open(fileName,'w')

    #write .h file
    #@implementation ModelResponseJsonModel
    #@end
    if(needGenFile > 0):
        mFileName = className + '.m'
        OjectCMFile = open(mFileName, 'w')
        OjectCMFile.write('//\n//Auto ' + className + '.m File \n//From Python Script Kevin\n//\n//https://github.com/wujiangwei/ModelNetworkClient\n\n')
        OjectCMFile.write('#import \"' + className + '.h\"\n\n')
        OjectCMFile.write('@implementation ' + className)
        OjectCMFile.write('\n')
        OjectCMFile.write('\n')
        OjectCMFile.write('@end')
        OjectCMFile.close()

    #define IOS Class Type
    protocol = '@protocol'
    defaultKey = 'NSString'
    IntKey = 'NSNumber'
    Strkey = 'NSString'
    ListKey = 'NSArray'

    #write .h File header
    if(needGenFile > 0):
        OjectCFile.write('//\n// Auto Create JsonModel File\n// ' + className + '.h' +  '\n//\n// Github: https://github.com/wujiangwei/ModelNetworkClient\n\n\n')
        OjectCFile.write('#import "JSONModel.h"\n')
        #need protocol
        if(needDicKey == 2):
            #@protocol albumListItemModel
            #@end
            OjectCFile.write('\n@protocol ' + className)
            OjectCFile.write('\n\n')
            OjectCFile.write('@end\n\n')

        OjectCFile.write(getHeaderFileStr(aDict))
        OjectCFile.write('\n')

        OjectCFile.write('\n\n@interface ' + className + ' : ' + yourModelBaseClassName)
        OjectCFile.write('\n\n')


    if(isinstance(aDict, list) or isinstance(aDict, tuple)):
        return ""

    for key in aDict:
        value = aDict[key]
        #@property (nonatomic, strong)NSString<Optional> *url;
        #@property (nonatomic, strong)NSNumber<Optional> *tagId;

        #@property (nonatomic, strong)NSArray<Optional, albumListItemModel> *albumList;
        #@property (nonatomic, strong)albumListItemModel<Optional> *testModel;

        if(isinstance(value, list) or isinstance(value, tuple)):
            protocolKeyJsonM = generationFileByDict(key, parseDicFromList(value), 2, 0)
            LineContent = ''
            if(len(protocolKeyJsonM) > 0):
                generationFileByDict(key, parseDicFromList(value), 2, 1)
                LineContent = '\n@property (nonatomic, strong) ' + ListKey + '<Optional, ' + protocolKeyJsonM + '> *' + key + ';\n'
            else:
                LineContent = '@property (nonatomic, strong) ' + ListKey + '<Optional> *' + key + ';\n'
            if(needGenFile > 0):
                OjectCFile.write(LineContent)
            #若是数组会加入默认key

        elif(isinstance(value, str) or isinstance(value, unicode)):
            LineContent = '@property (nonatomic, strong) ' + Strkey + '<Optional> *' + key + ';\n'
            if(needGenFile > 0):
                OjectCFile.write(LineContent)

        elif(isinstance(value, dict)):
            objectKey = generationFileByDict(key, value, 1, 1)
            LineContent = '\n@property (nonatomic, strong) ' + objectKey + '<Optional> *' + key + ';\n'
            if(needGenFile > 0):
                OjectCFile.write(LineContent)

        elif(isinstance(value, int) or isinstance(value, long) or isinstance(value, float)):
            LineContent = '@property (nonatomic, strong) ' + IntKey + '<Optional> *' + key + ';' + '\n'
            if(needGenFile > 0):
                OjectCFile.write(LineContent)

        else:
            #Null or other Object
            LineContent = '@property (nonatomic, strong) ' + Strkey + '<Optional> *' + key + ';\n'
            if(needGenFile > 0):
                OjectCFile.write(LineContent)

    if(needGenFile > 0):
        OjectCFile.write('\n')
        OjectCFile.write('@end')

        OjectCFile.close()
    return className


def getHeaderFileStr(aDict):
    importStr = ''
    if(isinstance(aDict, list) or isinstance(aDict, tuple)):
        return ""

    for key in aDict:

        value = aDict[key]
        if(isinstance(value, list) or isinstance(value, tuple)):
            protocolKeyJsonM = generationFileByDict(key, parseDicFromList(value), 2, 0)
            LineContent = ''
            if(len(protocolKeyJsonM) > 0):
                importStr = importStr + '#import "' + protocolKeyJsonM + '.h"\n'

        elif(isinstance(value, dict)):
            objectKey = generationFileByDict(key, value, 1, 1)
            importStr = importStr + '#import "' + objectKey + '.h"\n'

    return importStr


def parseDicFromList(aList):
    #the object in List,here must be Object,and not a string or int/null
    if(len(aList) <= 0):
        return {'unknow_object_type_in_listObject' : 'list is empty'}
    if(isinstance(aList[0], dict)):
        return aList[0]
    return aList

def transferJsonToDic(decodejson):
    #Array List
    if(isinstance(decodejson, list)):
        tDic = {}
        tDic[defaultListKey] = decodejson
        return tDic

    #dict
    if(isinstance(decodejson, dict)):
        return decodejson

    return {'newParseError' : 'content is invalid'}

generateModelByHttpGet()