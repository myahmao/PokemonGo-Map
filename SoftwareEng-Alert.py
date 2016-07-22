#   -*-   coding:   utf-8   -*-
import cookielib, urllib2, sys, datetime
from KaixinAccount import KaixinAccount
import codecs
import logging
import PySnarl
import os, sys, string
import smtplib
import base64
import time

gblUserName='myahmao@gmail.com'
gblPassword='mylove123'

gblBuyMonitoringEnabled = True
gblSellMonitoringEnabled = True

if not gblBuyMonitoringEnabled and not gblSellMonitoringEnabled:
  sys.exit(0)

'''
'http://www.kaixin001.com/!rich/market.php?cateid=2',
'http://www.kaixin001.com/!rich/market.php?cateid=3',
'http://www.kaixin001.com/!rich/market.php?cateid=4',
'http://www.kaixin001.com/!rich/market.php?cateid=6',
'http://www.kaixin001.com/!rich/market.php?cateid=7',
'http://www.kaixin001.com/!rich/market.php?cateid=8',
'''
gblUrlList = [
'http://www.kaixin001.com/!rich/market.php?cateid=2',
'http://www.kaixin001.com/!rich/market.php?cateid=3',
'http://www.kaixin001.com/!rich/market.php?cateid=4',
'http://www.kaixin001.com/!rich/market.php?cateid=6',
'http://www.kaixin001.com/!rich/market.php?cateid=7',
'http://www.kaixin001.com/!rich/market.php?cateid=8',
'http://www.kaixin001.com/!rich/market.php?cateid=9',
'http://www.kaixin001.com/!rich/market.php?cateid=10',

]

