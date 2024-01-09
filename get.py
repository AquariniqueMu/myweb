'''
Description: 
Author: Junwen Yang
Date: 2023-11-06 19:55:37
LastEditTime: 2023-12-28 16:54:21
LastEditors: Junwen Yang
'''
'''
Description: 
Author: Junwen Yang
Date: 2023-11-06 17:03:41
LastEditTime: 2023-11-12 20:08:46
LastEditors: Junwen Yang
'''
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from repost import repo_main  # 确保这个模块可用
import pandas as pd
import argparse
import networkx as nx
import math
from construct_net import construct_net_main
from DC import degree_centrality
from BC import betweenness_centrality
from CC import closeness_centrality
from SIR import infected_nodes_list,final_infect_scale
import random
import warnings
from CENC import centripetal_centrality
from emotion import emotion_calculate
warnings.filterwarnings('ignore')


app = Flask(__name__)
CORS(app)  # 允许跨域资源共享

@app.route('/')
def index():
    # 确保 search_weibo.html 文件位于 Flask 的 templates 文件夹中
    return render_template('index.html')

# 如果search_weibo.html在templates子文件夹中
@app.route('/search_weibo')
def search_weibo():
    return render_template('search_weibo.html')  # 替换'subfolder'为实际的子文件夹名

@app.route('/dissemination-network')
def dissemination_network():
    return render_template('dissemination-network.html')

@app.route('/key-spreader-analysis')
def key_spreader_analysis():
    return render_template('key-spreader-analysis.html')

@app.route('/emotionnetwork')
def emotionnetwork():
    return render_template('emotionnetwork.html')

@app.route('/sentimentspread')
def sentiment_spread():
    return render_template('sentimentspread.html')

@app.route('/sentimentanalysis')
def sentiment_analysis():
    return render_template('sentimentanalysis.html')

@app.route('/degree')
def degree():
    return render_template('degree.html')

@app.route('/edgesdata')
def edgesdata():
    return render_template('edgesdata.html')

@app.route('/nettopo')
def nettopo():
    return render_template('nettopo.html')


@app.route('/betweenness')
def betweenness():
    return render_template('betweenness.html')

@app.route('/closeness')
def closeness():
    return render_template('closeness.html')

@app.route('/top10')
def top10():
    return render_template('top10.html')

@app.route('/centripetal-title')
def centripetaltitle():
    return render_template('cenc_intro.html')


@app.route('/centripetal')
def centripetal():
    return render_template('centripetal.html')

@app.route('/centrality')
def centrality():
    return render_template('centrality.html')

