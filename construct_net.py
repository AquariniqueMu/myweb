'''
Description: 
Author: Junwen Yang
Date: 2023-04-22 00:09:29
LastEditTime: 2023-12-20 17:59:17
LastEditors: Junwen Yang
'''
import networkx as nx
import pandas as pd
import numpy as np
import re
# from alive_progress import alive_bar

def extract_user_comments(text: str, name:str) -> dict:
    
    if type(text) == float:
        return {name: ''}
    
    
    
    user_comments = {}
    main_user_comment = text.split("//@", 1)[0].strip()
    user_comments[name] = main_user_comment
    
    # 将文本中的全角冒号转换为半角冒号
    text = text.replace('：', ':')
    text = text.replace(' ://@', '://@')
    text = text.replace(' //@', '://@')
    pattern = r'(?<=//@[^:])//@'
    text = re.sub(pattern, r'://@', text)
    # print(text)
    
    pattern = r'//@([^:]+):([\s\S]*?)(?=//@|$)'

    
    for match in re.finditer(pattern, text):
        username = match.group(1)
        username = username.strip()
        comment = match.group(2).strip()
        user_comments[username] = comment
    
    return user_comments


def construct_graph(link_relation: dict,source_node:dict,if_directed:bool=True, data:pd.DataFrame=pd.DataFrame) -> nx.Graph:
    if if_directed:
        G = nx.DiGraph()
    else: 
        G = nx.Graph()

    data_cols = [ '微博ID', '文本内容', '发布终端', '转发数', '评论数', '点赞数', '用户ID', '昵称', '发布IP','转发微博ID', '转发微博文本', '转发微博作者ID', '转发微博作者昵称']
    

    # source_cols = ['微博ID', '微博内容', '转发数', '评论数', '点赞数', '发布地区', '发布终端', '用户id', '用户昵称', '微博数量', '关注数量', '粉丝数量', '个人简介', '性别', '认证理由', '是否会员', '会员等级', '微博等级']

    
    G.add_node(source_node['name'], text=source_node['text'])
    # for col in source_cols:
    #     G.nodes[source_node['name']][col] = source_data[source_data['用户昵称'] == source_node['name']][col]
    for user, comments in link_relation.items():
        for comment_user, comment in comments.items():
            if G.has_node(comment_user):
                continue
            else:
                G.add_node(comment_user, text=comment)
                # 给节点添加属性
                # for col in data_cols:
                    # G.nodes[comment_user][col] = data[data['昵称'] == comment_user][col].values[0] if len(data[data['昵称'] == comment_user][col].values) else ''
    
    
    
    # 给所有节点添加dataframe中对应的属性
    # for node in G.nodes:
    #     for col in data_cols:
    #         G.nodes[node][col] = data[data['昵称'] == node][col].values[0] if len(data[data['昵称'] == node][col].values) else ''
            
    # 打印网络的节点属性
    # print(G.nodes.data())
    
    for user, comments in link_relation.items():

        if not G.has_edge(source_node['name'], list(comments.keys())[-1]):
            G.add_edge(source_node['name'], list(comments.keys())[-1])
        
        if len(list(comments.keys())) == 1:
            if G.has_edge(source_node['name'], user):
                continue
            else:
                G.add_edge(source_node['name'], user)
        
        else:
            # 将所有的用户按照key的顺序依次相连
            for i in range(len(comments)-1):
                user1 = list(comments.keys())[i]
                user2 = list(comments.keys())[i+1]
                if G.has_edge(user2, user1):
                    continue
                else:
                    G.add_edge(user2, user1)
    return G


def construct_net_main(id,read_path: str = '', save_path: str = '',source_node_data:pd.DataFrame=pd.DataFrame):
    print("eqiwoeuioqwueioqwueiquwoeuqwi")
    # id = 4890498505115219
    
    data = pd.read_excel(read_path+'repo_{}.xlsx'.format(id), index_col=0, engine='openpyxl', sheet_name='Sheet1')
    if data.empty:
        return None
    link_relation = {}
    
    
    for index, row in data.iterrows():
        user_comments = extract_user_comments(row['文本内容'], row['昵称'])
        link_relation[row['昵称']] = user_comments
        
        # print(user_comments)
        # print('-----------------')
    
    source_node = {
        'name': data['转发微博作者昵称'][0],
        'text': data['转发微博文本'][0],
    }
    # print(data.columns)
    G = construct_graph(link_relation,source_node=source_node,if_directed=True,data=data)

    # 保存节点度信息, 用于检查连边是否正确
    df_name_degree = pd.DataFrame(dict(G.in_degree()).items(), columns=['name', 'degree'])
    df_name_degree.sort_values(by='degree', ascending=False, inplace=True)
    df_name_degree.to_excel(save_path+'repo_{}_degree.xlsx'.format(id), index=False)
    
    # 将G的连边保存到dataframe中，第一列为源节点，第二列为目标节点
    df = pd.DataFrame(columns=['源节点', '目标节点'])
    for edge in G.edges:
        df = df._append({'源节点': edge[0], '目标节点': edge[1]}, ignore_index=True)
    
    print(df)
    
    # 在edgelist中保存网络的文本信息
    nx.write_edgelist(G, save_path+'repo_{}.edgelist'.format(id), data=False)
    nx.write_edgelist(G, save_path+'result.edgelist', data=False)
    
    # 在gexf中保存网络的文本信息
    nx.write_gexf(G, save_path+'repo_{}.gexf'.format(id), encoding='utf-8', version='1.2draft')
    
    # nx.write_gpickle(G, save_path+'repo_{}.gpickle'.format(id), protocol=4, fix_imports=True)
    
    # nx.write_edgelist(G, save_path+'repo_{}.txt'.format(id), data=False)    
    # print(G)
    # txt_edge_list = nx.generate_edgelist(G, data=False)
    # txt_edge_list = '\n'.join(txt_edge_list)
    # df = pd.DataFrame(columns=['Source', 'Target'])
    # for line in txt_edge_list.split('\n'):
    #     source, target = line.split(' ')
    #     df.append({'Source': source, 'Target': target}, ignore_index=True)
    return df
    
    
    
# if __name__ == '__main__':
#     construct_net_main(4890498505115219)