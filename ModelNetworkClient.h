//
//  ModelNetworkClient.h
//  AppModule
//
//  Created by wujiangwei on 14-9-22.
//  Copyright (c) 2014年 Kevin. All rights reserved.
//

#import "AFNetworking.h"
#import "JSONModel.h"

#pragma mark - Define Module

//If Service just return an array, your response JSONModel can use this key to get Array
//Always, Service prefer to returning a Dic(Map/Key-Value) To Client
#define kModelNetworkDefaultArrayKey    @"modelNetworkDefaultArrayKey"

/**
 *  Http/Https response data Cache策略
 */
typedef enum : NSUInteger {
    // 不使用缓存
    URLCachePolicyNone = 0,
    // 忽略缓存 == 不适用缓存
    URLCachePolicyIgnoringLocalCacheData = URLCachePolicyNone,
    
    // 数据请求失败时(无网络时首页非空，或者某些离线策略)使用缓存
    URLCachePolicyReturnCacheDataOnError,
    
    // 先使用缓存加载 然后再请求数据刷新
    URLCachePolicyReturnCacheDataAndRequestNetwork,
    
}eURLCachePolicy;

/**
 *  Some Error
 *  Response data parse error
 */
typedef enum : NSUInteger {
    // 未知错误
    NetworkAPIHelperErrorCodeNone = 8000,
    // JSOMModel解析错误
    NetworkAPIHelperErrorCodeModelParse,
    
} NetworkAPIHelperErrorCode;

#pragma mark - Net Block

/**
 *  HTTP/HTTPs succeed block
 *  HTTP/HTTPs failed block
 */
typedef void (^BlockHTTPRequestSuccess)(AFHTTPRequestOperation *operation, id responseObject);
typedef void (^BlockHTTPRequestFailure)(AFHTTPRequestOperation *operation, NSError *error);

/**
 *  download progress block
 *  upload progress block
 */
typedef void (^BlockHTTPRequestDownloadProgress)(NSUInteger bytesRead, long long totalBytesRead, long long totalBytesExpectedToRead);
typedef void (^BlockHTTPRequestUploadProgress)(NSUInteger bytesWritten, long long totalBytesWritten, long long totalBytesExpectedToWrite);

//Net cache will support later
typedef void (^BlockHTTPRequestCache)(AFHTTPRequestOperation *operation, id responseObject, eURLCachePolicy cachePolicy);

@class ModelRequestJsonModel;
@class ModelResponseJsonModel;

/**
 *  封装HTTP请求
 *  HTTPS have not support
 */
@interface ModelNetworkClient : AFHTTPRequestOperationManager

#pragma mark - get handler
/**
 *  使用指定的BaseURL的Client
 *
 *  @return 使用指定的BaseURL的Client
 */
+ (instancetype)defaultNetClient:(NSString *)baseUrl;

#pragma mark - Debugger Tools

//是否打开log日志
- (void)setLogger:(BOOL)loggerSwitch;

/**
 *  修改BaseURL
 *  For 临时的RD QA Release Service 切换
 *  @param aURL BaseURL
 */
- (void)reloadHttpClientWithBaseURL:(NSString *)aURL;

#pragma mark - Http GET/POST Request

#pragma mark - GET

/**
 *  封装的GET请求
 *
 *  @param urlPath            请求的urlPath
 *  @param responseModelClass 解析的JSONModel
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)GET:(NSString *)urlPath
                        param:(NSDictionary *)params
                 JSONModelClass:(Class)responseModelClass
                        success:(BlockHTTPRequestSuccess)success
                        failure:(BlockHTTPRequestFailure)failure;

/**
 *  封装的GET请求
 *
 *  @param aModel             请求的参数Model，包含urlPath
 *  @param responseModelClass 解析的JSONModel
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)GETRModel:(ModelRequestJsonModel *)aModel
                 JSONModelClass:(Class)responseModelClass
                        success:(BlockHTTPRequestSuccess)success
                        failure:(BlockHTTPRequestFailure)failure;

#pragma mark - POST

/**
 *  封装的POST请求
 *
 *  @param urlPath            请求的urlPath
 *  @param responseModelClass 解析的JSONModel
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)POST:(NSString *)urlPath
                           param:(NSDictionary *)params
                  JSONModelClass:(Class)responseModelClass
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure;

/**
 *  封装的POST请求
 *
 *  @param aModel             请求和参数Model
 *  @param responseModelClass 解析的JSONModel
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)POSTRModel:(ModelRequestJsonModel *)aModel
                  JSONModelClass:(Class)responseModelClass
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure;

#pragma mark - POST Upload progress and POST Form Data

/**
 *  封装的POST请求,可以监控到上传文件的进度
 *
 *  @param urlPath            请求的urlPath
 *  @param responseModelClass 解析的JSONModel
 *  @param uploadProgress     上传进度回调
 *  @param downloadProgress   下载进度回调
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)POST:(NSURL *)urlPath
                           param:(NSDictionary *)params
                        JSONModelClass:(Class)responseModelClass
                        uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                      downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                               success:(BlockHTTPRequestSuccess)success
                               failure:(BlockHTTPRequestFailure)failure;

/**
 *  封装的POST请求,可以监控到上传文件的进度
 *
 *  @param aModel             请求和参数Model
 *  @param responseModelClass 解析的JSONModel
 *  @param uploadProgress     上传进度回调
 *  @param downloadProgress   下载进度回调
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)POSTRModel:(ModelRequestJsonModel *)aModel
                  JSONModelClass:(Class)responseModelClass
                  uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure;

//上传Form 表单
- (AFHTTPRequestOperation *)POST:(NSURL *)urlPath
                          WithFormData:(NSData *)data
                        JSONModelClass:(Class)responseModelClass
                        uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                      downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                               success:(BlockHTTPRequestSuccess)success
                               failure:(BlockHTTPRequestFailure)failure;

//上传Form 表单With RequestModel
- (AFHTTPRequestOperation *)POSTRModel:(ModelRequestJsonModel *)aModel
                    WithFormData:(NSData *)data
                  JSONModelClass:(Class)responseModelClass
                  uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure;

#pragma mark - Http with cache,The Cache base on Url and your params in your request

/**
 *  封装的GET请求
 *
 *  @param aModel             请求参数Model
 *  @param responseModelClass 解析的JSONModel
 *  @param cachePolicy        缓存策略
 *  @param onCache            获取缓存回调
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)GET:(ModelRequestJsonModel *)aModel
                 JSONModelClass:(Class)responseModelClass
                withCachePolicy:(eURLCachePolicy)cachePolicy
                        onCache:(BlockHTTPRequestCache)onCache
                        success:(BlockHTTPRequestSuccess)success
                        failure:(BlockHTTPRequestFailure)failure;

/**
 *  封装的POST请求
 *
 *  @param aModel             请求和参数Model
 *  @param responseModelClass 解析的JSONModel
 *  @param cachePolicy        缓存策略
 *  @param onCache            获取缓存回调
 *  @param success            成功回调
 *  @param failure            失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)POST:(ModelRequestJsonModel *)aModel
                  JSONModelClass:(Class)responseModelClass
                 withCachePolicy:(eURLCachePolicy)cachePolicy
                         onCache:(BlockHTTPRequestCache)onCache
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure;


#pragma mark - 基础请求发送

/**
 *  基础:根据参数发送请求
 *
 *  @param aURL       Full URL PATH
 *  @param httpMethod @"GET" or @"POST"
 *  @param responseModelClass 解析的JSONModel
 *  @param parameters 请求参数
 *  @param success    成功回调
 *  @param failure    失败回调
 *
 *  @return 已发送的request 可以为nil
 */
