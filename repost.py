'''
Description: 获取特定微博的转发信息
Author: Junwen Yang
Date: 2023-04-19 02:44:59
LastEditTime: 2023-12-20 17:57:45
LastEditors: Junwen Yang
'''
import json
import requests
import time
from lxml import etree
import os
from urllib.parse import parse_qs
import fake_useragent
import random
import datetime
import pandas as pd
import openpyxl
from openpyxl import Workbook
import re
import socket
import warnings
warnings.filterwarnings('ignore')




def get_fake_IP():
    """获取伪装IP

    Returns:
        str: 伪装IP
    """
    ip_page = requests.get(  # 获取200条IP
        'http://api.89ip.cn/tqdl.html?api=1&num=300&port=&address=&isp=')
    proxies_list = re.findall(
        r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)(:-?[1-9]\d*)',
        ip_page.text)

    # 转换proxies_list的元素为list,最初为'tuple'元组格式
    proxies_list = list(map(list, proxies_list))

    # 格式化ip  ('112', '111', '217', '188', ':9999')  --->  112.111.217.188:9999
    for u in range(0, len(proxies_list)):
        # 通过小数点来连接为字符
        proxies_list[u] = '.'.join(proxies_list[u])
        # 用rindex()查找最后一个小数点的位置，
        index = proxies_list[u].rindex('.')
        # 将元素转换为list格式
        proxies_list[u] = list(proxies_list[u])
        # 修改位置为index的字符为空白（去除最后一个小数点）
        proxies_list[u][index] = ''
        # 重新通过空白符连接为字符
        proxies_list[u] = ''.join(proxies_list[u])

    return "'" + random.choice(proxies_list) + "'"




def extract_location(string):
    """从微博的IP信息中解析出地址

    Args:
        string (str): 微博IP信息
    Returns:
        str: 地址
    """
    if string == None:
        return ''
    elif '发布于 ' in string:
        return string.split('发布于 ')[-1].strip()
    else:
        return string


def append_dict_to_dataframe(info_dict:dict, repo_col:list) -> pd.DataFrame:
    """
    将字典按照DataFrame列顺序添加到DataFrame中
    """
    # 将字典按照DataFrame列顺序重排
    df_info = pd.DataFrame(columns=repo_col)
    info_dict_sorted = {col: info_dict[col] for col in df_info.columns}
    
    # 将d_sorted的值添加到DataFrame中
    df_info = df_info._append(info_dict_sorted, ignore_index=True)
    
    return df_info

def extract_device(text):
    """从发布终端数据中提取出终端信息

    Args:
        text (str): 发布终端信息

    Returns:
        str: 终端信息
    """
    
    # 有些终端信息是空的，需要单独处理
    if text == None:
        return ''
    else:
        # 正则表达式匹配
        pattern = r'<a.*?>(.*?)<\/a>'
        result = re.search(pattern, text)
        
        if result:
            return result.group(1)
        else:
            return text



def format_datetime(datetime_str):
    """将微博的时间信息转化为更易读的格式

    Args:
        datetime_str (str): 微博的时间信息

    Returns:
        str: 更易读的时间信息
    """
    
    # 解析字符串为日期时间对象
    dt = datetime.datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %z %Y')
    
    # 格式化日期时间对象为指定的字符串格式
    return '{0:%Y}-{0.month}-{0.day} {0:%H:%M:%S} {0:%a}'.format(dt)


def Number_unit_conversion(number: str) -> str:
    """将微博的数字转换为纯数字

    Args:
        number (str): 微博的数字
    Returns:
        str: 纯数字
    """
    if type(number) == int:
        return str(number)
    elif number[-1] == '万':
        return str(int(float(number[:-1])*10000))
    elif number[-1] == '亿':
        return str(int(float(number[:-1])*100000000))
    else:
        return number


