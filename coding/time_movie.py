#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ziyi'

from selenium import webdriver
import pandas as pd
import time

def get_movie(url):
    df = pd.DataFrame({})
    contents = {}
    driver.get(url)
    movie_url = driver.find_element_by_xpath('//*[@id="moreRegion"]/li/h3/a').get_attribute('href')
    driver.find_element_by_xpath ('//*[@id="moreRegion"]/li/h3/a').click ()
    print(movie_url)
    driver.get(movie_url)
    time.sleep(5)
    contents['movie_name'] = driver.find_element_by_xpath('//*[@id="db_head"]/div[2]/div/div[1]/h1').text
    print(contents)
    try:
        contents['movie_english_name'] = driver.find_element_by_xpath('//*[@id="db_head"]/div[2]/div/div[1]/p[2]').text
    except:
        print('没有英文名称')
    contents['movie_time'] = driver.find_element_by_xpath('//*[@id="db_head"]/div[2]/div/div[2]/span').text
    movie_classes = driver.find_elements_by_xpath('//*[@id="db_head"]/div[2]/div/div[2]//a[@property="v:genre"]')
    classes = []
    for classify in movie_classes:
        classes.append(classify.text.encode('gbk','ignore').decode('gbk'))
    contents['movie_classify'] = ','.join(one for one in classes)
    contents['movie_show_time'] = driver.find_element_by_xpath('//*[@id="db_head"]/div[2]/div/div[2]/a[last()]').text
    contents['movie_introduce_videos'] = driver.find_element_by_xpath('//*[@id="movieNavigationRegion"]/dd[1]/a').text
    contents['movie_introduce_pictures'] = driver.find_element_by_xpath('//*[@id="movieNavigationRegion"]/dd[2]/a').text
    contents['movie_introduce_actors'] = driver.find_element_by_xpath('//*[@id="movieNavigationRegion"]/dd[3]/a').text
    contents['movie_introduce_comments'] = driver.find_element_by_xpath('//*[@id="movieNavigationRegion"]/dd[4]/a').text
    contents['movie_introduce_news'] = driver.find_element_by_xpath('//*[@id="movieNavigationRegion"]/dd[5]/a').text
    contents['movie_scores'] = driver.find_element_by_xpath('//*[@id="ratingRegion"]/div[1]/b').text
    contents['movie_scores_total'] = driver.find_element_by_xpath('//*[@id="ratingRegion"]/div[1]/p').text
    contents['movie_income'] = driver.find_element_by_xpath('//*[@id="ratingRegion"]/div[2]/span').text
    contents['movie_cinema'] = driver.find_element_by_xpath ('//*[@id="descripRegion"]/div/div/div[1]/b[1]').text
    contents['movie_play_times'] = driver.find_element_by_xpath('//*[@id="descripRegion"]/div/div/div[1]/b[2]').text
    contents['movie_director'] = driver.find_element_by_xpath('//*[@id="movie_warp"]/div[2]/div[3]/div/div[4]/div[2]/div[1]/div[2]/div[1]/dl/dd[1]/a').text
    contents['movie_scenarist'] = driver.find_element_by_xpath('//*[@id="movie_warp"]/div[2]/div[3]/div/div[4]/div[2]/div[1]/div[2]/div[1]/dl/dd[2]').text
    contents['movie_country'] = driver.find_element_by_xpath('//*[@id="movie_warp"]/div[2]/div[3]/div/div[4]/div[2]/div[1]/div[2]/div[1]/dl/dd[3]/a').text
    contents['movie_company'] = driver.find_element_by_xpath('//*[@id="movie_warp"]/div[2]/div[3]/div/div[4]/div[2]/div[1]/div[2]/div[1]/dl/dd[4]/a').text
    driver.find_element_by_xpath('//*[@id="movie_warp"]/div[2]/div[3]/div/div[4]/div[2]/div[1]/div[2]/div[1]/dl/dt/p[2]/a').click()
    time.sleep(3)
    contents['movie_introduction'] = driver.find_element_by_xpath('//*[@id="paragraphRegion"]/div/div[2]/div[2]/p[2]').text
    # '//*[@id="paragraphRegion"]/div/div[3]/div[2]/p[1]'
    # '//*[@id="paragraphRegion"]/div/div[4]/div[2]/p[1]'
    # '//*[@id="paragraphRegion"]/div/div[2]/div[2]/p[2]'
    comments_url = driver.find_element_by_xpath ('//*[@id="movieNavigationRegion"]/dd[5]/a').get_attribute('href')
    print(comments_url)
    if contents['movie_introduce_comments'] == '999+ 条影评':
        driver.find_element_by_xpath ('//*[@id="movieNavigationRegion"]/dd[5]/a').click ()
        print('bingo')
        time.sleep (2)
        driver.get(comments_url)
        time.sleep(3)
        contents['movie_long_comments'] = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/ul/li[1]/a').text.split('(')[-1].split(')')[0]
        contents['movie_short_comments'] = driver.find_element_by_xpath ('//html/body/div[5]/div/div[1]/ul/li[2]/a').text.split('(')[-1].split(')')[0]
        contents['movie_introduce_comments'] = int(contents['movie_short_comments'])+int(contents['movie_long_comments'])
    print(contents)
    df = df.append(contents, ignore_index=True)
    return df,comments_url

def get_comments_basic(comment_url):
    next_page = None
    driver.get(comments_url)
    time.sleep (3)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (2)
    driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')
    time.sleep (2)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (2)
    pages = driver.find_elements_by_xpath('//*[@id="PageNavigator"]/a')
    all_pages = len(pages)-2
    return all_pages

