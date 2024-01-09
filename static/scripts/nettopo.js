/*
 * @Description: 
 * @Author: Junwen Yang
 * @Date: 2023-11-07 04:27:04
 * @LastEditTime: 2023-12-28 04:00:18
 * @LastEditors: Junwen Yang
 */
function degreeToColor(degree, maxDegree) {
    // 设定最大和最小色调值，红色和天蓝色
    var minHue = -180; // 天蓝色
    var maxHue = 0;   // 红色

    

    // 计算当前度的色调
    var hue = minHue + (maxHue - minHue) * (degree / maxDegree);

    return `hsl(${hue}, 100%, 40%)`;
}
function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var menuIcon = document.querySelector('.menu-icon');
    if (sidebar.style.left === '-250px') {
        sidebar.style.left = '0px'; // Show the sidebar
        menuIcon.classList.remove('open'); // Move the menu icon to the right
    } else {
        sidebar.style.left = '-250px'; // Hide the sidebar
        menuIcon.classList.add('open'); // Move the menu icon back to the left
    }
}
document.addEventListener('DOMContentLoaded', function() {

    var mainContainer = document.getElementById('main');
    
    function initChart() {
        // 销毁旧的图表实例
        if (echarts.getInstanceByDom(mainContainer)) {
            echarts.dispose(mainContainer);
        }
        // 创建新的图表实例
        return echarts.init(mainContainer);
    }
    
    // var chart = echarts.init(document.getElementById('main'));
    
    document.getElementById('no-weight-btn').addEventListener('click', function() {
        
        fetchGraphData(false);  // 无权重
    });

    document.getElementById('with-weight-btn').addEventListener('click', function() {
        fetchGraphData(true);  // 带权重
    });

    function fetchGraphData(withWeight) {
        var chart = initChart();
        
        fetch('get-edgelist-data')
            .then(response => response.json())
            .then(graph_data => {
                // 设置节点的属性
                
                var nodeColors = {}; // 存储每个节点的颜色
                var nodedegree = {};
                graph_data.nodes.forEach(node => {
                    // 根据节点的度设置符号大小和颜色
                    node.symbolSize = 20 + 20 * (node.degree / node.max_degree); // 根据需求调整大小范围
                    var color = degreeToColor(node.degree, node.max_degree);
                    node.itemStyle = {
                        normal: {
                            color: color,
                            borderWidth: 0.3, // 设置边框宽度
                            borderColor: 'black', // 设置边框颜色
                            shadowBlur: 5, // 设置阴影模糊大小
                            shadowColor: 'rgba(0, 0, 0, 0.5)' // 设置阴影颜色
                        },
                        emphasis: {
                            color: '#B22222' // 强调时的颜色
                        }
                    };
                    
                    node.label = {
                        normal: {
                            show: false,
                            color: '#FFFFFF',
                            fontSize: 12,
                            formatter: node.name
                        }
                    };
                    nodeColors[node.name] = color; // 将颜色存储在 nodeColors 对象中
                    nodedegree[node.name] = node.degree;
                });
                graph_data.links.forEach(link => {
                    // 示例：根据边的某个属性（如权重）来设置粗细和颜色
                    // 这里需要根据您的数据结构进行相应调整
                    // var weight = link.weight || 1; // 假设有权重属性
                    // var thickness = Math.max(1, weight * 2); // 粗细按权重调整
                    // var color = weight > 5 ? '#FF0000' : '#999999'; // 权重大于5时为红色，否则为灰色
                    var targetColor = nodeColors[link.source];
                    var targetdegree = nodedegree[link.target];
                    link.lineStyle = {
                        normal: {
                            width: 0.6 + 5 * targetdegree, // 根据需求调整大小范围
                            color: targetColor,
                            curveness: 0.2
                        }
                    };
                });
                // 设置图表选项
                var option = {
                    title: {
                        text: '网络拓扑图'
                    },
                    series: [{
                        type: 'graph',
                        layout: 'force',
                        data: graph_data.nodes,
                        links: graph_data.links,
                        draggable: false,
                        focusNodeAdjacency: true,
                        roam: true,
                        force: {
                            repulsion: 500,
                            edgeLength: 500,
                            gravity: 0.1,
                            layoutAnimation: false
                        }
                    }]
                };
    
                // 应用图表选项
                chart.setOption(option);
            })
            .catch(error => console.error('Error:', error));
    }
    



});
