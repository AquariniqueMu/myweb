import networkx as nx
import pandas as pd

def betweenness_centrality(G):
    print('betweenness__centrality')
    print(G.number_of_nodes())
    bc_dict = nx.betweenness_centrality(G)
    print(bc_dict)
    sorted_bc = sorted(bc_dict.items(), key=lambda x: x[1], reverse=True)
    
    bc_df = pd.DataFrame(sorted_bc, columns=['节点名称', '介数中心性'])
    
    # 将bc归一化并设置为节点权重,yong min-max normalization
    norm_bc = {}
    for k, v in bc_dict.items():
        norm_bc[k] = (v - min(bc_dict.values())) / (max(bc_dict.values()) - min(bc_dict.values()))
    nx.write_weighted_edgelist(G, 'result_bc.edgelist')
    bc_df.to_excel('result_bc.xlsx', index=False)
    print(bc_df)
    return bc_df