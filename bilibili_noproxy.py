import requests
import time

bvids = []

def print_log(msg):
    print(msg, flush=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive'
}

reqdatas = []
for bvid in bvids:
    stime = str(int(time.time()))
    resp = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={}".format(bvid), headers=headers)
    rdata = resp.json()["data"]
    data = {
        'aid': rdata["aid"],
        'cid': rdata["cid"],
        "bvid": bvid,
        'part': '1',
        'mid': rdata["owner"]["mid"],
        'lv': '6',
        "stime": stime,
        'jsonp': 'jsonp',
        'type': '3',
        'sub_type': '0',
        'title': rdata["title"],
        'view': rdata["stat"]["view"]
    }
    reqdatas.append(data)

def goPlay(url):
    count = 0
    while True:
        try:
            for data in reqdatas:
                stime = str(int(time.time()))

                data["stime"] = stime
                headers["referer"] = "https://www.bilibili.com/video/{}/".format(data.get("bvid"))

                print_log("bvid: {}, title: {}, view: {}".format(data.get("bvid"), data.get("title"), data.get("view")))

                response = requests.post(url, data=data, headers=headers)
                if response.status_code == 200:
                    data["view"] += 1  # 更新播放量值

            count += 1
            print_log(count)
            time.sleep(100)
        except Exception as e:
            print_log(e)
            time.sleep(100)
            print_log('over')

url = "https://api.bilibili.com/x/click-interface/click/web/h5"

print_log("准备起飞啦~~~{}".format(bvids))

goPlay(url)