def Get_User_Info(user_id: str, headers:dict) -> dict:
    """
    根据微博的id获取用户的各项资料
    -------------
    userInfo中的keys:
    'id', 'screen_name', 'profile_image_url', 'profile_url', 'statuses_count', 'verified', 'verified_type', 'close_blue_v', 'description', 'gender', 'mbtype', 'svip', 'urank', 'mbrank', 'follow_me', 'following', 'follow_count', 'followers_count', 'followers_count_str', 'cover_image_phone', 'avatar_hd', 'like', 'like_me', 'toolbar_menus'
    """

    proxy = {
        'http':'127.0.0.1:7890',
        'https':'127.0.0.1:7890'
    }

    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value="+str(user_id)
    user_info = requests.get(url, headers=headers, proxies=proxy).json()
    with open('user_info.json', 'w', encoding='utf-8') as f:
        json.dump(user_info, f, ensure_ascii=False, indent=4)
    user_info = user_info['data']['userInfo']
    
    user_info_dict = {
        '用户编号': user_info['id'],
        '昵称': user_info['screen_name'],
        '微博数量': user_info['statuses_count'],
        '关注数': Number_unit_conversion(user_info.get('follow_count')),
        '粉丝数': Number_unit_conversion(user_info.get('followers_count')),
        '个人简介': user_info.get('description'),
        '性别': user_info.get('gender'),
        '认证原因': user_info.get('verified_reason'),
        '是否会员': '是' if user_info['mbtype'] > 2 else '否',
        '会员等级': user_info['mbrank'],
        '微博等级': user_info.get('urank')
    }
    
    return user_info_dict

#
def Get_Reposts(weibo_id: str, page:int, Cookie:str) -> dict:
    """
    根据微博的id, 当前的page数和headers获取指定页数的转发微博数据
    -------------
    data可用keys:
    'visible', 'created_at', 'id', 'idstr', 'mid', 'mblogid', 'user', 'can_edit', 'text_raw', 'text', 'annotations', 'source', 'favorited', 'cardid', 'pic_ids', 'geo', 'pic_num', 'is_paid', 'pic_bg_new', 'mblog_vip_type', 'number_display_strategy', 'reposts_count', 'comments_count', 'attitudes_count', 'attitudes_status', 'isLongText', 'mlevel', 'content_auth', 'is_show_bulletin', 'comment_manage_info', 'repost_type', 'share_repost_type', 'mblogtype', 'showFeedRepost', 'showFeedComment', 'pictureViewerSign', 'showPictureViewer', 'rcList', 'region_name', 'customIcons', 'retweeted_status'
    
    """
    # 在每次请求时都重新生成一个session, 应对反爬虫
    session = requests.Session()
    session.keep_alive = False
    ua = fake_useragent.UserAgent()    
    
    # 设置请求头, 伪装成浏览器
    ua = fake_useragent.UserAgent()
    headers = {
    # 随机生成的User-Agent，确保每次爬取的都是不同的User-Agent
    'User-Agent':ua.random,
    # 关闭长连接
    'Connection': 'close',
    
    # 这里输入使用的cookie
    'Cookie': Cookie
    
    }
    
    # 用于获取转发微博的url, 其中moduleID=feed是固定的，id是微博的id，page是转发信息的页数
    url = 'https://weibo.com/ajax/statuses/repostTimeline?moduleID=feed&id={}&page={}'.format(weibo_id, page)

    
    proxy = {
        'http':'127.0.0.1:7890',
        'https':'127.0.0.1:7890'
    }
    
    # 以防不明原因的连接失败，最多尝试100次requests.get
    for i in range(100):
        # 用session.get获取转发微博的json数据, 设置timeout时间为9999秒，避免因为网络原因导致的连接失败
        # repo = session.get(url, headers=headers, timeout=9999, verify=False,proxies={'http': get_fake_IP()})
        repo = session.get(url, headers=headers, timeout=9999, verify=False,proxies=proxy)

        # 若成功获取数据，则跳出循环
        if repo.status_code == 200:
            break
        
    # 若100次尝试均失败，则返回None，表示获取失败
    if repo.status_code == 400:
        print('>>>Error 400: Bad Request, 大概是被官方制裁了，休息几分钟或者换组Cookie试试吧')
        return None
    
    # 打印获取的数据，用于调试观察错误原因
    # print(repo.content.decode('utf-8')[0:200])
    
    # 解析json数据并返回
    repost_info = repo.json()
    
    # 关闭session和repo，降低内存占用和被识别的风险
    repo.close()
    session.close()
    
    return repost_info


