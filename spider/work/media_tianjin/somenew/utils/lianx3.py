a = 'noticeLoginFlag=1; ua_id=ZYXJmDHCfwNDGMhXAAAAAPVJG_jsih9D-7ep2snTGQg=; pgv_pvi=2258126848; pgv_pvid=5505708263; RK=aRZR0QdxEg; ptcz=319f503fd2b9796e0fae60bee6c61b89ba999a2bb7bf7989922265bd20df884d; o_cookie=494658565; pac_uid=1_494658565; gr_user_id=6bfcfe72-05bd-4408-a04f-8c5161c21f65; mm_lang=zh_CN; noticeLoginFlag=1; rewardsn=; wxtokenkey=777; uin=o0494658565; skey=@Z1ENKo2L9; ptisp=ctc; sig=h013f78337fc4a48f6024bd3ba477fa789251f8a6cecfe350308546bd86cb83250e35baa28e3ea55fbc; webwx_data_ticket=gScJb1tAc5Aycj7m/cBnvg1x; pgv_si=s5891575808; uuid=1f9a02a4374d43e9c771d55404d422f1; bizuin=3587797364; ticket=36492d6e0006644baf93d4855d9c7bedd7885401; ticket_id=gh_73f6cef5a698; cert=iwC_1HEVhBh9YbnzwZeo1fgs9wkxfAkQ; data_bizuin=3587797364; data_ticket=tB/BR/n2TLJFzcg83NqutWSJGIdGgo1aA1Ec5Yeau9JdkRp4CYj2V4FClSLd2jzC; slave_sid=MkxJWk40SzdBQzdPODdDN2RmcE1FZDdLU190cndiUTcwNkljMDZnYmlIUW1Rc0l5N2VyNnU2TjVsRmxhWGlGV1FVODFzRnBBS255NWpjYlFiQjhiN193MEtVSktiZFgxeW9qYU4yaHJ3X25RR1Zpeloxa3U1akRDTmV3VEZ1bXdEcE5UUHF6MnN3RkNuUnNP; slave_user=gh_73f6cef5a698; xid=0c7fdcfb534637631a18fb8bba0430d6; openid2ticket_odHHZ1TGQ2yTAXOldBOVRIkLq7ZA=2C1dXeJA9z42gSBygs4cJDJH5jtucoCfkpzJNJbf3kI='
a_list = a.split(';')
a_dict = {}
for a_lis in a_list:
    for a_li in a_lis.split('='):
        if '=' in a_li:
            a_l = a_lis.split('=')
            print(a_l)
            n = len(a_l)
            if n == 2:
                a_dict[a_li] = a_l[1]
                break
            elif n == 3 and a_lis.index('=') == -1:
                a_dict[a_li.lstrip('')] = a_l[1] + '='
                break
            elif n == 3 and a_lis.index('=') != -1:
                a_dict[a_li.lstrip('')] = a_l[1]+a_l[2]
                break
            else:
                print('-----------')
        else:
            a_dict[a_li] = a_lis.split('=')[1]
            break

print(a_dict)