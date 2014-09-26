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
  
  2.提供Python脚本，帮你自动生成服务器返回的数据 Model的.h和.m文件，
    脚本使用方法：
    
        IOSModelParse.py 文件中 修改以下配置项：
      

        yourProjectPrefix = 'JF'                //你的工程Prefix
        
        yourModelBaseClassName = 'JSONModel'    //所有model的继承类名，默认用JSONModel
        
        
        被解析的文件说明：（请仔细阅读）
        
        //需要解析的文件，注意：和IOSModelParse.py放在同级目录
        
        //文件内容来自：
        
            //把Api服务器的网址 比如:http://1.stormofheros.sinaapp.com/searchPic/key校园
            
            //把网址输入到浏览器中（浏览器需要有类似于JsonView的JSON插件）然后 复制此时浏览器返回的数据，
                如果数据没JSON格式化，你可以到http://bejson.com/网站上格式化，拷贝格式化后的数据，内容粘贴到fileOne文件中
                
            //为何必须要格式化：因为目前脚本是按行来解析，所以需要每一行一个 key:value，不能一行有多个key:value
            
                    //对的格式 {testKey1:'value1'}
                    //错误的格式{testKey1:'value1', testKey2:'value2'}
            //另外本解析生成器暂时不支持文件中有非常规字符（中文支持），比如
            
                    //src=http%3A%2F%2Fnuomi.xnimg.cn%2Fupload%2Fdeal%2F2014%2F6%2FV_L%2F1090022-axzfscrqei-11485054760212511.jpg&quality=80&width=470&height=285
                    
                    //所以如果你们的服务器返回了一些类似于这样的url，请把对用key的value删除后，再使用本脚本
                    
                    //解析器的关键是使用对应的key
                    
                    //对应一些无类型的解析字段，会给予new_error_list_empty的property名字，方便你把生成model放入工程时有相关的编译提示
        //配置文件内容            
        jsonFileList = ['fileOne', 'fileTwo', ...]     
        
        

  3.后续可能会考虑把请求也封装到脚本中去，可以给我一些意见 QQ:461647731
  
  
  4.如何使用本模块
  
    （可选）你可以定制话自己的NetClient，如果需要的话：
    
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
        
        
    如果你需要往你所有的请求中添加公共参数，重新以下方法
    
        - (NSDictionary *)commonRequestParam
        {
        	return nil;
        }
        
        
    以下2个方法，请见具体文件说明
    
    + (NSDictionary *)willParseDicToJSONModel:(NSDictionary *)netDic
    
    - (void)ignoreCacheCommonParam:(NSDictionary *)ignoreCommonDic
    
    
    
    简单使用本模块
    
    和AFNetworking一样使用，参见https://github.com/AFNetworking/AFNetworking
    
    
    Get Request
    
    //基本请求
    
    ModelNetworkClient *manager = [ModelNetworkClient manager];
    [manager GET:@"http://example.com/resources.json" parameters:nil success:^(AFHTTPRequestOperation *operation, id         responseObject) {
        NSLog(@"JSON: %@", responseObject);
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        NSLog(@"Error: %@", error);
    }];
    
    //Model化请求
    
    //JSONModel讲解：Optional 代表这个字段，服务器可以不返回，Ignore 代表反射时，忽略该字段，如果什么都不写，就是服务器必须返回这个字段（这样是不好的，会让客户端出现异常，除非服务器可以保证）
    
    1.定义你的返回Model：HomeResonseModel:
    
    @interface HomeResonseModel : BaseResponseJsonModel

    @property (nonatomic, strong)NSNumber<Optional> *errorId;   //number类型
    @property (nonatomic, strong)NSString<Optional> *homeString;//字符串
    @property (nonatomic, strong)homeListItemJsonModel<Optional> *homeObject;   //对象
    //协议homeListItemJsonModel，代表了，这个数组里的对象是什么
    //如果是基本类型，无需写homeListItemJsonModel，但是你要知道是NSNumber还是NSString~
    @property (nonatomic, strong)NSArray<Optional, homeListItemJsonModel> *homeList;    //数组

    @end
    
    @implementation HomeResonseModel

    //假数据测试代码
    - (NSString *)homeString
    {
        //当你需要伪造一些测试数据时，无需去找服务器修改字段
        //直接在model此处，写上你的本地测试数据
        //记得测试完毕后，删除该代码。
    
        //你也可以自定义数据的返回内容,根据原来的数据~
        return @“测试数据”;
    }
    @end
    
    //homeListItemJsonModel 对象
    @interface homeListItemJsonModel : JSONModel
    @property (nonatomic, strong)NSString<Optional> *imageUrl;
    @property (nonatomic, strong)NSNumber<Optional> *tagId;
    @end

    //这个请求完整地址为 http://example.com/resources.json， http://example.com为baseUrl，参见上文
    (可选)2.ModelRequestJsonModel *HomeRequestModel = [[ModelRequestJsonModel alloc] initWithURLPath:@"resources.json"];
    3.发起请求
    //直接使用url
    //不使用requestMode
    [[ModelNetworkClient defaultNetClient] GET:@"http://example.com/resources.json" JSONModelClass:[HomeResonseModel class] success:^(AFHTTPRequestOperation *operation, id responseObject) {
        //此时返回给你的，是已经自动填充好的HomeResonseModel Class对象
        //你可以在任何地方直接使用该对象，无需objectForKey
        //而homeListItemJsonModel，你可以用做刷新你的cell的数据源
        NSLog(@"JSONModel: %@", responseObject);
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        NSLog(@"Error: %@", error);
    }];
    
    //使用requestModel
    [[ModelNetworkClient defaultNetClient] GETRModel:HomeRequestModel JSONModelClass:[HomeResonseModel class]                success:^(AFHTTPRequestOperation *operation, id responseObject) {
        //此时返回给你的，是已经自动填充好的HomeResonseModel Class对象
        //你可以在任何地方直接使用该对象，无需objectForKey
        //当HomeResonseModel Class对象有一个数组Array的时，他
        NSLog(@"JSONModel: %@", responseObject);
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        NSLog(@"Error: %@", error);
    }];
    
    //如果客户端协议简单，推荐直接使用url
    
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
  
    3.如果你的服务器返回的数据是框架性的数据，使用JSONModel起来需要重复的建立很多文件，本模块提供了数据预处理，比如服务器统一返回如下字段
  
  {
  
    "errorId":0,
    
    'errorMessage':"message",
    
    'data':DataObject
    
  } 
  你可以把这3个字段处理到同级JSONModel目录
  
  {
  
    "errorId":0,
    
    'errorMessage':"message",
    
    //其他返回字段对象，去除了data层的包装，节约JSONModel文件建立的工作量
    
  } 
  
  