def Get_Weibo_Info(weibo_info:dict) -> dict:
    """
    根据获取的json数据解析转发微博的各种数据
    ----------------
    可用keys:
    'visible', 'created_at', 'id', 'idstr', 'mid', 'mblogid', 'user', 'can_edit', 'text_raw', 'text', 'annotations', 'source', 'favorited', 'cardid', 'pic_ids', 'geo', 'pic_num', 'is_paid', 'pic_bg_new', 'mblog_vip_type', 'number_display_strategy', 'reposts_count', 'comments_count', 'attitudes_count', 'attitudes_status', 'isLongText', 'mlevel', 'content_auth', 'is_show_bulletin', 'comment_manage_info', 'repost_type', 'share_repost_type', 'mblogtype', 'showFeedRepost', 'showFeedComment', 'pictureViewerSign', 'showPictureViewer', 'rcList', 'region_name', 'customIcons', 'retweeted_status'
    ----------------
    root微博可用keys:
    'visible', 'created_at', 'id', 'idstr', 'mid', 'mblogid', 'user', 'can_edit', 'text_raw', 'text', 'textLength', 'annotations', 'source', 'favorited', 'buttons', 'cardid', 'pic_ids', 'pic_focus_point', 'geo', 'pic_num', 'pic_infos', 'is_paid', 'mblog_vip_type', 'number_display_strategy', 'reposts_count', 'comments_count', 'attitudes_count', 'attitudes_status', 'isLongText', 'mlevel', 'content_auth', 'is_show_bulletin', 'comment_manage_info', 'mblogtype', 'showFeedRepost', 'showFeedComment', 'pictureViewerSign', 'showPictureViewer', 'rcList', 'region_name', 'customIcons'
    """
    
    info_dict = {
        '发布时间': format_datetime(weibo_info['created_at']),
        '微博编号': weibo_info['id'],
        '文本内容': weibo_info['text_raw'],
        '发布终端': extract_device(weibo_info['source']),
        '转发数': weibo_info['reposts_count'],
        '评论数': weibo_info['comments_count'],
        '点赞数': weibo_info['attitudes_count'],
        '用户编号': weibo_info['user']['id'],
        '昵称': weibo_info['user']['screen_name'], 
        '发布地址': extract_location(weibo_info.get('region_name'))
    }

    if weibo_info.get('retweeted_status'):
        info_dict['转发微博编号'] = weibo_info['retweeted_status']['id']
        info_dict['转发微博文本'] = weibo_info['retweeted_status']['text_raw']
        info_dict['转发微博作者编号'] = weibo_info['retweeted_status']['user']['id']
        info_dict['转发微博作者昵称'] = weibo_info['retweeted_status']['user']['screen_name']
    
    return info_dict


def merge_dataframes_remove_duplicate_rows(dfA, dfB):
    """纵向合并两个dataframe并删除重复行

    Args:
        dfA  (pd.DataFrame): dfA
        dfB  (pd.DataFrame): dfB

    Returns:
        pd.DataFrame: 合并后的dataframe
    """
    # 找出 dfB 中与 dfA 重复的行
    duplicated_rows = dfB['微博编号'].isin(dfA['微博编号'])

    # 通过布尔索引删除 dfB 中的重复行
    dfB = dfB[~duplicated_rows]

    # 纵向合并 dfA 和 dfB
    merged_df = pd.concat([dfA, dfB], axis=0).reset_index(drop=True)

    return merged_df