def get_long_comments(comments_url,pages):
    df = pd.DataFrame({})
    long_comments = {}
    comments_content_url = []
    writer_url = []
    have_score = None
    top = None
    driver.get(comments_url)
    time.sleep (3)
    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep (2)
    driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')
    time.sleep (2)
    movie_long_comments = driver.find_element_by_xpath ('/html/body/div[5]/div/div[1]/ul/li[1]/a').text.split ('(')[-1].split (')')[0]
    print(movie_long_comments)
    # long_comments_one = driver.find_element_by_xpath ('//*[@id="reviewRegion"]/dl[1]/dd[1]/div[1]/h3/a')
    # print(long_comments_one)
    for page in range(pages):
        next_page = None
        try:
            next_page = driver.find_element_by_xpath('//*[@id="key_nextpage"]')
        except:
            print('已经翻到最后一页了')
        finally:
            next_page = next_page
        if next_page or page:
            long_comments_list = driver.find_elements_by_xpath('//*[@id="reviewRegion"]/dl[@class="clearfix"]')
            for i,one_comments in enumerate(long_comments_list):
                print(i+1, one_comments)
                long_comments['header_name'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[1]/div[1]/h3/a'.format(i+1)).text
                long_comments['comment_href'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[1]/div[1]/h3/a'.format(i+1)).get_attribute('href')
                long_comments['praise'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[1]/div[2]/a[1]'.format(i+1)).text
                long_comments['share'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[1]/div[2]/a[2]'.format(i+1)).text
                long_comments['comments'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[1]/div[2]/a[3]'.format(i+1)).text
                long_comments['writer'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[2]/div/p[1]/a'.format(i+1)).text
                long_comments['writer_url'] = one_comments.find_element_by_xpath ('//*[@id="reviewRegion"]/dl[{}]/dd[2]/div/p[1]/a'.format(i+1)).get_attribute('href')
                long_comments['pubtime'] = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[2]/div/p[2]/a'.format(i+1)).text
                try:
                    have_score = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dd[2]/div/p[3]/span'.format(i+1)).text
                except:
                    print('该用户未进行评分')
                finally:
                    long_comments['score'] = have_score

                try:
                    top = one_comments.find_element_by_xpath('//*[@id="reviewRegion"]/dl[{}]/dt'.format(i+1)).text.replace('\n','')
                except:
                    print('该影评非top')
                finally:
                    long_comments['top'] = top
                long_comments['savetime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
                # print (long_comments)
                comments_content_url.append(long_comments['comment_href'])
                writer_url.append(long_comments['writer_url'])
                # long_comments['comment_content'] = get_comments_content(long_comments['comment_href'])
                # long_comments['people_location'],long_comments['people_constellatory'],long_comments['people_gender'] = get_people_infor(long_comments['writer_url'])
                df = df.append(long_comments, ignore_index=True)
                print (long_comments)
            if next_page:
                next_page.click ()
                time.sleep(3)
    return df,comments_content_url,writer_url

def get_comments_content(comment_content_url):
    comments_content = {}
    for one_content_url in comment_content_url:
        driver.get(one_content_url)
        time.sleep(3)
        content = '\n'.join(p.text for p in driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[3]//p'))
        comments_content[one_content_url] = content
        print('评论的内容获取成功')
    print(comments_content)
    return comments_content

def get_people_infor(people_url):
    writer_infro = {}
    for one_url in people_url:
        driver.get(one_url)
        time.sleep(3)
        driver.set_page_load_timeout (15)
        writer_infro['people_location'] = driver.find_element_by_xpath('//*[@id="left_col"]/div[1]/div/div/div[1]/div/div[2]/p[1]/span').text
        writer_infro['people_constellatory'] = driver.find_element_by_xpath('//*[@id="left_col"]/div[1]/div/div/div[1]/div/div[2]/p[2]').text.split('')[-1]
        writer_infro['people_gender'] = driver.find_element_by_xpath ('//*[@id="left_col"]/div[1]/div/div/div[1]/div/div[2]/p[2]').text.split ('')[1]
        print('评论者信息获取成功')
    return writer_infro

def get_short_comments(comments_url):
    df = pd.DataFrame({})
    short_comments = {}
    driver.get(comments_url)
    time.sleep (3)
    movie_short_comments = driver.find_element_by_xpath ('//html/body/div[5]/div/div[1]/ul/li[2]/a').text.split ('(')[-1].split (')')[0]
    short_comments_href = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/ul/li[2]/a').get_attribute('href')
    driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/ul/li[2]/a').click()
    driver.get(short_comments_href)
    time.sleep(2)
    short_comments['savetime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    a = driver.find_element_by_xpath('//*[@id="tweetRegion"]/dd[1]/div/h3').text
    print(a)
    # long_comments_list = driver.find_elements_by_xpath('#reviewRegion/dl[@class="clearfix"]')


def save_info(contents, name):
    df = pd.DataFrame()
    df = df.append(contents.copy())
    df.to_csv(r'data\movie\{}.csv'.format(name), encoding='gbk',)


if __name__ == '__main__':
    movie_name = '头号玩家'
    url = 'http://search.mtime.com/search/?q={}'.format (movie_name)
    driver = webdriver.Chrome (executable_path=r'D:\ksdler\chromedriver_win32_new\chromedriver')
    # contents, comments_url = get_movie(url)
    # save_info(contents,movie_name)
    comments_url = 'http://movie.mtime.com/219107/comment.html'
    # pages = get_comments_basic(comments_url)
    # long_comments, comment_content_url, writer_url = get_long_comments(comments_url, pages)
    # save_info(long_comments, movie_name+'_long_comments_basic')
    # get_comments_content(comment_content_url)
    # get_people_infor(writer_url)

    get_short_comments(comments_url)






