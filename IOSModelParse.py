# -*-coding:utf-8-*-
__author__ = 'wujiangwei'

import json

#config file,your can change anything here
yourProjectPrefix = 'JF'        #default
yourModelBaseClassName = 'JSONModel'    #default

jsonFileList = ['homePicJsonStr']

IOSPlatform = 1
AndroidPlatform = 0

#default key for list object
#warning,if your use JFNetworkingClient,do not change this default key
defaultListKey = 'kJFObjectDefaultArrayKey'
defaultSubObjectKey = 'kSubModelDefaultObjectKey'

def startParseFiles():
    #read file content
    for fileName in jsonFileList:
        try:
            fileFo = open(fileName, 'r')
            easyFileContent = ''
            for line in fileFo.readlines():
                addPreSuf = ':'
                lineStr = line.strip('\n')
                if(lineStr.count(addPreSuf) >= 1):
                    Location = lineStr.find(addPreSuf)
                    sufStr = lineStr[Location :]
                    dealStr = lineStr[: Location]
                    dealStr = "\"" + dealStr + "\""
                    lineStr = dealStr + sufStr
                else:
                    print 'please enter json format string'
                easyFileContent = easyFileContent + lineStr

            decodejson = json.loads(easyFileContent)
            fileFo.close()

            generationFileByDict(fileName, transferJsonToDic(decodejson), 0)
        except IOError:
            print 'can not find your file named' + fileName + IOError.message
        except ValueError:
            print ValueError.message

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
        OjectCMFile.write('////Auto ' + className + '.m File by Python Script,Kevin\n\n\n')
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
            OjectCFile.write('////Auto ' + className + '.h File by Python Script,Kevin\n\n\n\n')
            OjectCFile.write('#import "JSONModel.h"\n\n')
            #need protocol
            if(needDicKey == 2):
                #@protocol albumListItemModel
                #@end
                OjectCFile.write('@protocol ' + className)
                OjectCFile.write('\n')
                OjectCFile.write('@end\n\n')

            OjectCFile.write('@interface ' + className + ' : ' + yourModelBaseClassName)
            OjectCFile.write('\n')
            OjectCFile.write('\n')
        else:
            #Android
            protocol = 'implements'
            #TODO For Android:

    for key in aDict:
        print "aDict[%s] =" %key, aDict[key]
        value = aDict[key]
        #@property (nonatomic, strong)NSString<Optional> *url;
        #@property (nonatomic, strong)NSNumber<Optional> *tagId;

        #@property (nonatomic, strong)NSArray<Optional, albumListItemModel> *albumList;
        #@property (nonatomic, strong)albumListItemModel<Optional> *testModel;

        if(isinstance(value, list) or isinstance(value, tuple)):

            protocolKeyJsonM = generationFileByDict(key, parseDicFromList(value), 2)
            LineContent = '@property (nonatomic, strong) ' + ListKey + '<Optional, ' + protocolKeyJsonM + '> *' + key + ';'
            OjectCFile.write('\n')
            OjectCFile.write('\n')
            OjectCFile.write(LineContent)
            OjectCFile.write('\n')
            OjectCFile.write('\n')
            #深度遍历,目前只支持 Dic，如果是其他单对象，请联系461647731修改
            #以后会加入默认key


        elif(isinstance(value, str) or isinstance(value, unicode)):
            LineContent = '@property (nonatomic, strong) ' + Strkey + '<Optional> *' + key + ';'
            OjectCFile.write('\n')
            OjectCFile.write(LineContent)
            OjectCFile.write('\n')

        elif(isinstance(value, dict)):
            objectKey = generationFileByDict(key, value, 1)
            OjectCFile.write('\n')
            OjectCFile.write('\n')
            LineContent = '@property (nonatomic, strong) ' + objectKey + '<Optional> *' + key + ';'
            OjectCFile.write(LineContent)
            OjectCFile.write('\n')
            OjectCFile.write('\n')

        elif(isinstance(value, int) or isinstance(value, long) or isinstance(value, float) or \
                   isinstance(value, False) or isinstance(value, True)):
            LineContent = '\n@property (nonatomic, strong) ' + IntKey + '<Optional> *' + key + ';' + '\n'
            OjectCFile.write(LineContent)

        else:
            #Null or other Object
            LineContent = '@property (nonatomic, strong) ' + Strkey + '<Optional> *' + key + ';'
            OjectCFile.write('\n')
            OjectCFile.write(LineContent)
            OjectCFile.write('\n')

    OjectCFile.write('\n')
    OjectCFile.write('\n')
    OjectCFile.write('@end')

    OjectCFile.close()
    return className


def parseDicFromList(aList):
    #the object in List,here must be Object,and not a string or int/null
    if(not (isinstance(aList, list) or isinstance(aList, tuple))):
        return {'new_error' : 'not list'}

    if(len(aList) <= 0):
        return {'new_error' : 'list is empty'}
    if(isinstance(aList[0], dict)):
        return aList[0]
    return {defaultSubObjectKey : aList[0]}

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