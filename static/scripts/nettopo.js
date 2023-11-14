/*
 * @Description: 
 * @Author: Junwen Yang
 * @Date: 2023-11-07 04:27:04
 * @LastEditTime: 2023-11-14 08:44:46
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
                if (withWeight) {
                    // 找出最大权重
                    var maxWeight = Math.max(...graph_data.nodes.map(node => node.value));
                    // 为每个节点设置颜色
                    graph_data.nodes.forEach(node => {
                        node.label = {
                            normal: {
                                show: true,
                                color: '#000000',
                                formatter: node.name
                            }
                        };
                        node.itemStyle = {
                            normal: {
                                color: getWeightColor(node.value, maxWeight)
                            }
                        };
                    });
                }
                // 其他设置不变，直接使用 graph_data 生成图表
                graph_data.nodes.forEach(node => {
                    node.label = {
                        normal: {
                            show: false,
                            color: '#000000',
                            
                            // 字体大小
                            fontSize: 12,
                            formatter: node.name
                        }
                    };
                    node.itemStyle = {
                        normal: {
                            color: getWeightColor(node.value, maxWeight)
                        }
                    };
                });
                var option = {
                    title: {
                        text: '网络拓扑图'
                    },
                    series: [{
                        type: 'graph',
                        layout: 'force',
                        data: graph_data.nodes,
                        links: graph_data.links,
                        layout: 'force',
                        symbolSize: 24,
                        draggable: true,
                        focusNodeAdjacency: true,
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
    }
    
    function getWeightColor(weight, maxWeight) {
        // 假设weight为节点权重，maxWeight为所有节点中的最大权重
        var intensity = weight / maxWeight;
        var color = echarts.color.lerp(intensity, ['#FFFFFF', '#FF0000']); // 从白色到红色的渐变
        return color;
    }
    fetch('/get-edgelist-data')
    .then(response => response.json())
    .then(graph_data => {
        // 找出最大权重
        var maxWeight = Math.max(...graph_data.nodes.map(node => node.value));
        
        // 为每个节点设置颜色
        graph_data.nodes.forEach(node => {
            node.label = {
                normal: {
                    show: false,
                    color: '#000000',
                    formatter: node.name
                }
            };
            node.itemStyle = {
                normal: {
                    color: getWeightColor(node.value, maxWeight)
                }
            };
        });

        var option = {
            series: [{
                type: 'graph',
                layout: 'force',
                symbolSize: 24,
                draggable: true,
                roam: true,
                force: {
                    repulsion: 1000
                },
                
                // ...其他选项
                data: graph_data.nodes,
                links: graph_data.links,
                // ...其他选项
            }]
        };

        chart.setOption(option);
    })
    .catch(error => console.error('Error:', error));




});
