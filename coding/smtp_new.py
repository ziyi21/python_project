#-*- encoding: utf-8 -*-
'''
函数说明：Send_email_text() 函数实现发送带有附件的邮件，可以群发，附件格式包括：xlsx,pdf,txt,jpg,mp3等
参数说明：
    1. subject：邮件主题
    2. content：邮件正文
    3. filepath：附件的地址, 输入格式为["","",...]
    4. receive_email：收件人地址, 输入格式为["","",...]
'''
from email.header import Header
from email import encoders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import datetime


def Send_email_text(subject, content, filepath, receive_email):
    # sender = "digitalplanet@163.com"
    sender = "haxidata@163.com"
    passwd = "kong368534"
    receivers = receive_email  # 收件人邮箱

    msgRoot = MIMEMultipart()

    msgRoot['From'] = sender
    msgRoot['To'] = receivers

    # if len(receivers) > 1:
    # 	# msgRoot['To'] = receivers[0]  # 群发邮件
    # 	msgRoot['To'] = receivers[0]
    # 	msgRoot['CC'] = receivers[1]
    # 	# msgRoot['Bcc'] = ','.join(receivers[2:])
    # else:
    # 	msgRoot['To'] = receivers[0]

    #     添加图片
    fp = open('data/img/有你Offer公众号.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    msgRoot['Subject'] = subject
    part = MIMEText(content)
    msgRoot.attach(part)

    # html格式构造
    html = """
            <html> 
              <head></head> 
              <body> 
                  <p>
                    %s
                   <br><img src="cid:image1"></br> 
                  </p>
              </body> 
            </html> 
            """ % (content)
    htm = MIMEText(html, 'html', 'utf-8')
    msgRoot.attach(htm)

    ##添加附件部分
    for path in filepath:
        if ".jpg" in path or ".png" in path:
            # jpg类型附件
            jpg_name = path.split("/")[-1]
            part = MIMEApplication(open(path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=('gbk', '',jpg_name))
            msgRoot.attach(part)

        if ".pdf" in path:
            # pdf类型附件
            pdf_name = path.split("/")[-1]
            part = MIMEApplication(open(path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=pdf_name)
            msgRoot.attach(part)

        if ".xlsx" in path:
            # xlsx类型附件
            xlsx_name = path.split("/")[-1]
            part = MIMEApplication(open(path, 'rb').read())
            # part.add_header('Content-Disposition', 'attachment', filename=xlsx_name)
            part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', xlsx_name))
            # encoders.encode_base64(part)
            msgRoot.attach(part)

        if ".txt" in path:
            # txt类型附件
            txt_name = path.split("/")[-1]
            part = MIMEApplication(open(path, 'rb').read())
            # part.add_header('Content-Disposition', 'attachment', filename=txt_name)
            part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', txt_name))
            encoders.encode_base64(part)
            msgRoot.attach(part)


        if ".mp3" in path:
            # mp3类型附件
            mp3_name = path.split("/")[-1]
            part = MIMEApplication(open(path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=mp3_name)
            msgRoot.attach(part)

    try:
        # s = smtplib.SMTP()
        # s.set_debuglevel(1)
        # print(msgRoot.as_string())
        s = smtplib.SMTP()
        s.connect("smtp.163.com")  # 这里我使用的是阿里云邮箱,也可以使用163邮箱：smtp.163.com
        s.login(sender, passwd)
        s.sendmail(sender, receivers, msgRoot.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error, 发送失败")
    finally:
        s.quit()


subject = "2019届校招内推汇总表（更新至8.28）-有你Offer出品"
content = '小主，您的秋招内推汇总到了，请查收！感谢订阅有你Offer的秋招内推信息服务，有你Offer是面向全球求职者的一站式求职服务平台。我们拥有海量的实习信息、求职干货和就业指导，并提供1v1简历指导课程及1v1面试指导课程，助您斩获理想的offer~更多详情敬请关注【有你Offer】公众号~'
jpg_path = 'data/img/有你Offer公众号.jpg'
# pdf_path = "c.pdf"
# txt_path = "d\\e\\f.txt"
xlsx_path = "data/work/2019届校招内推汇总表（更新至8.28）-有你Offer出品.xlsx"
file_path = [xlsx_path]  #发送三个文件到两个邮箱
test_email = ['635516607@qq.com']
receive_email1 = ['vita.yuhua.zhang@outlook.com']
# receive_email1 = ['1428941524@qq.com','haxidata@163.com', 'kiisxx1993727@gmail.com', '744568921@qq.com']#"1428941524@qq.com",'744568921@qq.com'，'fsltus@126.com','haxidata@163.com', 'kiisxx1993727@gmail.com', 'fsltus@126.com'
receive_email2 = ["1428941524@qq.com",'744568921@qq.com','haxidata@163.com', 'kiisxx1993727@gmail.com',]#"1428941524@qq.com",'744568921@qq.com'，'fsltus@126.com','haxidata@163.com', 'kiisxx1993727@gmail.com', 'fsltus@126.com'
receive_email3 = ["1428941524@qq.com",'744568921@qq.com','haxidata@163.com', 'kiisxx1993727@gmail.com',]#"1428941524@qq.com",'744568921@qq.com'，'fsltus@126.com','haxidata@163.com', 'kiisxx1993727@gmail.com', 'fsltus@126.com'
receive_email4 = ["1428941524@qq.com",'744568921@qq.com','haxidata@163.com', 'kiisxx1993727@gmail.com',]#"1428941524@qq.com",'744568921@qq.com'，'fsltus@126.com','haxidata@163.com', 'kiisxx1993727@gmail.com', 'fsltus@126.com'

sep0908 = [
    'yangxiaoxiaotom@163.com',
    'xiaoyannju@foxmail.com',
    'g1w99x588@163.com',
    'shiyuhuang18@163.com',
    '602621267@qq.com',
    'wanmengdamon@gmail.com'
       ]

sep0910 = [
    '491660265@qq.com',
    'xchen6426@163.com',
    'fxg032zjc@163.com',
    '850094297@qq.com',
    '853202596@qq.com',
    '39821737@qq.com',
    '616394890@qq.com',
    '1486636925@qq.com',
    'vanilla_my@foxmail.com',
    '330594115@qq.com'
       ]

sep0912 = [
    'wy312336@163.com',
    '2803351027@qq.com',
    'xt17510@163.com',
    '13051606766@163.com',
    '945262781@qq.com',
    '978864796@qq.com',
    '493190776@qq.com',
]

sep0914 = [
    '1242310252@qq.com',
    '939535997@qq.com',
]

sep0916 = [
    '976932442@qq.com'
]

nov1108 = [
    '744568921@qq.com',
    'haxidata@163.com',
    'fsltus@126.com',
    'jieeliao@qq.com',
    'licong6990@outlook.com',
    '380521340@qq.com',
    'sulunkang@163.com',
    '812299133@qq.com',
    '575546908@qq.com',
    'tajiaayan@126.com',
    'chlw25@163.com',
    '892893234@qq.com',
    'dongxinyuancrystal@163.com',
    'lenagulina@163.com',
    'xuy2017@mpacc.nai.edu.cn',
    '532817138@qq.com',
    '1723041930@qq.com',
    'wymm520@126.com',
    '441811919@qq.com',
    '334679466@qq.com',
    '2044750616@qq.com',
    'taomy0522@163.com',
    'yeq1702@126.com',
    '18810589317@163.com',
]

nov1110 = [
    '491660265@qq.com',
    '641213180@qq.com',
    '2523698440@qq.com',
    '1175618019@qq.com',
    'mistmichael1994@gmail.com',
    '13322457055@163.com',
    '1427843763@qq.com',
    '2545546799@qq.com',
    '1043460563@qq.com',
    '513305365@qq.com',
    '531292087@qq.com',
    '602589698@qq.com',
    '991891149@qq.com',
    'shibocheng33@foxmail.com',
    '545333288@qq.com',
    '447945592@qq.com',
    'sun125210206@hotmail.com',
    'minying.kong@outlook.com',
    '775642161@qq.com',
    '1262119059@qq.com',
    'qiaodan13@yeah.net',
    'andrewchia@foxmail.com',
]

nov1112=[
    'yyxgio94@163.com',
    'cynthiafu9508@gmail.com',
    'liu.yaqi@husky.neu.edu',
    'jihoyi@foxmail.com',
    '1604858331@qq.com',
    'Adley_Ren@163.com',
    '745594319@qq.com',
    '729774384@qq.com',
    'vanorazyw@163.com',
    'zjhseu1995@163.com',
    '1214268412@qq.com',
    'vita.yuhua.zhang@outlook.com',
    '516601367@qq.com',
    'plus_wqn@163.com',
    'sqteen177@163.com',
    '690793055@qq.com',
    '464081842@qq.com',
    '939540558@qq.com',
    'litmary@163.com',
    '574205255@qq.com',
    'Lindsayemp@163.com',
]

nov1114 = [
    '897988295@qq.com',
    'rl_96118@163.com',
    '554631355@qq.com',
    'chengyusun18@163.com',
    '871558974@qq.com',
    '295988190@qq.com',
    'vita.yuhua.zhang@outlook.com',
    '1213767565@qq.com',
    'fantasticbaobao@163.com'
]

nov1116 = [
    'sherodjs@163.com'
]

nov1124 = [
    '473155897@qq.com'
]

nov1126 = [
    '741301256@qq.com',
    '3294674415@qq.com',
    '1029696036@qq.com',
]

nov1128 = [
    'wangyue0710@163.com',
]

vip = [
    'wangyue0710@163.com',
]

shiyong0814 = [
    '827089838@qq.com',
    '1083286282@qq.com',
    '250270834@qq.com',
    'yaodanuan@163.com',
    '13842025635@163.com',
    'rl_96118@163.com',
    'domixsean@outlook.com',
    'sh534367384@163.com',
    '294978075@qq.com',
    '18025576158@163.com',
    '1461300468@qq.com',
    '1194011352@qq.com',
    '2601094287@qq.com',
    '179601373@qq.com',
    '1604858331@qq.com',
    'lixiaofeibj@163.com',
    '13146981615@163.com',
    'hejingjinghz@163.com',
    '406228304@qq.com',
    '1620626489@qq.com',
    'alanguohello@163.com',
    '1186344741@qq.com',
    '171743566@qq.com',
    '15917175129@163.com',
    '599146834@qq.com',
    'huhuiqin24@163.com',
]



shiyong0816 = [
    'chuchupray@126.com',
    'lz392@georgetown.edu',
    'jinwy1105@163.com',
    'CassiopeiaElina@163.com',
    'sdkjdxhxy@163.com',
    '3156287385@qq.com',
]
shiyong0818 = [
    'jm0917@126.com',
    '214297458@qq.com',
    '290546789@qq.com',
    'xu944678895@163.com',
    '1608175731@qq.com',
    'wangyue0710@163.com',
    '1823682250@qq.com',
]
shiyong0820 = [
    '3048814801@qq.com',
    'qianyjtd@gmail.com',
    'wangying920205@126.com',
    '2462806920@qq.com',
    '877725901@qq.com',
    '374380547@qq.com',
    '978764156@qq.com',
    '515638594@qq.com',
    'waiyuzhaodan@163.com',
    'zhangxinyi_d@163.com',
    '18845796314@163.com',
    '974303861@qq.com',
    '314545988@qq.com',
    '328820975@qq.com',
    'hrx19960118@outlook.com',
    '2284013920@qq.com',
    '1099802150@qq.com',
    '499210390@qq.com',
    'lesleyrae88@hotmail.com',
    '1592380482@qq.com',
    '515638594@qq.com',
    '2366690017@qq.com',
    'esx56487@qq.com',
    '575206410@qq.com',
    '785584249@qq.com',
    '1582667364@qq.com',
    '1181990832@qq.com',
    'fanzixuan121@163.com',
    '1297581142@qq.com',
    'chan_suetying@163.com',
    '949485172@qq.com',
    'xili9459@uni.sydney.edu.au',
    'shilili0310@126.com',
    '821943130@qq.com',
    '708844241@qq.com',
    '956329053@qq.com',
    'dwq_1993@163.com',
    '811637478@qq.com',
    '18731203083@163.com',
    'xuexx207@hotmail.com',
    '1551545227@qq.com',
    '503003972@qq.com',
    '409073748@qq.com',
    'whl1203296651@qq.com',
    '1033492896@qq.com',
    'praha_wang@163.com',
    '635936876@qq.com',
    '421163021@qq.com',
    'sannalulu@126.com',
    '18895635091@163.com',
    'qiuyurui21@163.com',
    'sybil24@yeah.net',
    '2213855318@qq.com',
    '1723198738@qq.com',
    '44632290@qq.com',
    'dairuyi940615@163.com',
    'wuqingyi_job@163.com',
    '619230050@qq.com',
    '1539501382@qq.com',
    'mrq007@yeah.net',
    '544594786@qq.com',
    '850695156@qq.com',
    '879127500@qq.com',
    'zhutaomine@foxmail.com',
    '1260739661@qq.com',
    '512581502@qq.com',
    'm18211091722@163.com',
    'ddzeggs@163.com'
]
#
# for emails in [sep0908, sep0910, sep0912, sep0914, sep0916, nov1108, nov1110, nov1112, nov1114, nov1116, nov1124, nov1126,nov1124,nov1126,nov1128,vip]:
#     for receive_email in emails:
#         print(receive_email)
#         Send_email_text(subject, content, file_path, receive_email)

# for emails in [receive_email1]:
#     for receive_email in emails:
#         print(receive_email)
#         Send_email_text(subject, content, file_path, receive_email)

for emails in [test_email]:
    for receive_email in emails:
        print(receive_email)
        Send_email_text(subject, content, file_path, receive_email)

# Send_email_text(subject, content, file_path, receive_email)
# Send_email_text(subject, content, file_path, sep0908)
# Send_email_text(subject, content, file_path, sep0910)
# Send_email_text(subject, content, file_path, nov1108)
# # Send_email_text(subject, content, file_path, nov1110)
# Send_email_text(subject, content, file_path, shiyong0814)
# Send_email_text(subject, content, file_path, shiyong0816)
