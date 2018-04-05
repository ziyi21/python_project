# -*- coding: utf-8 -*-
# 作者:孔翔玉

# 引入需要的第三方库
import time
import urllib
from bs4 import BeautifulSoup
import ctypes
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import xlrd
from faker import Factory #它可以生成很多模拟的数据，如user-agent
f = Factory.create()


def open_excel(file):
    try:
        book = xlrd.open_workbook(file)
        return book
    except Exception as e:
        print ('打开工作簿'+file+'出错：'+str(e))
        return None


def read_sheets(file):
    try:
        book = open_excel(file)
        sheets = book.sheets()
        return sheets
    except Exception as e:
        print('读取工作表出错：'+str(e))
        return None


def read_data(sheet, n=0):
    dataset = []
    for r in range(sheet.nrows):
        col = sheet.cell(r, n).value
        dataset.append(col)
    return dataset

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = f.user_agent()
service_args = [
'--proxy=116.62.237.194:80',
'--proxy-type=http'
  ]
# open_driver = webdriver.PhantomJS(executable_path='D:/Anaconda2/phantomjs.exe', desired_capabilities=dcap, service_args=service_args )
# 启动浏览器，executable_path路径要根据自己chromedriver.exe的位置更改
# driver = webdriver.Chrome(executable_path=r'E:\EXE\EXE\chromedriver_win32\chromedriver',  desired_capabilities=dcap, service_args=service_args)
driver = webdriver.Chrome()
# 设置浏览器窗口位置及大小
# driver.set_window_rect(x=0, y=0, width=667, height=748)
# 设定页面加载限制时间
driver.set_page_load_timeout(60)
# 设置锁定标签等待时长
wait = WebDriverWait(driver, 30)


def get_content(url, i, waiting=5):
    driver.get(url)
    # 等待waiting秒，使js加载，时间可延长
    time.sleep(waiting)
    if 'login?' in driver.current_url:
        player = ctypes.windll.kernel32
        player.Beep(1000, 3000)
        time.sleep(50)
    # 获取网页内容
    content = driver.page_source.encode('utf-8')
    # print(content)
    if len(driver.window_handles) > 1:
        driver.close()
    res_soup = BeautifulSoup(content, 'lxml')
    return res_soup


def search(keyname, i):
    key = urllib.parse.quote(keyname)
    search_url = 'https://www.tianyancha.com/search?key=' + key + '&checkFrom=searchBox'
    print(search_url)
    res_soup = get_content(search_url, i)
    company_urls_div = res_soup.select('div.search_right_item.ml10')
    company_urls = []
    zczb_texts = []
    if len(company_urls_div) > 5:
        for i in range(5):
            company_url = company_urls_div[i].select('div a')[0].get('href')

            company_urls.append(company_url)
            zczbs = res_soup.select('div.search_right_item.ml10')[i]
            zczb = zczbs.select('div.search_row_new.pt20 div.title.overflow-width')[1].find('span').text
            zczb_texts.append(zczb)
            print('company_url:', company_url)
            print('注册资本：', zczb)
        return company_urls, zczb_texts
    elif len(company_urls_div) > 0:
        for i in range(len(company_urls_div)):
            company_url = company_urls_div[i].select('div a')[0].get('href')
            company_urls.append(company_url)
            zczbs = res_soup.select('div.search_right_item.ml10')[i]
            zczb = zczbs.select('div.search_row_new.pt20 div.title.overflow-width')[1].find('span').text
            zczb_texts.append(zczb)
            print('company_url:', company_url)
            print('注册资本：', zczb)
        return company_urls, zczb_texts
    else:
        print("不存在该公司")
        return None, None


def get_basic_info(res_soup):
    info = {}
    for i in range(1, 50):
        info['股东{}'.format(i)] = ''
        info['股东{}持股比例'.format(i)] = ''
    basics = res_soup.select('#_container_baseInfo div div.base0910 tr')
    # print(basics)
    yyqx = ''
    if basics:
        yyqx = basics[3].find_all('td')[1].text
    if yyqx:
        zcsj = yyqx.split('至')[0]  # 注册时间
        print(zcsj)
        info['注册时间'] = zcsj
    else:
        info['注册时间'] = ''
    zsfx = res_soup.select('span.selfRisk')
    if zsfx:
        info['自身风险'] = zsfx[0].text.strip()
    else:
        info['自身风险'] = ''
    print(zsfx)
    roundfrisk = res_soup.select('span.roundRisk')
    if roundfrisk:
        info['周边风险'] = roundfrisk[0].text.strip()
    else:
        info['周边风险'] = ''
    print(roundfrisk)
    out_inverst = res_soup.select('#nav-main-inverstCount span.intro-count')
    if out_inverst:
        info['对外投资'] = out_inverst[0].text.strip()
    else:
        info['对外投资'] = ''
    print(out_inverst)
    branchcount = res_soup.select('#nav-main-branchCount span.intro-count')
    if branchcount:
        info['分支机构'] = branchcount[0].text
    else:
        info['分支机构'] = ''
    print(branchcount)
    core_teams = res_soup.select('.staffinfo-module-container')
    for core_team in core_teams:
        if '董事长' in core_team.text:
            info['董事长'] = core_team.find('a').text
        if '总经理' in core_team.text:
            info['总经理'] = core_team.find('a').text

    holders = res_soup.select('#_container_holder tbody tr')
    m = 1
    for holder in holders:
        print(holder.find_all('td')[0].find('a').text)
        info['股东{}'.format(m)] = holder.find_all('td')[0].find('a').text
        info['股东{}持股比例'.format(m)] = holder.find_all('td')[1].text
        print(holder.find_all('td')[1].text)
        m = m + 1
    # info['注册资本'] = str(money) + '万元'
    bidcount = res_soup.select('#nav-main-bidCount span.intro-count')
    if bidcount:
        info['招投标项目总数'] = bidcount[0].text
    print(bidcount)
    bids = res_soup.select('#_container_bid tbody tr')
    n = 0
    for bid in bids:
        print(bid.find_all('td')[1].text)
        if 'PPP' in bid.find_all('td')[1].text:
            n = n+1
    info['PPP项目数'] = n
    patentcount = res_soup.select('#nav-main-patentCount span.intro-count')
    if patentcount:
        info['专利'] = patentcount[0].text
    print(patentcount)
    print('info:', info)
    return info


