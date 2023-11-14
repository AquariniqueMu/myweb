/*
 * @Description: 
 * @Author: Junwen Yang
 * @Date: 2023-11-07 04:27:04
 * @LastEditTime: 2023-11-13 16:55:59
 * @LastEditors: Junwen Yang
 */
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
    
    document.getElementById('emo-simulate-btn').addEventListener('click', function() {
        
        var chart = initChart();
        fetch('get-edgelist-data-emo')
            .then(response => response.json())
            .then(graph_data => {
                // 打印一句话
                // 找出最大权重
                var maxWeight = Math.max(...graph_data.nodes.map(node => node.value));
                // 找出具有最大symbolSize属性的前10个节点
                var top10Nodes = graph_data.nodes.sort((a, b) => b.Size - a.Size).slice(0, 10);
                // 为每个节点设置颜色
                graph_data.nodes.forEach(node => {
                    node.label = {
                        normal: {
                            show: top10Nodes.includes(node) ? true : false,
                            color: '#000000',
                            formatter: node.name,
                            fontSize: 14
                        }
                    };
                    node.itemStyle = {
                        normal: {
                            symbolSize: 48,
                            // 按照权重大小从绿色到红色渐变,最大权重为绿色，最小权重为红色，如果权重为0，则为灰色
                            color: node.value === 0 ? '#cccccc' : `rgb(${255 - Math.round(node.value / maxWeight * 255)}, 150, 220)`
                        }
                    };
            
                });
                
                
                var option = {
                    series: [{
                        type: 'graph',
                        layout: 'force',
                        data: graph_data.nodes,
                        links: graph_data.links,
                        layout: 'force',
                        focusNodeAdjacency: true,
                        symbolSize: 18,
                        draggable: true,
                        
                        roam: true,
                        force: {
                            repulsion: 1000
                        }
                    
                        // ...其他选项
                    }]
                };
                chart.setOption(option);
            })
            .catch(error => console.error('Error:', error));
    });


    function fetchGraphData() {
        var chart = initChart();
        fetch('get-edgelist-data-emo')
            .then(response => response.json())
            .then(graph_data => {
                // 打印一句话
                // 找出最大权重
                var maxWeight = Math.max(...graph_data.nodes.map(node => node.value));
                // 找出具有最大symbolSize属性的前10个节点
                var top10Nodes = graph_data.nodes.sort((a, b) => b.Size - a.Size).slice(0, 10);
                // 为每个节点设置颜色
                graph_data.nodes.forEach(node => {
                    node.label = {
                        normal: {
                            show: top10Nodes.includes(node) ? true : false,
                            color: '#000000',
                            formatter: node.name,
                            fontSize: 10
                        }
                    };
                    node.itemStyle = {
                        normal: {
                            symbolSize: 16,
                            // 按照权重大小从绿色到红色渐变,最大权重为绿色，最小权重为红色，如果权重为0，则为灰色
                            color: node.value === 0 ? '#cccccc' : `rgb(${255 - Math.round(node.value / maxWeight * 255)}, 150, 220)`
                        }
                    };
            
                });
                
                
                var option = {
                    series: [{
                        type: 'graph',
                        layout: 'force',
                        data: graph_data.nodes,
                        links: graph_data.links,
                        layout: 'force',
                        
                        symbolSize: 16,
                        draggable: true,
                        
                        roam: true,
                        force: {
                            repulsion: 1000
                        }
                    
                        // ...其他选项
                    }]
                };
                var myChart = initChart();
                chart.setOption(option);
            })
            .catch(error => console.error('Error:', error));
    }



});
