import networkx as nx
import pandas as pd

def degree_centrality(G):
    print('degree_centrality')
    
    print(G.number_of_nodes())
    dc_dict = nx.degree_centrality(G)
    print(dc_dict)
    sorted_dc = sorted(dc_dict.items(), key=lambda x: x[1], reverse=True)
    
    dc_df = pd.DataFrame(sorted_dc, columns=['节点名称', '度中心性'])
    
    # 将DC归一化并设置为节点权重
    norm_dc = {}
    for k, v in dc_dict.items():
        norm_dc[k] = v / (G.number_of_nodes() - 1)
    
    nx.write_weighted_edgelist(G, 'result_dc.edgelist')
    dc_df.to_excel('result_dc.xlsx', index=False)
    print(dc_df)
    return dc_df