def start_crawl(uid:int, Cookie:str, path:str):
    """根据微博uid获取所有转发微博数据的主函数

    Args:
        uid (int): 核心微博的uid, 在微博链接的url中可以找到
        headers (dict): 请求header, 设置User-Agent, Cookie等信息
    """
    
    # 含个人用户信息的列名，可能导致get次数过多，用户数据建议另外获取
    # repo_columns=['发布时间', '微博编号', '文本内容', '发布终端', '转发数', '评论数', '点赞数', '用户编号', '昵称', '微博数量', '关注数', '粉丝数', '个人简介', '性别', '认证原因', '是否会员', '会员等级', '微博等级','发布地址', '转发微博编号', '转发微博文本', '转发微博作者编号', '转发微博作者昵称']
    
    # 微博信息与含用户编号与名称的列名，可用于之后获取用户数据
    repo_columns=['发布时间', '微博编号', '文本内容', '发布终端', '转发数', '评论数', '点赞数', '用户编号', '昵称', '发布地址','转发微博编号', '转发微博文本', '转发微博作者编号', '转发微博作者昵称']
    
    # 参数设置
    weibo_id = uid
    filename_df = 'repo_'+str(weibo_id)+'.xlsx'
    sheet_name = '转发信息'
    page = 0
    repost_count = 0
    df = pd.DataFrame(columns=repo_columns)
    writer = pd.ExcelWriter(path+filename_df, engine='openpyxl')
    # df.to_excel(path+filename_df, index=False, encoding='utf-8-sig', engine='openpyxl')
    stop_flag = 0 # 用于判断是否连续获取到空数据，若连续获取到空数据则跳转到下一页
    
    # 设置超时时间，避免因为网络原因导致的连接失败
    socket.setdefaulttimeout(9999)
    
    # 开始抓取并记录数据
    while True:
        #  获取转发信息        
        repost_info = Get_Reposts(weibo_id, page, random.choice(Cookie))
        reposts = repost_info.get('data')
        max_page = repost_info.get('max_page')
        
        if len(reposts) == 0 and page <= max_page and stop_flag < 20:
            stop_flag += 1
            continue
        elif len(reposts) == 0 and page <= max_page and stop_flag >= 20:
            page += 1
            stop_flag = 0
            continue
        
        #  若成功获取信息，则开始解析
        if reposts == None or len(reposts) == 0:
            break
        else:
            # js.extend(reposts)
            for repost in reposts:
                
                # 获取转发微博信息
                weibo_info = Get_Weibo_Info(repost)
                
                # 获取转发用户信息，由于可能导致get次数过多，用户数据另外获取
                # user_info = Get_User_Info(repost['user']['id'], headers)
                
                # 合并微博信息与用户信息
                # combined_dict = {**weibo_info, **user_info}
                combined_dict = weibo_info
                
                # 将解析的dict格式的信息记录进dataframe
                df_repo_all_info = append_dict_to_dataframe(combined_dict, repo_columns)
                
                # 追加到总dataframe中
                # df = df._append(df_repo_all_info, ignore_index=True)
                df = merge_dataframes_remove_duplicate_rows(df, df_repo_all_info)
                
                repost_count += 1
        
        # 标记进度
        
        print('>>>Page: {}/{}, Reposts: {}'.format(page, max_page, len(df)))
        page += 1
        
        if page % 30 == 0:
            time.sleep(random.uniform(0.3, 1))  # 每30页休眠1-1.5秒，30次左右是比较容易被识别的点
        if page % 200 == 0:
            time.sleep(random.uniform(3, 5))    # 每100页休眠5-8秒
        if page % 500 == 0:
            time.sleep(random.uniform(30,50))   # 每500页休眠30-50秒
        
        if page % 1600 == 0:
            time.sleep(100)                     # 每1600页休眠100秒
            
        # sleep的时间一定要随机，否则容易被识别导致被锁IP或Cookie
        time.sleep(random.uniform(0, 0.5))
    
    # 爬取结束后保存数据
    df = df.astype(str)
    # with pd.ExcelWriter(path+filename_df,mode='a',engine='openpyxl') as writer:
    #     df.to_excel(writer, sheet_name=sheet_name, index=False)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer._save()
    writer.close()
    return df

def repo_main(uid, Cookie):
    
    
    
    # 这里输入要爬取的微博编号 
    # uid = 4890498505115219
    
    # 没什么用的格式输出
    print("=============================================================")
    print('========Crawling reposts of weibo id: {}======='.format(uid))
    print("=============================================================")
    
    # 开始爬取
    return start_crawl(uid, Cookie,path='')

