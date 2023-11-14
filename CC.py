'''
Description: 
Author: Junwen Yang
Date: 2023-11-12 20:09:15
LastEditTime: 2023-11-14 05:49:38
LastEditors: Junwen Yang
'''
import networkx as nx
import pandas as pd

def closeness_centrality(G):
    print('closeness__centrality')
    print(G.number_of_nodes())
    cc_dict = nx.closeness_centrality(G.reverse()) if nx.is_directed(G) else nx.closeness_centrality(G)
    print(cc_dict)
    sorted_bc = sorted(cc_dict.items(), key=lambda x: x[1], reverse=True)
    
    cc_df = pd.DataFrame(sorted_bc, columns=['节点名称', '接近中心性'])
    
    # 将bc归一化并设置为节点权重,min-max normalization
    norm_bc = {}
    for k, v in cc_dict.items():
        norm_bc[k] = (v - min(cc_dict.values())) / (max(cc_dict.values()) - min(cc_dict.values()))
    nx.write_weighted_edgelist(G, 'result_cc.edgelist')
    cc_df.to_excel('result_cc.xlsx', index=False)
    print(cc_df)
    return cc_df