def write_into(logfile, company_name):
    with open(logfile, 'a') as f:
        f.write(company_name+'\n')


def main(logfile, company_file):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cols = ['PPP项目数', '公司名称', '分支机构', '周边风险', '对外投资', '总经理', '注册时间', '注册资本', '股东1', '股东2', '股东3', '股东4', '股东5', '股东6', '股东7', '股东8', '股东9', '股东10', '股东11', '股东12', '股东13', '股东14', '股东15', '股东16', '股东17', '股东18', '股东19', '股东20', '股东21', '股东22', '股东23', '股东24', '股东25', '股东26', '股东27', '股东28', '股东29', '股东30', '股东31', '股东32', '股东33', '股东34', '股东35', '股东36', '股东37', '股东38', '股东39', '股东40', '股东41', '股东42', '股东43', '股东44', '股东45', '股东46', '股东47', '股东48', '股东49',
 '股东10持股比例', '股东11持股比例', '股东12持股比例', '股东13持股比例', '股东14持股比例', '股东15持股比例', '股东16持股比例', '股东17持股比例', '股东18持股比例', '股东19持股比例', '股东1持股比例', '股东20持股比例', '股东21持股比例', '股东22持股比例', '股东23持股比例', '股东24持股比例', '股东25持股比例', '股东26持股比例', '股东27持股比例', '股东28持股比例', '股东29持股比例', '股东2持股比例', '股东30持股比例', '股东31持股比例', '股东32持股比例', '股东33持股比例', '股东34持股比例', '股东35持股比例', '股东36持股比例', '股东37持股比例', '股东38持股比例', '股东39持股比例', '股东3持股比例', '股东40持股比例', '股东41持股比例', '股东42持股比例', '股东43持股比例', '股东44持股比例', '股东45持股比例', '股东46持股比例', '股东47持股比例', '股东48持股比例', '股东49持股比例', '股东4持股比例', '股东5持股比例', '股东6持股比例', '股东7持股比例', '股东8持股比例', '股东9持股比例', '自身风险', '董事长', '专利', '招投标项目总数']

    # 新生成一个DataFrame的变量保存爬取到的数据
    df = pd.DataFrame({})
    with open(logfile, 'a') as f:
        f.write('\n当前时间：' + now + '\n')
        sheets = read_sheets(company_file)
        cornames = []
        for sheet in sheets:
            dataset = read_data(sheet)
            cornames.extend(dataset)
        print(len(cornames))
        n = 0
        m = 0
        for i in range(len(cornames))[1000:914:-1]:
            n = n + 1
            m = m + 1
            if n > 2:
                df = df.ix[:, cols]
                df.to_csv(r'../data/company_info.csv', encoding='gbk', mode='a')
                df = pd.DataFrame({})
                n = 0
                time.sleep(300)
            if m > 200:
                m = 0
                time.sleep(600)
            urls, zczbs = search(cornames[i].strip(), i)#这个地方i是用来判断这个搜索时第几个，因为第一个往往要登陆所以给了较长的停留时间
            if urls:
                j = 0
                total_info = ''
                for url in urls:
                    soup = get_content(url, 1)
                    company_name = soup.select('div.company_header_width div.position-rel')[0].find('span').text
                    print(company_name)
                    if company_name == cornames[i].strip():

                        total_info = get_basic_info(soup)

                        total_info['注册资本'] = zczbs[j]

                        total_info['公司名称'] = cornames[i].strip()
                        print(total_info)
                        # 将获取到的单条招聘信息汇总
                        df = df.append(total_info, ignore_index=True)
                        print('查询成功。')
                        break
                    j = j + 1
                if not total_info:
                    print(cornames[i].strip() + '  查询失败。')
                    write_into(logfile, cornames[i])
            else:
                print(cornames[i].strip() + '  查询失败。')
                write_into(logfile, cornames[i])

    # df = df.ix[:, (df != df.ix[0]).any()]
    # 将爬取到的数据存储到硬盘上，存储格式为CSV
    df = df.ix[:, cols]
    df.to_csv(r'../data/company_info.csv', encoding='gbk', mode='a')


if __name__ == '__main__':
    logfile = '../data/failed_log.txt'
    filename = r'../data/企业名称.xlsx'
    main(logfile, filename)