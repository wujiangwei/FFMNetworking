Pod::Spec.new do |spec|
spec.name         = 'ModelNetworkClient'
spec.version      = '3.1.0'
spec.license      = { :type => 'MIT' }
spec.platform     = :ios
spec.homepage     = 'https://github.com/wujiangwei/ModelNetworkClient'
spec.authors      = { 'Kevin.Wu' => 'wujiangwei55@163.com' }
spec.summary      = '基于AFNetworking和JSONModel整合的IOS ModelNetworkClient，为需要使用网络的IOS App提供方便快捷、基于操作对象的App开发体验'
spec.source       = { :git => 'https://github.com/wujiangwei/ModelNetworkClient.git', :commit => '4fed2269f977873ea55a790166ecf4e0f19c0af3' }
spec.source_files = 'ModelNetworkClient.{h,m}'
spec.framework    = 'Foundation'
spec.dependency 'JSONModel'
spec.dependency 'AFNetworking', '~> 2.4.1'
spec.ios.deployment_target = "6.0"
spec.requires_arc = true
end