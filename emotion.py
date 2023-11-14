'''
Description: 
Author: Junwen Yang
Date: 2023-11-13 03:22:24
LastEditTime: 2023-11-13 04:20:41
LastEditors: Junwen Yang
'''
from cnsenti import Emotion
from cnsenti import Sentiment
import pandas as pd


def emotion_calculate(text):
    print(">>> Analyzing emotion of the text {}".format(text[:10]))
    senti = Sentiment()
    result = senti.sentiment_calculate(text)
    pos = result['pos']
    neg = result['neg']
    if pos > neg:
        return (pos - neg) / pos
    elif pos < neg:
        return - (neg - pos) / neg
    else:
        return 0
    
    
# df = pd.read_excel('repo_4966963325963766.xlsx')
# df = df[['发布时间','微博编号','文本内容','转发数','评论数','点赞数','昵称']]
# # df.to_excel('repo_4966963325963766.xlsx', index=False, encoding='utf-8')
# # 增加一列情绪分值
# df['情绪分值'] = df['文本内容'].apply(emotion_calculate)
# print(df)