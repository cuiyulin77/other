# -*- coding: utf-8 -*-
import logging
# 引入log日志，以‘a’追加的方式写入本地文件.加上时间
# FEED_EXPORT_ENCODING = 'utf-8'
# logging.basicConfig(filename='weibo_spider.log',level=logging.DEBUG,format='%(asctime)s  u%(message)s',datefmt='%m/%d/%Y %I:%M:%S')

# Scrapy settings for WB project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WB'

SPIDER_MODULES = ['WB.spiders']
NEWSPIDER_MODULE = 'WB.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'WB (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 16
# 禁止重试:
# RETRY_ENABLED = False
# 减小下载超时:
DOWNLOAD_TIMEOUT = 100
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1000000
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'WB.middlewares.WbSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'WB.middlewares.WbDownloaderMiddleware': 543,
'WB.middlewares.RandomUserAgent': 1,
'WB.middlewares.RandomProxy': 10,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'WB.pipelines.WbPipeline': 300,
'WB.pipelines.DBPipeline': 30,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

USER_AGENTS = ['Mozilla/5.0 (Linux; Android 6.0; Le X620 Build/HBXCNCU5902606112S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile M',
'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/',
'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Langu',
'Mozilla/5.0 (Linux; Android 5.1.1; vivo Xplay5A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safar',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser',
'Mozilla/5.0 (Linux; Android 6.0; LEX626 Build/HEXCNFN5902606111S) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safar',
'Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; ZUK Z2121 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11',
'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.17 NetType/WIFI Langu',
'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/1',
'MQQBrowser/5.3/Mozilla/5.0 (Linux; Android 6.0; TCL 580 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Mobil',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.16 NetType/WIFI Langua',
'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.',
'Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.3',
'Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.7.2 Mobile/15A372 Safari/',
'Mozilla/5.0 (Linux; Android 6.0; MX6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TB',
'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A405 MicroMessenger/6.5.15 NetType/WIFI Lang',
'Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; PRA-AL00 Build/HONORPRA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrow',
'Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (Linux; Android 5.1; OPPO R9tm Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537',
'Mozilla/5.0 (Linux; Android 7.0; VTR-AL00 Build/HUAWEIVTR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (Linux; Android 7.0; Infinix X572 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/5',
'Mozilla/5.0 (Linux; Android 6.0.1; SM-A7100 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36',
'Mozilla/5.0 (iPhone 91; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14C92 Safari/8',
'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/',
'Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 wxwork/2.1.5 MicroMessenger/6.3.22',
'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; MX5 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile S',
'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; C106 Build/ZAXCNFN5902606201S) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCB',
'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; KIW-TL00H Build/HONORKIW-TL00H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UC',
'Mozilla/5.0 (Linux; Android 6.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mob',
'Mozilla/5.0 (Linux; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A402 MicroMessenger/6.5.16 NetType/WIFI Lan',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; SM-G9500 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.',
'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; NX531J Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.8 Mob',
'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A402 wxwork/2.1.5 MicroMessenger/6.3.22',
'Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 5X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari',
'Mozilla/5.0 (iPhone 6; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.6.1 Mobile/13E238 Safari/8',
'Mozilla/5.0 (Linux; Android 5.1; vivo X6D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.16 NetType/WIFI Langu',
'Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; EVA-DL00 Build/HUAWEIEVA-DL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser',
'Mozilla/5.0 (Linux; Android 5.0.2; vivo X6A Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/53',
'Mozilla/5.0 (Linux; Android 5.1.1; MX4 Pro Build/LMY48W; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537',
'Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTE Build/KTU84P; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBro',
'Mozilla/5.0 (Linux; Android 7.0; MIX Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TB',
'Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6',
'Mozilla/5.0 (Linux; Android 7.1.1; NX563J Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6',
'Mozilla/5.0 (Linux; Android 7.0; EVA-AL10 Build/HUAWEIEVA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (Linux; Android 5.1; vivo X6Plus D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrow',
'Mozilla/5.0 (Linux; Android 6.0; ALE-TL00 Build/HuaweiALE-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (Linux; Android 7.0; ZUK Z2121 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/',
'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; PLK-AL10 Build/HONORPLK-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrow',
'Mozilla/5.0 (Linux; Android 7.0; WAS-AL00 Build/HUAWEIWAS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (iPhone 6p; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/',
'Mozilla/5.0 (Linux; Android 7.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Saf',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mob',
'Mozilla/5.0 (Linux; Android 6.0; Redmi Note 4X Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E277 MicroMessenger/6.5.16 NetType/4G Languag',
'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobi',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; EVA-DL00 Build/HUAWEIEVA-DL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBro',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.17 NetType/WIFI Langu',
'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.15 NetType/4G Languag',
'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 search%2F1.0 baiduboxapp/0_0.1.1.7_enohp',
'Mozilla/5.0 (Linux; Android 5.1.1; OPPO R7sPlus Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safar',
'Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari',
'Mozilla/5.0 (iPhone 6p; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 MQQBrowser/7.8.0 Mobile/12B436 Safari/8',
'Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser',
'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; KIW-CL00 Build/HONORKIW-CL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowse',
'Mozilla/5.0 (Linux; Android 6.0.1; MI 4LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/',
'Mozilla/5.0 (Linux; Android 4.4.2; Coolpad 8675 Build/KOT49H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBro',
'Mozilla/5.0 (Linux; Android 6.0.1; vivo X9i Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser',
'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; VIE-AL10 Build/HUAWEIVIE-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBro',
'Mozilla/5.0 (Linux; Android 6.0; Redmi Note 4 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrows',
'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; Redmi 3 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safa',
'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; Redmi Note 4 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser',
'Mozilla/5.0 (Linux; Android 7.0; SM-G9550 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.',
'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBro',
'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Max',
'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safa',
'Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.',
'Mozilla/5.0 (Linux; Android 7.0; HUAWEI CAZ-AL10 Build/HUAWEICAZ-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobi',
'Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537',
'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.17 NetType/4G Languag',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.7 NetType/WIFI Langua',
'Mozilla/5.0 (Linux; Android 6.0; M5 Note Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.',
'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36',
'Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3000 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBr',
'Mozilla/5.0 (Linux; Android 8.0; G8342 Build/47.1.A.2.324; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowse',
'Mozilla/5.0 (Linux; Android 7.0; EVA-TL00 Build/HUAWEIEVA-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.16 NetType/4G Languag',
'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.5.16 NetType/4G Languag',
'Mozilla/5.0 (Linux; Android 6.0; EVA-TL00 Build/HUAWEIEVA-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQB',
'Mozilla/5.0 (Linux; Android 6.0.1; SM-C5000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser',
'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OD105 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.15 NetType/WIFI Langu',
'Mozilla/5.0 (iPhone 6s; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.8.0 Mobile/13F69 Safari/8',]
