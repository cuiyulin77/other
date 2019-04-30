#
# from redis import *
# pool = ConnectionPool(host='127.0.0.1', port=6379, db=14)
# r = StrictRedis(connection_pool=pool)
# ip1_str = r.get('ip1').decode()
# ip2_str = r.get('ip2').decode()
# PROXIES=[ip1_str,ip2_str]
# print(PROXIES)

ip_list = [1,2,3,4,5]
nums = len(ip_list)
print(nums)
ip_key_name = []
for i in range(nums):
    ip_key_name.append('ip'+str(i))

for i in range(nums):
    # ip从列表中拼接出ip地址
    ip = ip_list[i]['ip'] + ':' + str(ip_list[i]['port'])
    print(ip)
    #获取失效时间的时间戳
    ip_time = time.strptime(ip_list[i]['expire_time'], "%Y-%m-%d %H:%M:%S")
    ip_time = int(time.mktime(ip_time))
    now = int(time.time())
    ip_left = int(ip_time) - now
    # 2.设置ip的过期时间
    a = r.setex(ip_key_name[i], ip_left, ip)
    print(a)