- (AFHTTPRequestOperation *)sendRequestForURL:(NSURL *)fullURL
                                   httpMethod:(NSString *)httpMethod
                           responseModelClass:(Class)responseModelClass
                               withParameters:(NSDictionary *)parameters
                                      success:(BlockHTTPRequestSuccess)success
                                      failure:(BlockHTTPRequestFailure)failure;

#pragma mark - Override Method

/**
 *  Override此函数，这样你所有的请求都会带有你返回的参数,LIKE - apiVersion,timestamp
 *
 *  @return  返回Dic，会加入到请求的参数中去
 */
- (NSDictionary *)commonRequestParam;

/**
 *  网络cache相关
 *  Override此函数，忽略公共参数中的一些字段，更好的做基于url MD5的网络cache
 *
 *  @return  返回Dic，会加入到请求的参数中去
 */
- (void)ignoreCacheCommonParam:(NSDictionary *)ignoreCommonDic;

/**
 *  Override此函数
 *  当你需要统一修改服务器返回的数据结构时，可以重载该方法,在把Dic映射到Model前修改Dic，给予更好的数据结构
 *  保证返回的model的结构一致性
 *  该方法需求来源于 服务器返回字段架构一致性 From Baidu Nuomi
 *
 *  @param netDic   原始网络数据转化成的Dic
 *
 *  @return  处理过的Dic
 */
+ (NSDictionary *)willParseDicToJSONModel:(NSDictionary *)netDic;

#pragma mark - Model Network Client Support Service data
/**
 *  Model解析支持的字段类型，最终都是讲这些字段解析成为Dic，然后解析为JSONModel
 *  不同字段将会使用如下的解析方式，需要特别注意 如果服务器直接返回Array的话，利用了默认的key来生成Dic
 *  NSData -> Json/Dic -> JSONModel
 *  NSDic -> JSONModel
 *  NSArray -> (default key:Array) -> Dic -> JSONModel
 */
+ (BOOL)isClassTypeSupport:(id)checkData;

#pragma mark - Model Network Client Tools

+ (NSDictionary *)dictionaryFromResponseData:(id)responseData;

+ (ModelResponseJsonModel *)JSONModelFromResponseDictionary:(NSDictionary *)dictionary
                                   withJSONModelClass:(Class)JSONModelClass
                                                error:(NSError **)error;

//default is json relate:
//`application/json` `text/json` `text/javascript`
- (void)addresponseSerializerContentTypes:(NSString *)contentType;

@end


#pragma mark - Base Request Model and Response Model

#pragma mark - Request Model
@interface ModelRequestJsonModel : JSONModel

//Url Path
@property (nonatomic, strong)NSString<Ignore> *urlPath;

//App 版本号
@property (nonatomic, strong)NSString<Optional> *appVersion;

//Service Api 版本号
@property (nonatomic, strong)NSString<Optional> *apiVersion;

//初始化   urlPath
- (id)initWithURLPath:(NSString *)ap;

@end

#pragma mark - Response Model

@interface ModelResponseJsonModel : JSONModel

//可选的公共参数
//网络错误ID 和 网络错误Message
@property (nonatomic, strong)NSString<Optional> *errorMsg;
@property (nonatomic, strong)NSNumber<Optional> *errorId;

@end

