{
    "辽宁": {
        "大连": {
            "瓦房店": [
                "瓦房店发布",
                "瓦房店旅游局"
            ],"普兰店": [
                "普兰店发布",
                "普兰店区旅游"
            ]
        },
        "营口": {
            "熊岳": [
                "熊岳小雨温泉"
            ],"大石桥": [
                "大石桥发布",
                "大石桥吃喝玩乐网"
            ]
        }
    }
}
import requests
postData = {'access_token': 'multipart/form-data'
}

# 对于我们工作中的自己人,我们一般会使用别的验证,而不是csrf_token验证
response = requests.post('//qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=accesstoken001&type=file HTTP/1.1',data=postData)
# 通过get请求返回的文本值
print(response.text)
# https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=K3MyCE-v0e_cm2pmWY6fzKJYoO4QStFUtaC-Sy3ebsVUfRRQ_9yS_EjAzG2Z4TLvNx8X0NNNRNHu_EstPVX96rILwjypnkRJapIsFU9HeqzAklfuY9sxXZu_v1-jbgBDpwZWcQSNU2_UdpltpJG_-uPpNslF83EIjdkngQSGvRIhSfFT4QxM1xR3vtw6ai6qPX1IOSrSPHsRocHKeqRJ1w&type=file