@app.route('/regional-analysis')
def regional_analysis():
    return render_template('regional-analysis.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    uid = request.form['uid']
    df = get(uid)  # 调用已经提供的get函数
    # df = construct_net_main(uid)
    # 返回JSON数据
    return jsonify(df.to_dict(orient='records'))

@app.route('/download-table', methods=['POST'])
def download_table():
    # 确保文件名和路径是正确的
    uid = request.form['uid']
    return send_from_directory(directory='', filename='repo_'+str(uid)+'.xlsx', as_attachment=True,path='')


@app.route('/download_net_data', methods=['POST'])
def download_net_data():
    # 确保文件名和路径是正确的
    uid = request.form['uid']
    return send_from_directory(directory='', filename='repo_'+str(uid)+'.edgelist', as_attachment=True,path='')


@app.route('/buildnetwork', methods=['POST'])
def build_network():
    uid = request.form['uid']
    df = construct_net_main(uid)
    # 返回JSON数据
    return jsonify(df.to_dict(orient='records'))

def calculate_emotion(uid):
    df = pd.read_excel('repo_'+str(uid)+'.xlsx')
    
    df['情绪分值'] = ''
    # 增加一列情绪分值
    df['情绪分值'] = df['文本内容'].apply(emotion_calculate)
    df = df[['发布时间','微博编号','文本内容','转发数','评论数','点赞数','昵称','情绪分值']]
    
    
    df.to_excel('repo_'+str(uid)+'_emo.xlsx')
    df.to_excel('result_emo.xlsx')
    return df


@app.route('/sentimentanalysiscalc', methods=['POST'])
def sentimentanalysiscalc():
    uid = request.form['uid']
    dfemo = calculate_emotion(uid)
    # 返回JSON数据
    return dfemo.to_json(orient='records')

@app.route('/download-emo-data', methods=['POST'])
def download_emo_data():
    # 确保文件名和路径是正确的
    uid = request.form['uid']
    return send_from_directory(directory='', filename='repo_'+str(uid)+'_emo.xlsx', as_attachment=True,path='')

@app.route('/crawl-information', methods=['GET'])
def crawl_information():
    return render_template('index.html')

def get(uid):
    # 获取表单数据
    print(uid)
    
    # 这里的Cookie值应该替换为你实际使用的值
    Cookie = ['_T_WM=23905197128; XSRF-TOKEN=adbcb1; WEIBOCN_FROM=1110006030; mweibo_short_token=2a7e880bfa; SSOLoginState=1681656805; ALF=1684248805; MLOGIN=1; SCF=ApWjTkHfskwTD4Pq7psk9WtokzKE-kms6Xfvcr6f5MlojFoFjplVwA5I5AWdySiHEtiqrNkQKnRoG7f0QfP4_-s.; SUB=_2A25JOHu1DeRhGeNK4lQX8SjIzziIHXVqwwX9rDV6PUJbktAGLXDYkW1NSOnZEHiYBp31ruu-uZKGR_U3ft7j9gRJ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W58gYcZFnj-.ia.Az5L9aKu5JpX5K-hUgL.Fo-X1KqceKqXShB2dJLoIXBLxKqL1K.LB--LxK-L1h-LB-BLxKnL12eLBo.LxKBLB.eL122LxKqL1KqLB-qLxKMLBo2LBoeLxK-LBo5L1Kx9McfDMntt; M_WEIBOCN_PARAMS=luicode=20000174&uicode=20000174',
              'WEIBOCN_FROM=1110006030; loginScene=102003; geetest_token=d7338363a8117a86d245b2934fa149b7; SUB=_2A25ITyLbDeRhGeNJ61MS8CjFzj6IHXVrJToTrDV6PUJbkdAGLUnYkW1NS-fvIiBPOZC3UQgafRRtsftCfRD9BaeG; _T_WM=54616214241; MLOGIN=1; XSRF-TOKEN=6b62dc; mweibo_short_token=ba74727db8; M_WEIBOCN_PARAMS=lfid%3D231093_-_selffollowed%26luicode%3D20000174%26uicode%3D10000011%26fid%3D102803'
              ]

    # 使用repo_main处理数据并返回DataFrame
    df = repo_main(uid, Cookie)

    # 如果你想要在这里保存Excel文件，可以取消以下注释
    df.to_excel('repo_'+str(uid)+'.xlsx', index=False)
    # print(df.columns)
    df.astype(str)
    # 返回DataFrame
    return df

@app.route('/get-edgelist-data', methods=['GET'])
def get_edgelist_data():
    # 读取文件
    edges = []
    with open('result.edgelist', 'r', encoding='utf-8') as file:  # 指定编码为utf-8
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                edges.append({'source': parts[0], 'target': parts[1]})

    # 处理数据
    nodes = []
    node_set = set()
    for edge in edges:
        node_set.add(edge['source'])
        node_set.add(edge['target'])
    nodes = [{'name': node} for node in node_set]



    G = nx.read_weighted_edgelist('result.edgelist', create_using=nx.Graph())
    degrees = dict(G.degree())
    log_degrees = {node: math.log(degree + 2) for node, degree in degrees.items()}  # 加1是为了避免对0取对数
    degrees = log_degrees
    # 最大值改为第二大值+5
    max_degree = sorted(degrees.values(), reverse=True)[1] + 1
    min_degree = min(degrees.values())
    
    for node in nodes:
        node_name = node['name']
        node_degree = degrees[node_name]
        # 归一化节点度
        node['degree'] = (node_degree - min_degree) / (max_degree - min_degree) if node_degree !=  sorted(degrees.values(), reverse=True)[0] else (max_degree - min_degree) / (max_degree - min_degree) 
        node['max_degree'] = (max_degree - min_degree) / (max_degree - min_degree) 
        # 用对数减少大度值的影响
        print(node['degree'])

    # 创建JSON对象
    graph_data = {
        'nodes': nodes,
        'links': edges
    }
    return jsonify(graph_data)

@app.route('/get-edgelist-data-dc', methods=['GET'])
def get_edgelist_data_dc():
    print('get_edgelist_data_dc')   
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_dc.edgelist',  create_using=nx.DiGraph())
    dict_degree = nx.degree_centrality(G)
    # max-min归一化
    for k, v in dict_degree.items():
        dict_degree[k] = (v - min(dict_degree.values())) / (max(dict_degree.values()) - min(dict_degree.values()))
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    maxdegree = sorted(dict_degree.values(), reverse=True)[1]
    node_list = [{'name': node, 'value': dict_degree[node] * 40} if dict_degree[node] !=  sorted(dict_degree.values(), reverse=True)[0] else {'name': node, 'value': maxdegree * 40 + 10}  for node in G.nodes()]
    
    
    for node in node_list:
        node['max_degree'] = maxdegree * 40
    
    print(node_list)
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)

