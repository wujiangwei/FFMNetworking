//
//  ModelNetworkClient.m
//  AppModule
//
//  Created by wujiangwei on 14-9-22.
//  Copyright (c) 2014年 Kevin. All rights reserved.
//

#import "ModelNetworkClient.h"

NSString *const kNetworkDataParseErrorDomain = @"ModelNetworkClient.JSON.PARSE.ERROR";

static ModelNetworkClient *__helper = nil;

@interface ModelNetworkClient()
{
    BOOL _isOpenLogger;
}

@end

@implementation ModelNetworkClient

#pragma mark - handler

+ (instancetype)defaultNetClient:(NSString *)baseUrl {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        __helper = [[self alloc] initWithBaseURL:[NSURL URLWithString:baseUrl]];
    });
    return __helper;
}

#pragma mark - Debugger Tools

- (void)setLogger:(BOOL)loggerSwitch
{
    _isOpenLogger = loggerSwitch;
}

- (void)reloadHttpClientWithBaseURL:(NSString *)aURL {
    __helper = [[ModelNetworkClient alloc] initWithBaseURL:[NSURL URLWithString:aURL]];
}

#pragma mark - Http GET and POST

#pragma mark - POST

- (AFHTTPRequestOperation *)GET:(NSString *)urlPath
                          param:(NSDictionary *)params
                 JSONModelClass:(Class)responseModelClass
                        success:(BlockHTTPRequestSuccess)success
                        failure:(BlockHTTPRequestFailure)failure
{
    NSURL *fullUrl = [NSURL URLWithString:urlPath relativeToURL:self.baseURL];
    return [self sendRequestForURL:fullUrl httpMethod:@"GET" responseModelClass:responseModelClass withParameters:params success:success failure:failure];
}

- (AFHTTPRequestOperation *)GETRModel:(ModelRequestJsonModel *)aModel
                 JSONModelClass:(Class)responseModelClass
                        success:(BlockHTTPRequestSuccess)success
                        failure:(BlockHTTPRequestFailure)failure
{
    NSURL *fullUrl = [NSURL URLWithString:aModel.urlPath relativeToURL:self.baseURL];
    return [self sendRequestForURL:fullUrl httpMethod:@"GET" responseModelClass:responseModelClass withParameters:[aModel toDictionary] success:success failure:failure];
}

#pragma mark - POST

- (AFHTTPRequestOperation *)POST:(NSString *)urlPath
                            param:(NSDictionary *)params
                  JSONModelClass:(Class)responseModelClass
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure
{
    NSURL *fullUrl = [NSURL URLWithString:urlPath relativeToURL:self.baseURL];
    return [self sendRequestForURL:fullUrl httpMethod:@"POST" responseModelClass:responseModelClass withParameters:params success:success failure:failure];
}

- (AFHTTPRequestOperation *)POSTRModel:(ModelRequestJsonModel *)aModel
                  JSONModelClass:(Class)responseModelClass
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure
{
    NSURL *fullUrl = [NSURL URLWithString:aModel.urlPath relativeToURL:self.baseURL];
    return [self sendRequestForURL:fullUrl httpMethod:@"POST" responseModelClass:responseModelClass withParameters:[aModel toDictionary] success:success failure:failure];
}

#pragma mark - POST Upload progress and POST Form Data

- (AFHTTPRequestOperation *)POST:(ModelRequestJsonModel *)aModel
                           param:(NSDictionary *)params
                  JSONModelClass:(Class)responseModelClass
                  uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure
{
    NSAssert(0, @"do not support now");
    return nil;
}

- (AFHTTPRequestOperation *)POSTRModel:(ModelRequestJsonModel *)aModel
                        JSONModelClass:(Class)responseModelClass
                        uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                      downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                               success:(BlockHTTPRequestSuccess)success
                               failure:(BlockHTTPRequestFailure)failure
{
    NSAssert(0, @"do not support now");
    return nil;
}

//上传Form 表单
- (AFHTTPRequestOperation *)POST:(ModelRequestJsonModel *)aModel
                    WithFormData:(NSData *)data
                  JSONModelClass:(Class)responseModelClass
                  uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                         success:(BlockHTTPRequestSuccess)success
                         failure:(BlockHTTPRequestFailure)failure
{
    NSAssert(0, @"do not support now");
    return nil;
}

- (AFHTTPRequestOperation *)POSTRModel:(ModelRequestJsonModel *)aModel
                          WithFormData:(NSData *)data
                        JSONModelClass:(Class)responseModelClass
                        uploadProgress:(BlockHTTPRequestUploadProgress)uploadProgress
                      downloadProgress:(BlockHTTPRequestDownloadProgress)downloadProgress
                               success:(BlockHTTPRequestSuccess)success
                               failure:(BlockHTTPRequestFailure)failure
{
    NSAssert(0, @"do not support now");
    return nil;
}

#pragma mark - Http with cache

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
                         failure:(BlockHTTPRequestFailure)failure
{
    NSAssert(0, @"do not support now");
    return nil;
}

