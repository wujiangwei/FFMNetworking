Pod::Spec.new do |spec|
spec.name         = 'FFMNetworking'
spec.license      = { :type => 'MIT' }
spec.platform     = :ios, '6.0'
spec.homepage     = 'https://github.com/wujiangwei/FFMNetworking'
spec.authors      = 'Kevin.Wu'
spec.summary      = 'Base on AFNetworking(2.x) And JSONModel, ModelNetworkClient, For Object NetData Deal and fast developing'
spec.source       =  {:git => 'https://github.com/wujiangwei/FFMNetworking.git'}
spec.source_files = 'FFMNetworking.{h,m}'
spec.frameworks = 'Foundation'
spec.dependency 'JSONModel'
spec.dependency 'AFNetworking'
spec.ios.deployment_target = '6.0'
spec.requires_arc = true
end
