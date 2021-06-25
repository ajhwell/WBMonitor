import requests,json,sys,time,os
from selenium.common.exceptions import NoSuchElementException
class wbMonitor():
    uid = []
    weiboid = set()
    def __init__(self, uid):
            self.reqHeaders={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://passport.weibo.cn/signin/login',
                'Connection': 'close',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
            }
            self.uid = uid

    # 获取访问连接
    def getweiboInfo(self):
        try:
            self.weiboInfo = []
            for i in self.uid:
                userInfo = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s' % (i)
                res = requests.get(userInfo, headers=self.reqHeaders)
                for j in res.json()['data']['tabsInfo']['tabs']:
                    if j['tab_type'] == 'weibo':
                        self.weiboInfo.append(
                            'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s' % (
                            i, j['containerid']))
        except Exception as e:
            sys.exit()

    # 收集已经发布动态的id
    def getWBQueue(self):
        try:
            for i in self.weiboInfo:
                res = requests.get(i, headers=self.reqHeaders)
                for j in res.json()['data']['cards']:
                    if j['card_type']==9:
                        self.weiboid.add(j['mblog']['id'])
        except Exception as e:
            print(e)
            sys.exit()
    # 开始监控
    def startmonitor(self, ):
        returnDict = {}  # 获取微博相关内容，编辑为邮件
        try:
            for i in self.weiboInfo:
                res = requests.get(i, headers=self.reqHeaders)
                for j in res.json()['data']['cards']:
                    if j['card_type'] == 9:
                        if j['mblog']['id'] not in self.weiboid:
                            self.weiboid.add(j['mblog']['id'])
                            returnDict['created_at'] = j['mblog']['created_at']
                            returnDict['text'] = j['mblog']['text']
                            returnDict['source'] = j['mblog']['source']
                            returnDict['nickName'] = j['mblog']['user']['screen_name']
                            return returnDict
        except Exception as e:
            sys.exit()
    def MonitorWB(self):
        time.sleep(5)
        try:
            self.getweiboInfo()
            if not self.weiboid:
                self.getWBQueue()
            newWeibo = self.startmonitor()
            if newWeibo is not None:
                text = newWeibo['nickName'] + '发布了一条微博'
                desp = newWeibo['text']
                return [True, text, desp]
            else:
                return [False]
        except NoSuchElementException:
            return [False]