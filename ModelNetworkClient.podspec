Pod::Spec.new do |spec|
spec.name         = 'ModelNetworkClient'
spec.version      = '0.9'
spec.license      = { :type => 'MIT' }
spec.platform     = :ios, '6.0'
spec.homepage     = 'https://github.com/wujiangwei/ModelNetworkClient'
spec.authors      = 'Kevin.Wu'
spec.summary      = 'Base on AFNetworking(2.x) And JSONModel, ModelNetworkClient, For Object NetData Deal and fast developing'
spec.source       =  {:git => 'git://github.com/wujiangwei/ModelNetworkClient.git', :tag => 'v0.9'}
spec.source_files = 'ModelNetworkClient.{h,m}'
spec.dependency 'JSONModel'
spec.dependency 'AFNetworking'
spec.ios.deployment_target = '6.0'
spec.requires_arc = true
end