/**
 *  封装的GET请求
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
- (AFHTTPRequestOperation *)GET:(ModelRequestJsonModel *)aModel
                 JSONModelClass:(Class)responseModelClass
                withCachePolicy:(eURLCachePolicy)cachePolicy
                        onCache:(BlockHTTPRequestCache)onCache
                        success:(BlockHTTPRequestSuccess)success
                        failure:(BlockHTTPRequestFailure)failure
{
    NSAssert(0, @"do not support now");
    return nil;
}

#pragma mark - 基础Http请求

- (AFHTTPRequestOperation *)sendRequestForURL:(NSURL *)aURL httpMethod:(NSString *)httpMethod responseModelClass:(Class)responseModelClass withParameters:(NSDictionary *)parameters success:(BlockHTTPRequestSuccess)success failure:(BlockHTTPRequestFailure)failure
{
    //Add public HTTP params
    NSMutableDictionary *dictionary = [NSMutableDictionary dictionary];
    NSDictionary *commonParam = [self commonRequestParam];
    [dictionary addEntriesFromDictionary:commonParam];
    //相同key会用户参数会覆盖公共参数
    [dictionary addEntriesFromDictionary:parameters];
    
    NSError *reError = nil;
    NSURLRequest *request = [self.requestSerializer requestWithMethod:httpMethod URLString:[aURL absoluteString] parameters:dictionary error:&reError];
    NSAssert(reError == nil, @"get request error:Url = %@ Method = %@ param = %@", aURL, httpMethod, parameters);
    
    _isOpenLogger == YES ? NSLog(@"***** urlRequest %@ *****", request) : nil;
    
    AFHTTPRequestOperation *operation = [self HTTPRequestOperationWithRequest:request success:^(AFHTTPRequestOperation *operation, id responseObject) {
        NSError *error = nil;
        
        ModelResponseJsonModel *responseModel = [ModelNetworkClient JSONModelFromResponseDictionary:[ModelNetworkClient dictionaryFromResponseData:responseObject] withJSONModelClass:responseModelClass error:&error];
        if (error == nil && success && responseModelClass != nil) {
            success(operation, responseModel);
        }else{
            failure(operation, error);
        }
        
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        if (failure) {
            failure(operation, error);
        }
    }];
    if (operation != nil) {
        [self.operationQueue addOperation:operation];
    }else{
        NSLog(@"error operation = nil");
    }
    
    return operation;
}

#pragma mark - Override Method

- (NSDictionary *)commonRequestParam
{
    //Base Class Method do nothing
    //Like Timestamps
        //[dictionary setObject:[NSString stringWithFormat:@"%.0f", [[NSDate date] timeIntervalSince1970] * 1000] forKey:@"timestamp"];
    return nil;
}

+ (NSDictionary *)willParseDicToJSONModel:(NSDictionary *)netDic
{
    //Base Class Method do nothing
    return netDic;
}

- (void)ignoreCacheCommonParam:(NSDictionary *)ignoreCommonDic;
{
    //Base Class Method do nothing
    return;
}

#pragma mark - Model Network Client Support Service data

+ (BOOL)isClassTypeSupport:(id)checkData
{
    if ([checkData isKindOfClass:[NSData class]] ||
        [checkData isKindOfClass:[NSDictionary class]] ||
        [checkData isKindOfClass:[NSArray class]]) {
        return YES;
    }
    
    return NO;
}

#pragma mark - Model Network Client Tools

+ (NSDictionary *)dictionaryFromResponseData:(id)responseData {
    
    if ([ModelNetworkClient isClassTypeSupport:responseData] == NO) {
        return nil;
    }
    
    if ([responseData isKindOfClass:[NSData class]]) {
        return [NSJSONSerialization JSONObjectWithData:responseData options:0 error:NULL];
    }
    
    if ([responseData isKindOfClass:[NSDictionary class]]) {
        return (NSDictionary *)responseData;
    }
    
    if ([responseData isKindOfClass:[NSArray class]]) {
        NSMutableDictionary *mDic = [[NSMutableDictionary alloc] initWithCapacity:1];
        [mDic setObject:responseData forKey:kModelNetworkDefaultArrayKey];
        return mDic;
    }
    
    return nil;
}

+ (ModelResponseJsonModel *)JSONModelFromResponseDictionary:(NSDictionary *)dictionary
                                   withJSONModelClass:(Class)JSONModelClass
                                                error:(NSError **)error {
    
    ModelResponseJsonModel *aModel = nil;
    
    @try
    {
        //如何需要特殊处理服务器返回的数据结构，在此处处理
        NSDictionary *dealedDic = [ModelNetworkClient willParseDicToJSONModel:dictionary];
        
        aModel = [(ModelResponseJsonModel *)[JSONModelClass alloc] initWithDictionary:dealedDic error:error];
    }
    @catch (NSException *exception) {
        *error = [NSError errorWithDomain:kNetworkDataParseErrorDomain
                                     code:NetworkAPIHelperErrorCodeModelParse
                                 userInfo:@{
                                            NSLocalizedDescriptionKey: @"JSONModel解析错误[数据类型不匹配]"
                                            }];
    }
    @finally {
    }
    
    return aModel;
}

- (void)addresponseSerializerContentTypes:(NSString *)contentType
{
    NSMutableSet *nSet = [NSMutableSet setWithSet:self.responseSerializer.acceptableContentTypes];
    [nSet addObject:contentType];
    [self.responseSerializer setAcceptableContentTypes:nSet];
}

#pragma mark - Http Cache Module

- (NSString *)urlMD5
{
    return nil;
}

- (void)cacheResponse:(NSDictionary *)responseDic
{
    //
}

- (NSDictionary *)readResponse:(NSURLRequest *)urlRequest
{
    [urlRequest.URL absoluteString];
    return nil;
}

@end

#pragma mark - Base Request Model and Response Model

#pragma mark - Request Model

@implementation ModelRequestJsonModel

- (id)initWithURLPath:(NSString *)ap
{
    self = [super init];
    if (self != nil) {
        self.urlPath = ap;
    }
    
    return self;
}

@end

#pragma mark - Response Model

@implementation ModelResponseJsonModel

@end