@app.route('/get-edgelist-data-bc', methods=['GET'])
def get_edgelist_data_bc():
    print('get_edgelist_data_bc')   
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_bc.edgelist',  create_using=nx.DiGraph())
    dict_bc = nx.betweenness_centrality(G)
    # max-min归一化
    for k, v in dict_bc.items():
        dict_bc[k] = (v - min(dict_bc.values())) / (max(dict_bc.values()) - min(dict_bc.values()))
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': dict_bc[node] * 40} for node in G.nodes()]
    # print(node_list)
    
    max_bc = sorted(dict_bc.values(), reverse=True)[0]
    min_bc = min(dict_bc.values())
    
    
    # 归一化
    for node in node_list:
        node['value'] = math.log((node['value'] - min_bc) / (max_bc - min_bc) * 9 + 1) + 1
    
    for node in node_list:
        node['max_bc'] = max_bc
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)

@app.route('/get-edgelist-data-cc', methods=['GET'])
def get_edgelist_data_cc():
    print('get_edgelist_data_bc')   
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_cc.edgelist',  create_using=nx.DiGraph())
    dict_cc = nx.closeness_centrality(G.reverse())
    # max-min归一化
    for k, v in dict_cc.items():
        dict_cc[k] = (v - min(dict_cc.values())) / (max(dict_cc.values()) - min(dict_cc.values()))
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': dict_cc[node]} for node in G.nodes()]
    # print(node_list)
    
    max_cc = sorted(dict_cc.values(), reverse=True)[0]
    
    for node in node_list: 
        node['max_cc'] = max_cc
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)


@app.route('/get-degree-data', methods=['POST'])
def get_degree_data():
    # 读取文件
    uid = request.form['uid']
    G = nx.read_weighted_edgelist('repo_{}.edgelist'.format(uid),  create_using=nx.DiGraph())
    df = degree_centrality(G)
    return jsonify(df.to_dict(orient='records'))

@app.route('/get-bc-data', methods=['POST'])
def get_bc_data():
    # 读取文件
    uid = request.form['uid']
    
    G = nx.read_weighted_edgelist('repo_{}.edgelist'.format(uid),  create_using=nx.DiGraph())
    df = betweenness_centrality(G)
    return jsonify(df.to_dict(orient='records'))

