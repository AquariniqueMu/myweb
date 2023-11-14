import networkx as nx
import pandas as pd
#import voterank_plus
import math
import H_index
#import k_shell_entroph
import ECRM
# import secondMethod
from pandas import DataFrame

def h_indexs(G, nOfh_index):
    nodes = list(nx.nodes(G))
    # n = len(nodes)
    h = H_index.calcHIndexValues(G, nOfh_index)
    d = {'node':nodes,'h_index':h}
    d = DataFrame(d)
    # h_list = [(nodes[i], h[i]) for i in range(n)]  # (alt, imp): (候选元素，重要性)
    # h_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return d

def degree(g):
    """use the degree to get topk nodes
     # Arguments
         g: a graph as networkx Graph
         topk: how many nodes will be returned
     Returns
         return the topk nodes by degree, [(node1, ' '), (node2, '' ), ...]
     """
    degree_rank = nx.degree_centrality(g)
    # degree_rank = sorted(degree_rank.items(), key=lambda x: x[1], reverse=True)
    node1 = []
    score1 = []
    for node in degree_rank.keys():
        node1.append(node)
    for score in degree_rank.values():
        score1.append(score)
    d = {'node':node1,'degree':score1}
    d = DataFrame(d)
        # if len(rank1) == topk:
        #     for i in range(len(rank1)):
        #         rank1[i] = (rank1[i], ' ')
        #     return rank1
    return d

def closeness(g):
    """use the degree to get topk nodes
     # Arguments
         g: a graph as networkx Graph
         topk: how many nodes will be returned
     Returns
         return the topk nodes by degree, [(node1, ' '), (node2, '' ), ...]
     """
    closeness_rank = nx.closeness_centrality(g)
    node1 = []
    score1 = []
    for node in closeness_rank.keys():
        node1.append(node)
    for score in closeness_rank.values():
        score1.append(score)
    d = {'node':node1,'closeness':score1}
    d = DataFrame(d)
    return d

def betweenness(g):
    """use the degree to get topk nodes
     # Arguments
         g: a graph as networkx Graph
         topk: how many nodes will be returned
     Returns
         return the topk nodes by degree, [(node1, ' '), (node2, '' ), ...]
     """
    betweenness_rank = nx.betweenness_centrality(g)
    node1 = []
    score1 = []
    for node in betweenness_rank.keys():
        node1.append(node)
    for score in betweenness_rank.values():
        score1.append(score)
    d = {'node':node1,'betweenness':score1}
    d = DataFrame(d)
    return d

def constrain(g):
    """use the degree to get topk nodes
     # Arguments
         g: a graph as networkx Graph
         topk: how many nodes will be returned
     Returns
         return the topk nodes by degree, [(node1, ' '), (node2, '' ), ...]
     """
    constrain_rank = nx.constraint(g)
    node1 = []
    score1 = []
    for node in constrain_rank.keys():
        node1.append(node)
    for score in constrain_rank.values():
        score1.append(score)
    d = {'node':node1,'constrain':score1}
    d = DataFrame(d)
    return d

def kshell(G):
    """use the kshell to get topk nodes
     # Arguments
         g: a graph as networkx Graph
         topk: how many nodes will be returned
     Returns
         return the topk nodes by kshell, [(node1, ' '), (node2, ' '), ...]
     """
    node_core = nx.core_number(G)
    node1 = []
    score1 = []
    for node in node_core.keys():
        node1.append(node)
    for core in node_core.values():
        score1.append(core)
    d={'node':node1,'kshell':score1}
    d=DataFrame(d)
    return d

def CenC(G,alpha):
    '''
    :param G: network graph
    :param alpha:retard infactor
    
    return
    CenC_rank: a dict of node and node's CenC value
    '''
#    rank = []
    res_dict = {}
    #count dict
    nodes = list(nx.nodes(G))
    #计算度中心性——返回字典
    print(">>> 正在计算度值 ")
    degree_rank = nx.degree_centrality(G)
    #计算约束系数——返回字典
    print(">>> 正在计算约束系数")
    constraint_rank = nx.constraint(G)
    #计算k壳——返回字典
    print(">>> 正在计算K壳值")
    k_shell_rank = nx.core_number(G)
    
    CenC_rank = {}
    
    for node in nodes:
        sum1 = 0
        sum2 = 0
        sum3 = 0
        neighbors = list(nx.neighbors(G, node))
        nei1_li = []
        nei2_li = []
        nei3_li = []
        for nbr1 in neighbors:
            nei1_li.append(nbr1)
        for nbr1 in nei1_li:
            for SNs in list(nx.neighbors(G,nbr1)):
                nei2_li.append(SNs)
        nei2_li = list(set(nei2_li) - set(nei1_li))
        if node in nei2_li:
            nei2_li.remove(node)
        for nbr2 in nei2_li:
            for TNs in nx.neighbors(G, nbr2):
                nei3_li.append(TNs)
        nei3_li = list(set(nei3_li) - set(nei2_li) - set(nei1_li))
        if node in nei3_li:
            nei3_li.remove(node)
                      
        for nbr1 in nei1_li:
            sum1 += math.exp(degree_rank[node] * alpha) * (1/constraint_rank[node]) *  (k_shell_rank[nbr1]/ (abs(k_shell_rank[node]-k_shell_rank[nbr1])+1)) / (nx.shortest_path_length(G,node,nbr1) ** 2)          
        for nbr2 in nei2_li:
            sum2 += math.exp(degree_rank[node] * alpha) * (1/constraint_rank[node]) *  (k_shell_rank[nbr2]/ (abs(k_shell_rank[node]-k_shell_rank[nbr2])+1)) / (nx.shortest_path_length(G,node,nbr2) ** 2)
        for nbr3 in nei3_li:
            sum3 += math.exp(degree_rank[node] * alpha) * (1/constraint_rank[node]) *  (k_shell_rank[nbr3]/ (abs(k_shell_rank[node]-k_shell_rank[nbr3])+1)) / (nx.shortest_path_length(G,node,nbr3) ** 2)       
                 
        CenC_rank[node] = sum1 + sum2 + sum3
        print(">>> Calculated {}/{} nodes".format(len(CenC_rank), len(nodes)))
    return CenC_rank

def ECRM_F(G):
    g=G.copy()
    hierarchy = ECRM.ok_shell(g)  # ECRM method used
    node_core = ECRM.ECRM(G, hierarchy)
    node = []
    score = []
    for i in range(int(len(G))):
        for j in range(2):
            if j==0:
                node.append(node_core[i][j])
            else:
                score.append(node_core[i][j])
    d = {'node':node,'ECRM':score}
    d = DataFrame(d)
    return d


def centripetal_centrality(G2):
    G = G2.copy()
    G.remove_edges_from(nx.selfloop_edges(G))
    if G.number_of_nodes()>10000:
        lj = 10000
    elif G.number_of_nodes()>1000:
        lj = 1000
    else:
        lj = 100
    alpha=G.number_of_nodes()/lj    

    CenC_result = CenC(G,alpha)

    
    sorted_CenC = sorted(CenC_result.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_CenC,columns=['节点名称','向心力中心性'])
    
    # 将cenc归一化并设置为节点权重,min-max normalization
    norm_bc = {}
    for k, v in CenC_result.items():
        norm_bc[k] = (v - min(CenC_result.values())) / (max(CenC_result.values()) - min(CenC_result.values()))
    nx.write_weighted_edgelist(G, 'result_cenc.edgelist')
    df.to_excel('result_cenc.xlsx', index=False)
    print(">>> CenC计算完成")
    return df
    
    