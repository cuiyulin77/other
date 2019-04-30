# -*- coding: utf-8 -*-

# Scrapy settings for blog project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'blog'

SPIDER_MODULES = ['blog.spiders']
NEWSPIDER_MODULE = 'blog.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'blog.middlewares.BlogSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'blog.middlewares.BlogDownloaderMiddleware': 543,
    'blog.middlewares.RandomUserAgent': 1,
    # 'blog.middlewares.RandomProxy': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'blog.pipelines.BlogPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
]

PROXIES =  [
{"port":"27835","ip":"60.169.221.157"},{"port":"33030","ip":"125.112.204.225"},{"port":"27314","ip":"183.135.248.212"},{"port":"37240","ip":"120.40.135.34"},{"port":"32594","ip":"115.221.123.222"},{"port":"29661","ip":"49.85.7.158"},{"port":"46194","ip":"113.121.241.121"},{"port":"40691","ip":"115.203.215.86"},{"port":"41050","ip":"110.88.127.19"},{"port":"21306","ip":"123.162.192.155"},{"port":"36924","ip":"60.182.198.45"},{"port":"47061","ip":"49.87.75.48"},{"port":"34244","ip":"180.122.144.185"},{"port":"26059","ip":"115.221.122.53"},{"port":"35227","ip":"60.175.196.125"},{"port":"35451","ip":"116.226.60.121"},{"port":"33935","ip":"123.161.119.86"},{"port":"40738","ip":"113.121.242.49"},{"port":"38110","ip":"59.56.242.223"},{"port":"43774","ip":"115.221.121.216"},
{"port":"22195","ip":"125.109.193.55"},{"port":"31969","ip":"218.66.147.144"},{"port":"42979","ip":"222.78.124.197"},{"port":"22058","ip":"114.231.64.34"},{"port":"46959","ip":"121.232.185.36"},{"port":"34027","ip":"113.128.27.232"},{"port":"30969","ip":"114.99.72.250"},{"port":"35892","ip":"117.95.199.6"},{"port":"46061","ip":"1.198.97.206"},{"port":"26902","ip":"49.81.187.7"},{"port":"22567","ip":"123.163.140.218"},{"port":"26395","ip":"123.161.155.16"},{"port":"33017","ip":"113.121.161.31"},{"port":"43360","ip":"36.25.56.144"},{"port":"45558","ip":"180.114.93.203"},{"port":"29090","ip":"117.28.147.170"},{"port":"34959","ip":"218.66.147.114"},{"port":"26724","ip":"110.82.103.143"},{"port":"40078","ip":"175.8.26.21"},{"port":"38440","ip":"120.39.160.108"},{"port":"36639","ip":"180.113.81.213"},{"port":"22389","ip":"223.245.241.246"},{"port":"23815","ip":"117.95.199.179"},{"port":"41222","ip":"123.55.185.198"},{"port":"23888","ip":"175.8.27.0"},{"port":"37455","ip":"115.203.213.50"},{"port":"20203","ip":"115.203.220.131"},{"port":"30385","ip":"218.66.147.100"},{"port":"34241","ip":"114.230.217.186"},{"port":"27487","ip":"116.54.77.137"},
{"port":"26489","ip":"202.98.76.21"},{"port":"40297","ip":"115.203.209.93"},{"port":"47458","ip":"42.57.89.74"},
 {"port":"25642","ip":"117.69.98.188"},{"port":"38435","ip":"218.66.147.97"},{"port":"26354","ip":"183.154.51.62"},{"port":"25668","ip":"220.191.82.213"},{"port":"28475","ip":"140.224.98.59"},{"port":"24239","ip":"120.43.232.241"},{"port":"46959","ip":"183.144.208.155"},{"port":"30711","ip":"115.215.49.122"},{"port":"32156","ip":"49.68.127.243"},{"port":"49096","ip":"115.203.208.176"},{"port":"44500","ip":"175.146.71.253"},{"port":"22839","ip":"113.128.8.149"},{"port":"22330","ip":"123.55.176.123"},{"port":"30910","ip":"117.31.149.134"},{"port":"35719","ip":"120.33.247.145"},{"port":"24084","ip":"113.121.240.130"},{"port":"34773","ip":"110.82.103.92"},{"port":"33055","ip":"180.125.22.152"},{"port":"40644","ip":"218.66.150.197"},{"port":"21507","ip":"180.113.81.43"},{"port":"44274","ip":"116.231.245.214"},{"port":"32674","ip":"171.15.95.226"},{"port":"31402","ip":"120.39.118.176"},{"port":"39205","ip":"49.81.16.194"},{"port":"36573","ip":"218.66.145.240"},{"port":"25720","ip":"120.35.130.74"},{"port":"49669","ip":"117.86.21.118"},
{"port":"42067","ip":"123.161.119.12"},{"port":"35894","ip":"218.73.136.232"},{"port":"21159","ip":"115.203.220.131"},{"port":"24582","ip":"183.52.105.248"},{"port":"32336","ip":"115.203.193.22"},{"port":"43247","ip":"27.158.127.147"},{"port":"30635","ip":"114.239.110.229"},{"port":"25587","ip":"110.86.97.196"},{"port":"33921","ip":"117.27.111.146"},{"port":"22482","ip":"123.55.184.137"},{"port":"28662","ip":"115.203.203.20"},{"port":"47777","ip":"183.144.210.2"},{"port":"30797","ip":"125.78.6.246"},{"port":"23339","ip":"49.85.0.190"},{"port":"35968","ip":"60.169.216.108"},{"port":"26544","ip":"1.195.26.41"},{"port":"20070","ip":"115.203.218.161"},{"port":"38688","ip":"125.119.48.236"},{"port":"44519","ip":"114.232.163.156"},{"port":"49653","ip":"125.125.229.222"},
{"port":"48479","ip":"123.163.20.163"},{"port":"47937","ip":"125.126.175.109"},{"port":"33611","ip":"106.46.4.13"},{"port":"49375","ip":"115.203.215.206"},{"port":"20721","ip":"117.57.91.150"},{"port":"28144","ip":"140.224.98.54"},{"port":"42805","ip":"27.156.213.214"},{"port":"42101","ip":"180.155.135.49"},{"port":"37251","ip":"61.143.17.178"},{"port":"20306","ip":"115.221.127.215"},{"port":"38320","ip":"114.238.130.81"},{"port":"42120","ip":"115.202.236.4"},{"port":"33387","ip":"115.203.210.190"},{"port":"49992","ip":"114.230.217.108"},{"port":"37913","ip":"115.221.125.26"},{"port":"41759","ip":"36.25.25.74"},{"port":"29953","ip":"61.143.23.196"},{"port":"36949","ip":"1.198.89.242"},{"port":"31899","ip":"115.203.216.81"},{"port":"39367","ip":"115.203.220.100"},
{"port":"42305","ip":"125.125.181.15"},{"port":"45286","ip":"113.121.243.144"},{"port":"20227","ip":"171.13.37.52"},{"port":"34844","ip":"175.8.27.18"},{"port":"44326","ip":"123.149.162.224"},{"port":"23254","ip":"110.89.132.14"},{"port":"41227","ip":"122.242.93.41"},{"port":"32391","ip":"223.244.127.128"},{"port":"49425","ip":"115.203.207.228"},{"port":"47460","ip":"36.99.206.39"},{"port":"40826","ip":"114.231.71.102"},{"port":"27652","ip":"27.154.182.251"},{"port":"47962","ip":"113.121.184.167"},{"port":"25573","ip":"114.231.69.96"},{"port":"31582","ip":"60.175.213.188"},{"port":"48189","ip":"113.135.237.210"},{"port":"48613","ip":"171.15.92.255"},{"port":"27912","ip":"115.215.49.121"},{"port":"49888","ip":"140.224.98.39"},{"port":"45949","ip":"218.73.137.142"},
]