@app.route('/get-cc-data', methods=['POST'])
def get_cc_data():
    # 读取文件
    uid = request.form['uid']
    
    G = nx.read_weighted_edgelist('repo_{}.edgelist'.format(uid),  create_using=nx.DiGraph())
    df = closeness_centrality(G)
    return jsonify(df.to_dict(orient='records'))

@app.route('/get-edgelist-data-dc-top10', methods=['GET'])
def get_edgelist_data_dc_top10():
    # 获取第N高度值的节点位次
    selected_node_index = request.args.get('index')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_dc.edgelist',  create_using=nx.DiGraph())
    dc_dict = nx.degree_centrality(G)
    sorted_dc_dict = sorted(dc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    # 获取第N高度值的节点的名称
    print(selected_node_index)
    if selected_node_index != '10':
        seed_node = sorted_dc_dict[int(selected_node_index)][0]
    else:
        # 随机选择一个节点
        seed_node = random.choice(list(G.nodes()))
    
    print(seed_node)
    
    infected_nodes = infected_nodes_list(G, seed_node)
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': infected_nodes[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)
import numpy as np
@app.route('/get-edgelist-data-emo', methods=['GET'])
def get_edgelist_data_emo():
    # 获取第N高度值的节点位次
    data = pd.read_excel('result_emo.xlsx')[['昵称','情绪分值']]
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result.edgelist',  create_using=nx.DiGraph())

    emo_of_nodes = {}
    for node in G.nodes():
        emo_of_nodes[node] = data.loc[data['昵称'] == node, '情绪分值'].values[0] if len(data.loc[data['昵称'] == node, '情绪分值'].values) > 0 else 0
        print(node, emo_of_nodes[node])

    node_size = nx.degree_centrality(G)
    emo_of_edges = {}
    # 边的权重为两个节点的情绪分值的差值，目标节点减去源节点
    for edge in G.edges():
        emo_of_edges[edge] = emo_of_nodes[edge[1]] - emo_of_nodes[edge[0]]
        if emo_of_edges[edge] == np.inf:
            emo_of_edges[edge] = 1

    
    
    
    edges = [{'source': str(edge[0]), 'target': str(edge[1])} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': str(node), 'value': emo_of_nodes[node], 'Size':node_size[node]} for node in G.nodes()]
    
    
    
    print(">>> Done with node_list")
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    print(graph_data)
    print(">>> Done with graph_data")
    # print(graph_data)
    return jsonify(graph_data)


@app.route('/get-edgelist-data-bc-top10', methods=['GET'])
def get_edgelist_data_bc_top10():
    # 获取第N高度值的节点位次
    selected_node_index = request.args.get('index')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_dc.edgelist',  create_using=nx.DiGraph())
    dc_dict = nx.betweenness_centrality(G)
    sorted_dc_dict = sorted(dc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    # 获取第N高度值的节点的名称
    print(selected_node_index)
    if selected_node_index != '10':
        seed_node = sorted_dc_dict[int(selected_node_index)][0]
    else:
        # 随机选择一个节点
        seed_node = random.choice(list(G.nodes()))
    
    print(seed_node)
    
    infected_nodes = infected_nodes_list(G, seed_node)
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': infected_nodes[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)



@app.route('/get-edgelist-data-cc-top10', methods=['GET'])
def get_edgelist_data_cc_top10():
    # 获取第N高度值的节点位次
    selected_node_index = request.args.get('index')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_cc.edgelist',  create_using=nx.DiGraph())
    cc_dict = nx.closeness_centrality(G.reverse())
    
    sorted_cc_dict = sorted(cc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    # 获取第N高度值的节点的名称
    print(selected_node_index)
    if selected_node_index != '10':
        seed_node = sorted_cc_dict[int(selected_node_index)][0]
    else:
        # 随机选择一个节点
        seed_node = random.choice(list(G.nodes()))
    
    print(seed_node)
    
    infected_nodes = infected_nodes_list(G, seed_node,directed=False)
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': infected_nodes[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)


@app.route('/get-cenc-data', methods=['POST'])
def get_cenc_data():
    # 读取文件
    uid = request.form['uid']
    G = nx.read_weighted_edgelist('repo_{}.edgelist'.format(uid),  create_using=nx.Graph())
    df = centripetal_centrality(G)
    return jsonify(df.to_dict(orient='records'))

@app.route('/get-edgelist-data-cenc', methods=['GET'])
def get_edgelist_data_cenc():
    print('get_edgelist_data_dc')   
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_dc.edgelist',  create_using=nx.DiGraph())
    df = pd.read_excel('result_cenc.xlsx')
    dict_cenc = {}
    for node in G.nodes():
        dict_cenc[node] = df.loc[df['节点名称'] == node, '向心力中心性'].values[0] if len(df.loc[df['节点名称'] == node, '向心力中心性'].values) > 0 else 0
        print(node, dict_cenc[node])
    # max-min归一化
    for k, v in dict_cenc.items():
        dict_cenc[k] = (v - min(dict_cenc.values())) / (max(dict_cenc.values()) - min(dict_cenc.values())) if (max(dict_cenc.values()) - min(dict_cenc.values())) != 0 else 0
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    
    
    # 最大值改为第二大值+5
    max_cenc = sorted(dict_cenc.values(), reverse=True)[0]
    # 替换最大值
    for node in dict_cenc:
        if dict_cenc[node] == sorted(dict_cenc.values(), reverse=True)[0]:
            dict_cenc[node] = max_cenc
    
    # log_cenc = {node: math.log(cenc + 1) for node, cenc in dict_cenc.items()}  # 加1是为了避免对0取对数
    # dict_cenc = log_cenc
    
    
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': dict_cenc[node], 'max_cenc': max_cenc} for node in G.nodes()]
    
    print(node_list)
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)





@app.route('/get-edgelist-data-cenc-top10', methods=['GET'])
def get_edgelist_data_cenc_top10():
    # 获取第N高度值的节点位次
    selected_node_index = request.args.get('index')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist('result_dc.edgelist',  create_using=nx.DiGraph())
    df = pd.read_excel('result_cenc.xlsx')
    cenc_dict = {}
    for node in G.nodes():
        cenc_dict[node] = df.loc[df['节点名称'] == node, '向心力中心性'].values[0] if len(df.loc[df['节点名称'] == node, '向心力中心性'].values) > 0 else 0
        print(node, cenc_dict[node])
    sorted_cenc_dict = sorted(cenc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    # 获取第N高度值的节点的名称
    print(selected_node_index)
    if selected_node_index != '10':
        seed_node = sorted_cenc_dict[int(selected_node_index)][0]
        print(seed_node,"top10")
    else:
        # 从中心性最高的10个节点之外随机选择一个节点
        list_no_top10 = list(G.nodes())
        for i in range(10):
            list_no_top10.remove(sorted_cenc_dict[i][0])
        seed_node = random.choice(list_no_top10)
        print(seed_node,"random")
    
    # print(seed_node)
    
    infected_nodes = infected_nodes_list(G, seed_node)
    
    edges = [{'source': str(edge[0]), 'target': str(edge[1])} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': str(node), 'value': infected_nodes[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)

@app.route('/get-edgelist-data-dc-top10-2', methods=['GET'])
def get_edgelist_data_dc_top10_2():
    # 获取第N高度值的节点位次
    netname = request.args.get('networkName')
    seed_num = request.args.get('seedCount')
    print(netname, seed_num)
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist(netname + '.edgelist',  create_using=nx.Graph())

    df = degree_centrality(G)
    score_dict = {}
    for node in G.nodes():
        score_dict[node] = df.loc[df['节点名称'] == node, '度中心性'].values[0] if len(df.loc[df['节点名称'] == node, '度中心性'].values) > 0 else 0
        print(node, score_dict[node])
    sorted_score_dict = sorted(score_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    
    if_seed_node = dict.fromkeys(G.nodes(), 0)
    for key, value in sorted_score_dict[:int(seed_num)]:
        if_seed_node[key] = 1
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': if_seed_node[node]} for node in G.nodes()]
    
    print(node_list)
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)


@app.route('/get-edgelist-data-cc-top10-2', methods=['GET'])
def get_edgelist_data_cc_top10_2():
    # 获取第N高度值的节点位次
    netname = request.args.get('networkName')
    seed_num = request.args.get('seedCount')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist(netname + '.edgelist',  create_using=nx.Graph())

    df = closeness_centrality(G)
    score_dict = {}
    for node in G.nodes():
        score_dict[node] = df.loc[df['节点名称'] == node, '接近中心性'].values[0] if len(df.loc[df['节点名称'] == node, '接近中心性'].values) > 0 else 0
        print(node, score_dict[node])
    sorted_score_dict = sorted(score_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    
    if_seed_node = dict.fromkeys(G.nodes(), 0)
    for key, value in sorted_score_dict[:int(seed_num)]:
        if_seed_node[key] = 1
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': if_seed_node[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)


@app.route('/get-edgelist-data-bc-top10-2', methods=['GET'])
def get_edgelist_data_bc_top10_2():
    # 获取第N高度值的节点位次
    netname = request.args.get('networkName')
    seed_num = request.args.get('seedCount')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist(netname + '.edgelist',  create_using=nx.Graph())
    print(G.number_of_nodes())
    df = betweenness_centrality(G)
    score_dict = {}
    for node in G.nodes():
        score_dict[node] = df.loc[df['节点名称'] == node, '介数中心性'].values[0] if len(df.loc[df['节点名称'] == node, '介数中心性'].values) > 0 else 0
        print(node, score_dict[node])
    sorted_score_dict = sorted(score_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    
    if_seed_node = dict.fromkeys(G.nodes(), 0)
    for key, value in sorted_score_dict[:int(seed_num)]:
        if_seed_node[key] = 1
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': if_seed_node[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)


@app.route('/get-edgelist-data-cenc-top10-2', methods=['GET'])
def get_edgelist_data_cenc_top10_2():
    # 获取第N高度值的节点位次
    netname = request.args.get('networkName')
    seed_num = request.args.get('seedCount')
    
    # 读取文件
    edges = []
    nodes = {}
    G = nx.read_weighted_edgelist(netname + '.edgelist',  create_using=nx.Graph())

    df = centripetal_centrality(G)
    score_dict = {}
    for node in G.nodes():
        score_dict[node] = df.loc[df['节点名称'] == node, '向心力中心性'].values[0] if len(df.loc[df['节点名称'] == node, '向心力中心性'].values) > 0 else 0
        print(node, score_dict[node])
    sorted_score_dict = sorted(score_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    
    if_seed_node = dict.fromkeys(G.nodes(), 0)
    for key, value in sorted_score_dict[:int(seed_num)]:
        if_seed_node[key] = 1
    
    edges = [{'source': edge[0], 'target': edge[1]} for edge in G.edges()]
    # 生成节点数据，设置 symbolSize 为权重的20倍
    node_list = [{'name': node, 'value': if_seed_node[node]} for node in G.nodes()]
    
    
    
    
    # 创建JSON对象
    graph_data = {
        'nodes': node_list,
        'links': edges
    }
    return jsonify(graph_data)


def seed_node_select(G, seed_num, cenc_rank):
    '''
    Step 1: Calculate CenC. Calculate and rank the CenC of each node in the network according to Eq.24 Add all nodes to the seed alternative set.
    Step 2: Choose seeds. The node in the seed alternative set with the biggest CenC value is chosen as the seed and deleted from the alternative set.
    Step 3: Seed exclusion. Identify the neighbors within the third order range of the seed node in step 2 and remove them from the seed alternative set.
    Step 4: Reiterate steps 2 and 3 until the number of seed nodes that satisfy the requirement is filtered.
    Step 5: If the number of seeds from step 4 is insufficient to meet demand, the non-seeded nodes are selected with the corresponding number of nodes depending on the CenC value from largest to smallest.
    '''
    
    seed_candidate = [cenc_rank[0]]
    nodes = list(set(G.nodes()) - set(seed_candidate))
    cnt = 0
    print(seed_candidate)
    print(nodes)
    while cnt < seed_num:
        candidate = nodes[cnt]
        # 如果节点在上一个种子节点的三阶邻域内，则不作为种子节点，从nodes中删除
        last_seed = seed_candidate[cnt]
        # 获取节点的三阶邻域
        neighbors = nx.single_source_shortest_path_length(G, last_seed, cutoff=3).keys()
        if candidate in neighbors:
            nodes.remove(candidate)
        else:
            seed_candidate.append(candidate)
            cnt += 1
            
        if len(nodes) == 0 and cnt < seed_num:
            # 如果节点不够了，就从剩下的节点中选择
            rest_nodes = list(set(G.nodes()) - set(seed_candidate))
            seed_candidate += rest_nodes[:seed_num - cnt]
            break
    
    return seed_candidate

        
                
    





@app.route('/start-simulation', methods=['GET'])
def SIR_compare():
    # seed_count, network_name, infection_rate, recovery_rate
    seed_count = int(request.args.get('seed-number'))
    network_name = request.args.get('network-name')
    infection_rate = float(request.args.get('infection-rate'))
    recovery_rate = float(request.args.get('recovery-rate'))
    
    
    # 读取网络
    G = nx.read_weighted_edgelist(network_name + '.edgelist')

    # 计算中心性
    df_dc = degree_centrality(G)
    df_bc = betweenness_centrality(G)
    df_cc = closeness_centrality(G)
    df_cenc = centripetal_centrality(G)  # 假设这是您自定义的函数

    dc, bc, cc, cenc = {}, {}, {}, {}
    for node in G.nodes():
        dc[node] = df_dc.loc[df_dc['节点名称'] == node, '度中心性'].values[0]
        bc[node] = df_bc.loc[df_bc['节点名称'] == node, '介数中心性'].values[0]
        cc[node] = df_cc.loc[df_cc['节点名称'] == node, '接近中心性'].values[0]
        cenc[node] = df_cenc.loc[df_cenc['节点名称'] == node, '向心力中心性'].values[0]
    
    
    # 合并中心性分数
    node_centrality = {node: {'degree': dc[node], 'betweenness': bc[node], 
                              'closeness': cc[node], 'centripetal': cenc[node]}
                       for node in G.nodes()}

    # 生成节点排名
    dc_rank = sorted(dc, key=dc.get, reverse=True)
    bc_rank = sorted(bc, key=bc.get, reverse=True)
    cc_rank = sorted(cc, key=cc.get, reverse=True)
    cenc_rank = sorted(cenc, key=cenc.get, reverse=True)
    cenc_rank = seed_node_select(G, seed_count, cenc_rank)

    # 模拟SIR传播
    dc_result = final_infect_scale(G, dc_rank[:seed_count], infection_rate, recovery_rate)
    bc_result = final_infect_scale(G, bc_rank[:seed_count], infection_rate, recovery_rate)
    cc_result = final_infect_scale(G, cc_rank[:seed_count], infection_rate, recovery_rate)
    cenc_result = final_infect_scale(G, cenc_rank, infection_rate, recovery_rate)

    res = {
        '度中心性': dc_result,
        '介数中心性': bc_result,
        '接近中心性': cc_result,
        '向心力中心性': cenc_result
    }

    print(res)
    return res




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)



