from config import PUSH_KEY,WB_USERID
from weibo import wbMonitor
import requests,time
times = 1440
def timer(n,task):
    count=0
    while True:
        count+=1
        if(count>times):
            msg = 'Monitor End'
            requests.get('https://sc.ftqq.com/' + PUSH_KEY + '.send?text=' + msg)
            break
        result = task.MonitorWB()
        print(result[0])
        if(result[0]):
            title = result[1]
            desp = result[2]
            requests.get('https://sc.ftqq.com/' + PUSH_KEY + '.send?text=' + title +'&desp='+desp)
            print(f'succ get newWeibo in {count}')
        else:
            print(f'keep get and now {count}')
        time.sleep(n)
task = wbMonitor(uid=WB_USERID)
timer(60,task)