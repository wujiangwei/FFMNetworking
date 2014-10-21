ModelNetworkClient
==================

基于AFNetworking和JSONModel整合的IOS ModelNetworkClient(JFNetworkClient)
最低支持IOS 6.0的开发
（项目来自于 百度团购团队，经历了2次重构（一次百度团购、一次百度糯米）产生的网络框架，再整理后分享给大家）

依赖外部模块：
  AFNetworking（2.x+）
  JSONModel
  
(使用ModelNetworkClient前，你应该去了解JSONModel，这样可以更好的使用本模块)




ModelNetworkClient 主要提供以下功能：

  1.把网络返回数据（NSData、NSArray、NSDictionary）自动转化成JSONObject，方便外部模块的使用
  
  2.提供Python脚本，帮你自动生成服务器返回的数据 JSONModel的.h和.m文件，
  
    **** 使用方法 ****
        
        1. 打开终端，输入命令
           cd + modelShell的目录
           
        2. 输入命令
           python AutoJSONModelShell.py
           
        3. 根据提示输入相关内容：【1】Full GET Url 【2】Json Content
        
        4. model成功生成到和AutoJSONModelShell.py同级目录下
    
    
        IOSModelParse.py 文件中可修改以下配置项：
      
        yourProjectPrefix = 'JF'                //你的工程Prefix
        
        yourModelBaseClassName = 'JSONModel'    //所有model的继承类名，默认用JSONModel
        
        
    **** 注意事项 ****
    
        1.Get Url 返回的空字段，比如 空的dic/array 你都需要手动补充具体的model
        
        2.若不同模块的model需要复用，需要互相协商
        
        3.注意补全不完整model（给予生成model的数据完整，则model完成）
        
        

  3.后续可能会考虑把请求（RequestModel）也封装到脚本中去，可以给我一些意见 QQ:461647731
  
  
  4.如何使用本模块
    
    **** ModelNetworkClient 使用方法 ****
    
    （可选）你可以定制自己的NetClient，如果需要的话：
    
    如果你需要加入baseUrl 你需要继承ModelNetworkClient，并且重写以下方法
    
        + (NSString *)baseUrl
        {
            //返回你的baseUrl
            return @"http://example.com/";
        }
        
        
    如果需要打开本模块日志，重写以下方法
    
        - (id)initWithBaseURL:(NSURL *)url
        {
            self = [super initWithBaseURL:url];
            if (self) {
                //增加返回的content type类型，适合用个人开发者的简易服务器
                [self addresponseSerializerContentTypes:@"text/html"];
                //打开日志
                [self setLogger:YES];
            }
    
            return self;
        }
        
        
    如果你需要往你所有的请求中添加公共参数，重写以下方法
    
        - (NSDictionary *)commonRequestParam
        {
        	return nil;
        }
    
    
    **** 网络请求 使用方法 ****
    
    **** **** **** **** **** ****
    
    和AFNetworking一样使用，参见https://github.com/AFNetworking/AFNetworking
    
    Get Request（AFNetworking）
    
    //基本请求：返回基本数据
    
    ModelNetworkClient *manager = [ModelNetworkClient manager];
    [manager GET:@"http://example.com/resources.json" parameters:nil success:^(AFHTTPRequestOperation *operation, id         responseObject) {
        NSLog(@"JSON: %@", responseObject);
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        NSLog(@"Error: %@", error);
    }];
    
    
    **** **** **** **** ****
    
    //优化的请求：返回你用脚本生成的model
    
    [[ModelNetworkClient defaultNetClient] GET:@"http://example.com/resources.json" JSONModelClass:[HomeResonseModel class] success:^(AFHTTPRequestOperation *operation, id responseObject) {
    
        //此时返回给你的，是已经自动填充好的HomeResonseModel Class对象
        //你可以在任何地方直接使用该对象，无需objectForKey
        //而homeListItemJsonModel，你可以用做刷新你的cell的数据源
        
        NSLog(@"JSONModel: %@", responseObject);
        
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
    
        NSLog(@"Error: %@", error);
        
    }];
    
    **** **** **** **** ****
    
    //进一步细化的请求：使用requestModel
    [[ModelNetworkClient defaultNetClient] GETRModel:HomeRequestModel JSONModelClass:[HomeResonseModel class]                success:^(AFHTTPRequestOperation *operation, id responseObject) {
    
        //此时返回给你的，是已经自动填充好的HomeResonseModel Class对象
        //你可以在任何地方直接使用该对象，无需objectForKey
        NSLog(@"JSONModel: %@", responseObject);
        
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
    
        NSLog(@"Error: %@", error);
        
    }];
    
    
    **** **** 一些进阶说明 **** ****
    
    //如果客户端协议简单，推荐直接使用url
    
    （可选）
    
    //什么情况下推荐使用requestModel
    
      //当你的请求比较复杂时，比如，所有的客户端请求都需要带Api版本号，App版本号，定位信息时。
    
      //此时你可以定义一个BaseRequestModel,在这个里面写好公共请求参数
    
      //你的其他model，都继承于BaseRequestModel，然后加上每个请求特有的参数
    
  
    POST Requet
    
    和GET大同小异
  
  
  
  
  （可选）一些细节功能描述
  
  1.封装App网络请求的公共参数，对于一个App来讲，大部分时候服务器都会规定一些基础（公共参数：appVersion、apiVersion、location、userId），App端需要每个接口都传递这些参数，ModelNetworkClient对此进行了封装，可以在重载相关函数，快速实现该功能
  
  2.提供Http请求数据的缓存功能，该缓存基于你的请求path（实现中）
    该功能主要用于 
    
    a.提升App的离线使用体验  
    
    b.为你的App提供一些离线功能（比如 我的糯米券、美团券、其他需要缓存的离线信息）
    
  你可以定制你的path产生字段
  
  比如：当你的请求中 存在 timestamps时，每次基于path产生的缓存路径都会不一样，所以此时的缓存是无效的，你需要在产生path前，让类似于timestamps这种字段设置为忽略，这样cache path就不会包含这个字段
  
  3.如果你的服务器返回的数据是框架性的数据，使用JSONModel起来需要重复的建立很多文件，本模块提供了数据预处理
  
  
  **** JSONModel 说明 ****
  
  很细节全面的讲解~
  http://blog.csdn.net/u013368288/article/details/23887257
