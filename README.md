ModelNetworkClient
==================

基于AFNetworking和JSONModel整合的IOS ModelNetworkClient
最低支持IOS 6.0的开发

（项目来自于 百度团购团队，经历了2次重构（一次百度团购、一次百度糯米）产生的网络框架，再整理后分享给大家）

依赖外部模块：
  AFNetworking（2.x+）
  JSONModel
  
使用ModelNetworkClient前，你应该去了解JSONModel，这样可以更好的使用本模块

ModelNetworkClient 主要提供以下功能：

  1.把网络返回数据（NSData、NSArray、NSDictionary）自动转化成JSONObject，方便外部模块的使用
  
  （可选）功能
  
  2.封装App网络请求的公共参数，对于一个App来讲，大部分时候服务器都会规定一些基础（公共参数：appVersion、apiVersion、location、userId），App端需要每个接口都传递这些参数，ModelNetworkClient对此进行了封装，可以在重载相关函数，快速实现该功能
  
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
  
  4.提供Http请求数据的缓存功能，该缓存基于你的请求path
    该功能主要用于 
    
    a.提升App的离线使用体验  
    
    b.为你的App提供一些离线功能（比如 我的糯米券、美团券、其他需要缓存的离线信息）
    
  你可以定制你的path产生字段
  
  比如：当你的请求中 存在 timestamps时，每次基于path产生的缓存路径都会不一样，所以此时的缓存是无效的，你需要在产生path前，让类似于timestamps这种字段设置为忽略，这样cache path就不会包含这个字段
  
  