gblAlertItems = [
  #{'name': '水果店', 'buyThreshold': 44000, 'sellThreshold': 52000, 'buy_sell': 0},
  #{'name': '奶茶店', 'buyThreshold': 72000, 'sellThreshold': 78000, 'buy_sell': 0},
  #{'name': '杂货店', 'buyThreshold': 84000, 'sellThreshold': 92000, 'ename': 'Grocery', 'buy_sell': 0},
  #{'name': '包子铺', 'buyThreshold': 91000, 'sellThreshold': None, 'buy_sell': 0},
  #{'name': '服装店', 'buyThreshold': 108000, 'sellThreshold': None, 'buy_sell': 0},
  #{'name': '养鸡场', 'buyThreshold': 200000, 'sellThreshold': None, 'buy_sell': 0},
  {'name': '火锅店', 'buyThreshold': 270000, 'sellThreshold': 310000, 'ename': 'Hot pot', 'buy_sell': 0},
  {'name': '蛋糕店', 'buyThreshold': 288000, 'sellThreshold': 304000, 'ename': 'Bakery', 'buy_sell': 0},
  {'name': '饰品店', 'buyThreshold': 472000, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '社区超市', 'buyThreshold': 555000, 'sellThreshold': 620000, 'buy_sell': 0, 'ename': ''},
  {'name': '养猪场', 'buyThreshold': 739000, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '公仔玩偶店', 'buyThreshold': 1020000, 'sellThreshold': 1130000, 'ename': 'Doll Shop', 'buy_sell': 0},  #low 900000, highest 1300000
  {'name': '彩票投注站', 'buyThreshold': 1050000, 'sellThreshold': 1130000, 'ename': 'Lottery Site', 'buy_sell': 0}, #low 1000000, high 1200000
 #{'name': '奶粉厂', 'buyThreshold': 1150000, 'sellThreshold': 1210000, 'buy_sell': 0, 'ename': ''},
  {'name': '中餐厅', 'buyThreshold': 1650000, 'sellThreshold': 1800000, 'ename': 'Chinese Rest', 'buy_sell': 0},
 #{'name': '西餐厅', 'buyThreshold': 4000000, 'sellThreshold': 4500000, 'ename': 'Western Rest', 'buy_sell': 0},
  {'name': '电脑专卖店', 'buyThreshold': 2800000, 'sellThreshold': 3120000, 'ename': 'Computer Shop', 'buy_sell': 0},
  {'name': '时尚美甲店', 'buyThreshold': 3000000, 'sellThreshold': 3300000, 'buy_sell': 0, 'ename': ''},
 #{'name': '婚纱影楼', 'buyThreshold': 11000000, 'sellThreshold': 12000000, 'buy_sell': 0, 'ename': ''},
  {'name': '饲料厂', 'buyThreshold': 11000000, 'sellThreshold': 12000000, 'buy_sell': 0, 'ename': ''},
  
  {'name': '豪华海鲜酒楼', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '房地产公司', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '大型家具卖场', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '汽车公司', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '石油天然气公司', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '黄金采矿公司', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '证券交易所', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
   
  #{'name': '麻将馆', 'buyThreshold': 86000, 'sellThreshold': 93000, 'ename': 'Majon', 'buy_sell': 0},
  {'name': '美发厅', 'buyThreshold': 260000, 'sellThreshold': 282000, 'ename': 'Hair Salon', 'buy_sell': 0},
  {'name': '电玩城', 'buyThreshold': 460000, 'sellThreshold': 505000, 'ename': 'Game City', 'buy_sell': 0},
  {'name': '网吧', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '酒吧', 'buyThreshold': 940000, 'sellThreshold': 1030000, 'buy_sell': 0, 'ename': ''},
  {'name': '咖啡厅', 'buyThreshold': 1900000, 'sellThreshold': 2040000, 'buy_sell': 0, 'ename': ''},
  {'name': '美容院', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': 'KTV', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '健身俱乐部', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': 'SPA养生会所', 'buyThreshold': 21100000, 'sellThreshold': 23800000, 'buy_sell': 0, 'ename': ''},
  {'name': '温泉度假村', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '电影院', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '游乐园', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
# {'name': '赌场', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
# {'name': '迪拜七星级酒店', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},

  {'name': '城市轻轨列车', 'buyThreshold': 49000000, 'sellThreshold': 52800000, 'buy_sell': 0, 'ename': ''}, 
  {'name': '加长轿车', 'buyThreshold': 2600000, 'sellThreshold': 2850000, 'buy_sell': 0, 'ename': ''},
  {'name': '磁悬浮列车', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '私人商务飞机', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  
# {'name': '社区公园', 'buyThreshold': 86000, 'sellThreshold': 96000, 'buy_sell': 0, 'ename': ''},
  {'name': '时尚公寓', 'buyThreshold': 1300000, 'sellThreshold': 1600000, 'ename': 'Modern Apt', 'buy_sell': 0}, #low 1200000, highest 2000000
  {'name': '个性LOFT', 'buyThreshold': 4200000, 'sellThreshold': 4550000, 'ename': 'Loft', 'buy_sell': 0},
  {'name': '花园洋房', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '豪华别墅', 'buyThreshold': 26500000, 'sellThreshold': 28500000, 'buy_sell': 0, 'ename':'Big house'},
  {'name': '私家马场', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '金融街', 'buyThreshold': 94000000, 'sellThreshold': 102000000, 'buy_sell': 0, 'ename': ''},
  {'name': '高尔夫球场', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  
  {'name': '名牌手包', 'buyThreshold': 205000, 'sellThreshold': 230000, 'buy_sell': 0, 'ename': ''},
  {'name': '定制成衣', 'buyThreshold': 570000, 'sellThreshold': 600000, 'buy_sell': 0, 'ename': ''},
  {'name': '珍珠头冠', 'buyThreshold': 1250000, 'sellThreshold': 1320000, 'ename': 'Pearl Crown', 'buy_sell': 0}, #low 1140000, highest 1500000
  {'name': '房屋戒指', 'buyThreshold': 1800000, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '豪华腕表', 'buyThreshold': 4950000, 'sellThreshold': 5400000, 'buy_sell': 0, 'ename': 'Golden Watch'},
  {'name': '翡翠名品', 'buyThreshold': 7500000, 'sellThreshold': 8100000, 'buy_sell': 0, 'ename': ''},
  {'name': '粉红钻石', 'buyThreshold': 16000000, 'sellThreshold': 17750000, 'ename': 'Diamond', 'buy_sell': 0},
  {'name': '超级跑车', 'buyThreshold': 47000000, 'sellThreshold': 52000000, 'buy_sell': 0, 'ename': 'Sports car'},
  {'name': '顶级豪宅', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': 'Bomber'},
  
  {'name': '轰炸机', 'buyThreshold': 47000000, 'sellThreshold': 52000000, 'buy_sell': 0, 'ename': 'Bomber'},
  
  {'name': '人造卫星', 'buyThreshold': 92000000, 'sellThreshold': 110000000, 'ename':'Satellite', 'buy_sell': 0},
  {'name': '太阳能汽车', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '海上钻井平台', 'buyThreshold': None, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},

	{'name': '光碟', 'buyThreshold': 20, 'sellThreshold': None, 'ename': 'CD', 'buy_sell': 0},  
  {'name': '山寨手机', 'buyThreshold': 1300, 'sellThreshold': 2800, 'ename': 'Fake Cellphone', 'buy_sell': 0},
  {'name': '笔记本电脑', 'buyThreshold': 7000, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '人力车', 'buyThreshold': 6000, 'sellThreshold': 8000, 'buy_sell': 0, 'ename': ''},
  {'name': '美女帅哥证', 'buyThreshold': 200, 'sellThreshold':None, 'ename': 'Boys&Girls', 'buy_sell': 0},
  {'name': '火车票', 'buyThreshold': 200, 'sellThreshold': 400, 'ename': 'Train Tickets', 'buy_sell': 0},
  {'name': '手机卡', 'buyThreshold': 250, 'sellThreshold': 500, 'ename': 'Phone Sim Card', 'buy_sell': 0},
  {'name': '奶粉', 'buyThreshold': 300, 'sellThreshold': 600, 'ename': 'Milk powder', 'buy_sell': 0},
  {'name': '散装酒', 'buyThreshold': 350, 'sellThreshold': 600, 'buy_sell': 0, 'ename': ''},
  {'name': '保健品', 'buyThreshold': 300, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '进口化妆品', 'buyThreshold': 500, 'sellThreshold': None, 'buy_sell': 0, 'ename': ''},
  {'name': '二手电脑', 'buyThreshold': 1300, 'sellThreshold': None, 'ename': 'Second Hand PC', 'buy_sell': 0},
  {'name': '旧奥拓', 'buyThreshold': 12000, 'sellThreshold': 19000, 'buy_sell': 0, 'ename': ''},
  {'name': '小卖部', 'buyThreshold': 35000, 'sellThreshold': None, 'ename': '7-11', 'buy_sell': 0, 'ename': ''},
  {'name': '鲜花店', 'buyThreshold': 25000, 'sellThreshold': 42000, 'buy_sell': 0, 'ename': ''},
 
]

#gblLogger = logging.getLogger('')

def initLogging(fn):
 logFormat = '%(asctime)s %(levelname)-5s - %(message)s'
 logging.basicConfig(filename=fn, level=logging.DEBUG, format=logFormat, filemode='a')

TEN_KILO = '万'
Yi = '亿'

# ============= MAIN ================
arg = None
if len(sys.argv) > 1:
  arg = sys.argv[1]

#initLogging('kaixin.log')

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

me = KaixinAccount()
fout1 = open('login.log', 'a')
if me.login(gblUserName, gblPassword) != -1:
   fout1.write('%s login success!\n' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
fout1.close()

def checkPrice():
  fout = open('super-alert.out', 'a')
  fout.write('\n\n★★★Timestamp: %s ★★★\n' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

  bBuyAlerted = False
  bSellAlerted = False

  for url in gblUrlList:
    req = urllib2.Request(url)
    handle = urllib2.urlopen(req)

    line = handle.readline()
    while line is not None and len(line) != 0:
      if line.find('</b></li>') != -1:
        for item in gblAlertItems:
          if line.find('<b>' + item['name'] + '</b>') != -1:
            line = handle.readline()
            startPos = line.find('>')
            endPos = line.find('元<', startPos)
            strPrice = line[startPos + 1:endPos]
            posTenKilo = strPrice.find(TEN_KILO)
            posYi = strPrice.find(Yi)
            price = 0
            if posTenKilo == -1 and posYi == -1:
              price = int(strPrice)
            else:
              if posYi == -1:
                 price = int(float(strPrice[:posTenKilo]) * 10000)
              else:
                 price = int(float(strPrice[:posYi]) * 100000000)
            # or (cmp(item['name'], '火锅店') == 0 and price <=270000 ) \     or (cmp(item['name'], '火锅店') == 0 and price >310000 ) \
            # or (cmp(item['name'], '火锅店') == 0 and (price <=270000 or price >310000)) \
            
            if (cmp(item['name'], '公仔玩偶店') == 0 and (price <=1020000)) \
               or (cmp(item['name'], '中餐厅') == 0 and (price <= 1600000)) \
               or (cmp(item['name'], '彩票投注站') == 0 and (price <=1020000))\
               or (cmp(item['name'], '珍珠头冠') == 0 and (price <=1140000)) \
               or (cmp(item['name'], '个性LOFT') == 0 and (price <=4000000)) \
               or (cmp(item['name'], '时尚公寓') == 0 and (price <=1300000)) \
               or (cmp(item['name'], '粉红钻石') == 0 and (price <=15500000)) \
               or (cmp(item['name'], '超级跑车') == 0 and (price < 47000000)) \
               or (cmp(item['name'], '豪华别墅') == 0 and (price <= 25000000)) \
               or (cmp(item['name'], 'SPA养生会所') == 0 and (price <= 20400000)) \
               or (cmp(item['name'], '轰炸机') == 0 and (price <= 46000000)) \
               or (cmp(item['name'], '豪华腕表') == 0 and (price <= 4700000)) \
               or (cmp(item['name'], '金融街') == 0 and (price <= 92000000)) \
               or (cmp(item['name'], '人造卫星') == 0 and (price <=92000000)) :
               item['buy_sell'] = -1
               PySnarl.snShowMessage("Reminder", 'Item to Buy: %s %d\n' % (item['ename'], price/10000), timeout =10)
            if (cmp(item['name'], '公仔玩偶店') == 0 and (price > 1220000)) \
               or (cmp(item['name'], '中餐厅') == 0 and (price >=1800000)) \
               or (cmp(item['name'], '彩票投注站') == 0 and (price > 1140000))\
               or (cmp(item['name'], '珍珠头冠') == 0 and (price >= 1380000)) \
               or (cmp(item['name'], '个性LOFT') == 0 and (price >=4600000)) \
               or (cmp(item['name'], '时尚公寓') == 0 and (price>=1760000)) \
               or (cmp(item['name'], '粉红钻石') == 0 and (price >=18000000)) \
               or (cmp(item['name'], '超级跑车') == 0 and (price >= 51500000)) \
               or (cmp(item['name'], '豪华别墅') == 0 and (price >= 28500000)) \
               or (cmp(item['name'], 'SPA养生会所') == 0 and (price >= 24000000)) \
               or (cmp(item['name'], '轰炸机') == 0 and (price >= 53000000)) \
               or (cmp(item['name'], '豪华腕表') == 0 and (price >= 5350000)) \
               or (cmp(item['name'], '人造卫星') == 0 and (price >= 108000000)) :
               item['buy_sell'] = 1
               PySnarl.snShowMessage("Reminder", 'Item to Sell: %s %d\n' % (item['ename'], price/10000), timeout =10)

            if (cmp(item['name'], '公仔玩偶店') == 0 and (price <=1020000 or price > 1220000)) \
               or (cmp(item['name'], '中餐厅') == 0 and (price <= 1600000 or price >=1800000)) \
               or (cmp(item['name'], '彩票投注站') == 0 and (price <=1020000 or price > 1140000))\
               or (cmp(item['name'], '珍珠头冠') == 0 and (price <=1140000 or price >= 1380000)) \
               or (cmp(item['name'], '个性LOFT') == 0 and (price <=4000000 or price >=4600000)) \
               or (cmp(item['name'], '时尚公寓') == 0 and (price <=1300000 or price>=1760000)) \
               or (cmp(item['name'], '粉红钻石') == 0 and (price <=15500000 or price >=18000000)) \
               or (cmp(item['name'], '超级跑车') == 0 and (price < 47000000 or price >51500000)) \
               or (cmp(item['name'], '豪华别墅') == 0 and (price <= 25000000 or price >=28500000)) \
               or (cmp(item['name'], 'SPA养生会所') == 0 and (price <= 20400000 or price >=24000000)) \
               or (cmp(item['name'], '轰炸机') == 0 and (price <= 46000000 or price >=53000000)) \
               or (cmp(item['name'], '豪华腕表') == 0 and (price <= 4800000 or price >=5400000)) \
               or (cmp(item['name'], '金融街') == 0 and (price <= 92000000)) \
               or (cmp(item['name'], '人造卫星') == 0 and (price <=92000000 or price >= 108000000)) :
               #PySnarl.snShowMessage("Hot Item", '***HOT ITEM TO DEAL!***\n %s: %d\n' % (item['ename'], price), timeout =10)

             if (0):     
               # 邮件服务器地址
               mailserver = "smtp.gmail.com"
               # 邮件用户名
               username = "dwbush@gmail.com"
               # 密码
               password = "abcdefg"
               # smtp会话过程中的mail from地址
               from_addr = "abcd@gmail.com"
               # smtp会话过程中的rcpt to地址
               #to_addr = "supertycoon@googlegroups.com"
               to_addr = "efgh@gmail.com"
               # 信件内容
               if (item['buy_sell'] == 1):
                  msg = "卖出：%s 现在的价格是: %d " %(item['name'], price)
               else: 
                  msg = "买入：%s 现在的价格是: %d " %(item['name'], price)
               svr = smtplib.SMTP(mailserver, 587)
               # 设置为调试模式，就是在会话过程中会有输出信息
               svr.set_debuglevel(1)
               # ehlo命令，docmd方法包括了获取对方服务器返回信息
               svr.docmd("EHLO server")
               svr.starttls() # <------ 这行就是新加的支持安全邮件的代码！
               # auth login 命令
               svr.docmd("AUTH LOGIN")
               # 发送用户名，是base64编码过的，用send发送的，所以要用getreply获取返回信息
               svr.send(base64.encodestring(username))
               svr.getreply()
               # 发送密码
               svr.send(base64.encodestring(password))
               svr.getreply()
               # mail from, 发送邮件发送者
               svr.docmd("MAIL from: <%s>" % from_addr)
               # rcpt to, 邮件接收者
               svr.docmd("RCPT TO: <%s>" %(to_addr))
               #svr.docmd("RCPT TO: <'dearyong@gmail.com'>, <'ahyong@gmail.com'>")
               # data命令，开始发送数据
               svr.docmd("DATA")
               svr.send("SUBJECT: [Kaixin] Price Change Reminder\n\n")
               # 发送正文数据
               svr.send(msg)
               # 比如以\r\n.\r\n作为正文发送结束的标记
               svr.send("\r\n.\r\n")
               svr.getreply()
               # 发送结束，退出
               svr.quit()
               print
            if gblBuyMonitoringEnabled and item['buyThreshold'] is not None and price <= item['buyThreshold']:
              bBuyAlerted = True
              fout.write('%s ★***HOT ITEM TO BUY!***★ %s:%d\n' % (datetime.datetime.now().strftime('%m-%d %H:%M:%S'), item['name'], price))
            elif gblSellMonitoringEnabled and item['sellThreshold'] is not None and price >= item['sellThreshold']:
              bSellAlerted = True
              fout.write('%s ★***TIME TO SELL!***★ %s:%d\n' % (datetime.datetime.now().strftime('%m-%d %H:%M:%S'), item['name'], price))
            else:
              fout.write('%s: %s:%d\n' % (datetime.datetime.now().strftime('%m-%d %H:%M:%S'), item['name'], price))

            break

      # process the next line
      line = handle.readline()

    handle.close()

  fout.close()

  if bBuyAlerted:
    #gblLogger.debug('Hot Item(s) detected!!!')
    print ("\r"),
    PySnarl.snShowMessage("Buy", "Double check the items?", timeout =10)

  if bSellAlerted:
    #gblLogger.debug('Hot Item(s) detected!!!')
    print ("\r"),
    PySnarl.snShowMessage("Sell", "Double check the items?", timeout =10)

  #gblLogger.debug('Parsed URL - Kaixin super business man market')

while True:
  print("                         \r"),
  print("Running ...\r"),
  checkPrice()
  i= 120
  while i > 0:
    print("                         \r"),
    print("%s, %d sec left\r" %(datetime.datetime.now().strftime('%H:%M:%S'), i)),
    time.sleep(1)
    i = i - 1
  