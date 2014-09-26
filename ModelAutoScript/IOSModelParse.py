# -*-coding:utf-8-*-
__author__ = 'wujiangwei'

import json
import re

#config file,your can change anything here
yourProjectPrefix = 'JF'        #default
yourModelBaseClassName = 'JSONModel'    #default

jsonFileList = ['homePicJsonStr']

IOSPlatform = 1
AndroidPlatform = 0

#default key for list object
#warning,if your use JFNetworkingClient,do not change this default key
defaultListKey = 'kJFObjectDefaultArrayKey'

def startParseFiles():
    #read file content
    for fileName in jsonFileList:
        try:
            fileFo = open(fileName, 'r')
            easyFileContent = ''
            for line in fileFo.readlines():
                addPreSuf = ':'
                lineStr = line.strip('\n')
                lineStr = line.strip()
                if(lineStr.count(addPreSuf) >= 1):
                    Location = lineStr.find(addPreSuf)
                    sufStr = lineStr[Location :]
                    dealStr = lineStr[: Location]
                    #TODO:"如果这边key已经带了""就不要加了
                    dealStr = "\"" + dealStr + "\""
                    lineStr = dealStr + sufStr
                    #额外不规则数据的处理
                    lineStr.replace("'", "\"")
                easyFileContent = easyFileContent + lineStr

            easyFileContent = re.sub(r"(,?)(\w+?)\s*?:\s*(?='|\d|\[|{)", r"\1'\2':", easyFileContent)
            decodejson = json.loads(easyFileContent)
            fileFo.close()

            generationFileByDict(fileName, transferJsonToDic(decodejson), 0)
        except IOError:
            print 'can not find your file named' + fileName + IOError.message

def FirstStrBigger(str):
    firStr = str[:1]
    bodyStr = str[1:]
    return firStr.title() + bodyStr

def generationFileByDict(fileName, aDict, needDicKey):
    className = ''
    if(needDicKey != 2):
        className = yourProjectPrefix + FirstStrBigger(fileName).strip() + 'JsonModel'
    else:
        className = yourProjectPrefix + FirstStrBigger(fileName).strip() + 'ItemJsonModel'

    if(IOSPlatform):
        fileName = className + '.h'
    else:
        fileName = className + '.java'

    OjectCFile = open(fileName,'w')

    if(IOSPlatform > 0):
        #write .h file
        #@implementation ModelResponseJsonModel
        #@end
        mFileName = className + '.m'
        OjectCMFile = open(mFileName, 'w')
        OjectCMFile.write('//\n//Auto ' + className + '.m File \n//From Python Script Kevin\n//\n//https://github.com/wujiangwei/ModelNetworkClient\n\n')
        OjectCMFile.write('#import \"' + className + '.h\"\n\n')
        OjectCMFile.write('@implementation ' + className)
        OjectCMFile.write('\n')
        OjectCMFile.write('\n')
        OjectCMFile.write('@end')
        OjectCMFile.close()

    #...
        protocol = ''
        #default type
        defaultKey = ''
        #object type
        IntKey = ''
        Strkey = ''
        ListKey = ''

        #IOS
        if(IOSPlatform):
            #define IOS Class Type
            protocol = '@protocol'
            defaultKey = 'NSString'
            IntKey = 'NSNumber'
            Strkey = 'NSString'
            ListKey = 'NSArray'

            #write .h File header
            OjectCFile.write('//\n// Auto Create JsonModel File\n// ' + className + '.h' +  '\n//\n// Github: https://github.com/wujiangwei/ModelNetworkClient\n\n\n')
            OjectCFile.write('#import "JSONModel.h"\n')
            #need protocol
            if(needDicKey == 2):
                #@protocol albumListItemModel
                #@end
                OjectCFile.write('\n@protocol ' + className)
                OjectCFile.write('\n\n')
                OjectCFile.write('@end')

            OjectCFile.write('\n\n@interface ' + className + ' : ' + yourModelBaseClassName)
            OjectCFile.write('\n\n')

        else:
            #Android
            protocol = 'implements'
            #TODO For Android:

    if(isinstance(aDict, list) or isinstance(aDict, tuple)):
        return ""

    for key in aDict:
        print "aDict[%s] =" %key, aDict[key]
        value = aDict[key]
        #@property (nonatomic, strong)NSString<Optional> *url;
        #@property (nonatomic, strong)NSNumber<Optional> *tagId;

        #@property (nonatomic, strong)NSArray<Optional, albumListItemModel> *albumList;
        #@property (nonatomic, strong)albumListItemModel<Optional> *testModel;

        if(isinstance(value, list) or isinstance(value, tuple)):
            protocolKeyJsonM = generationFileByDict(key, parseDicFromList(value), 2)
            LineContent = ''
            if(len(protocolKeyJsonM) > 0):
                LineContent = '\n@property (nonatomic, strong) ' + ListKey + '<Optional, ' + protocolKeyJsonM + '> *' + key + ';\n'
            else:
                LineContent = '@property (nonatomic, strong) ' + ListKey + '<Optional> *' + key + ';\n'
            OjectCFile.write(LineContent)
            #若是数组会加入默认key

        elif(isinstance(value, str) or isinstance(value, unicode)):
            LineContent = '@property (nonatomic, strong) ' + Strkey + '<Optional> *' + key + ';\n'
            OjectCFile.write(LineContent)

        elif(isinstance(value, dict)):
            objectKey = generationFileByDict(key, value, 1)
            LineContent = '\n@property (nonatomic, strong) ' + objectKey + '<Optional> *' + key + ';\n'
            OjectCFile.write(LineContent)

        elif(isinstance(value, int) or isinstance(value, long) or isinstance(value, float)):
            LineContent = '@property (nonatomic, strong) ' + IntKey + '<Optional> *' + key + ';' + '\n'
            OjectCFile.write(LineContent)

        else:
            #Null or other Object
            LineContent = '@property (nonatomic, strong) ' + Strkey + '<Optional> *' + key + ';\n'
            OjectCFile.write(LineContent)

    OjectCFile.write('\n')
    OjectCFile.write('@end')

    OjectCFile.close()
    return className


def parseDicFromList(aList):
    #the object in List,here must be Object,and not a string or int/null
    if(len(aList) <= 0):
        return {'new_error_list_empty_write_model_yourself' : 'list is empty'}
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


startParseFiles()