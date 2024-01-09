'''
Description: SIR模型代码
Author: Junwen Yang
Date: 2023-06-30 12:12:58
LastEditTime: 2023-12-20 18:00:04
LastEditors: Junwen Yang
'''
import networkx as nx
import numpy as np
import pandas as pd
import random

def SIR_simulation(G, initial_infected=[0], infection_rate=0.1, recovery_rate=0.1, max_iteration=100, num_simulations=1, infected_times=dict(),directed=True):
    if not directed:
        G = G.to_directed()
    final_scales = []
    avg_scales_df = pd.DataFrame()
    
    for simulation in range(num_simulations):
        S = set(G.nodes) - set(initial_infected) # S表示易感者的集合
        I = set(initial_infected) # I表示感染者的集合
        R = set() # R表示康复者的集合
        scales = []

        for iteration in range(max_iteration):
            # 更新感染者和康复者
            for infected_node in list(I):
                # 感染者有一定的概率康复
                if random.random() < recovery_rate:
                    
                    I.remove(infected_node)
                    R.add(infected_node)

                # 感染者的健康邻居有一定的概率被感染
                for neighbor in G.neighbors(infected_node):
                    if neighbor in S and random.random() < infection_rate:
                        infected_times[neighbor] += 1
                        S.remove(neighbor)
                        I.add(neighbor)

            scales.append(len(I) + len(R)) # 记录每个时间步的感染规模
            
        final_scales.append(len(I) + len(R)) # 记录最终的传播规模
        avg_scales_df = avg_scales_df._append(pd.DataFrame(scales, columns=['Scale']), ignore_index=True)

    
    
    avg_scales_df = avg_scales_df.mean(axis=0) # 计算每个时间步的感染规模的平均值
    avg_final_scale = np.mean(final_scales) # 计算平均最终传播规模

    return infected_times, avg_final_scale

def infected_nodes_list(G, seed_node,directed=True):

    # 第一个节点为初始感染节点
    infected_times = dict.fromkeys(G.nodes, 0) # 记录每个节点被感染的次数
    infected_times[seed_node] = len(G) # 初始感染节点的感染次数为节点总数
    infect_dict , avg_final_scale= SIR_simulation(G, initial_infected=[seed_node],infection_rate=0.2, recovery_rate=0.1, max_iteration=100, num_simulations=1, infected_times=infected_times,directed=directed)
    print(infect_dict)
    return infect_dict


def final_infect_scale(G, seed_nodes, infection_rate=0.2, recovery_rate=0.2, max_iteration=100, num_simulations=10,directed=True):

    infected_times = dict.fromkeys(G.nodes, 0) # 记录每个节点被感染的次数
    infect_dict , avg_final_scale= SIR_simulation(G, initial_infected=seed_nodes,infection_rate=infection_rate, recovery_rate=recovery_rate, max_iteration=max_iteration, num_simulations=num_simulations, infected_times=infected_times,directed=directed)
    print(avg_final_scale)
    return avg_final_scale