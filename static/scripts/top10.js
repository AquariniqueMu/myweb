/*
 * @Description: 
 * @Author: Junwen Yang
 * @Date: 2023-11-14 03:39:45
 * @LastEditTime: 2023-11-14 07:16:57
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
    // 初始化每个图表

    var sirChart = echarts.init(document.getElementById('sir-chart-container'));

    var dcChart = echarts.init(document.getElementById('dc-chart'));
    var bcChart = echarts.init(document.getElementById('bc-chart'));
    var ccChart = echarts.init(document.getElementById('cc-chart'));
    var cencChart = echarts.init(document.getElementById('cenc-chart'));
    var seedCount = document.getElementById('seed-number').value;
    var networkName = document.getElementById('network-name').value;
    var infectionRate = document.getElementById('infection-rate').value;
    var recoveryRate = document.getElementById('recovery-rate').value;

    var dc_url = 'get-edgelist-data-dc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
    var bc_url = 'get-edgelist-data-bc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
    var cc_url = 'get-edgelist-data-cc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
    var cenc_url = 'get-edgelist-data-cenc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;


    // 设置按钮事件监听器
    document.getElementById('dc-btn').addEventListener('click', function() {
        fetchGraphDataForChart(dcChart, dc_url);
    });
    document.getElementById('bc-btn').addEventListener('click', function() {
        fetchGraphDataForChart(bcChart, bc_url);
    });
    document.getElementById('cc-btn').addEventListener('click', function() {
        fetchGraphDataForChart(ccChart, cc_url);
    });
    document.getElementById('cenc-btn').addEventListener('click', function() {
        fetchGraphDataForChart(cencChart, cenc_url);
    });

    // 定义加载并显示图表数据的函数
    function fetchGraphDataForChart(chart, url) {
        fetch(url)
        .then(response => response.json())
        .then(graph_data => {
            console.log(graph_data);
            // 找出value值为1的节点
            var top_1 = graph_data.nodes.filter(node => node.value == 1);
            // 为每个节点设置样式，前十的节点标红，其他节点标蓝
            graph_data.nodes.forEach(node => {
                node.label = {
                    normal: {
                        show: top_1.includes(node) ? true : false,
                        // symbolSize: 12,
                        color: '#000000',
                        // 字体大小
                        fontSize: 8,
                        formatter: node.name
                    }
                };
                node.itemStyle = {
                    normal: {
                        color: top_1.includes(node) ? '#FF0000' : '#0000FF',
                        symbolSize:top_1.includes(node) ? 36 : 12
                    }
                };
            });
            var option1 = {
                series: [{
                    type: 'graph',
                    layout: 'force',
                    data: graph_data.nodes,
                    links: graph_data.links,
                    // symbolSize: top10.includes(node) ? 24 : 12,
                    // 对top10节点设置更大的symbolSize
                    // symbolSize: 12,
                    
                    draggable: true,
                    roam: true,
                    
                    force: {
                        repulsion: 1000
                    },
                    label: {
                        normal: {
                            show: true,
                            
                            textStyle: {
                                color: '#333'
                                
                            }
                        }
                    }
                }]
            };
            
            

       
            chart.setOption(option1);
        })
        .catch(error => console.error('Error:', error));
    }

    

    document.getElementById('start-simulation').addEventListener('click', function() {
        var seedCount = document.getElementById('seed-number').value;
        var networkName = document.getElementById('network-name').value;
        var infectionRate = document.getElementById('infection-rate').value;
        var recoveryRate = document.getElementById('recovery-rate').value;

        var url = `/start-simulation?seed-number=${seedCount}&network-name=${networkName}&infection-rate=${infectionRate}&recovery-rate=${recoveryRate}`;

        fetch(url)
        .then(response => response.json())
        .then(data => {
            var option = {
                backgroundColor: '#f4f4f4', // 背景颜色
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: ['度中心性', '介数中心性', '接近中心性', '向心力中心性'],
                    axisLabel: {
                        fontSize: 18,
                        fontWeight: 'bold'
                    }
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        fontSize: 18
                    }
                },
                series: [{
                    data: [
                        {value: data['度中心性'], itemStyle: {color: 'rgba(135,206,235, 0.7)'},name:'度中心性'},
                        {value: data['介数中心性'], itemStyle: {color: 'rgba(100,149,237, 0.7)'},name:'介数中心性'},
                        {value: data['接近中心性'], itemStyle: {color: 'rgba(30,144,255, 0.7)'},name:'接近中心性'},
                        {value: data['向心力中心性'], itemStyle: {color: 'rgba(128,0,0, 0.7)'},name:'向心力中心性'}
                    ],
                    type: 'bar',
                    barWidth: '25%',
                    label: {
                        show: true,
                        position: 'top',
                        fontSize: 18,
                        fontWeight: 'bold'
                    }
                }],
                legend: {
                    data: ['度中心性', '介数中心性', '接近中心性', '向心力中心性'],
                    align: 'top'
                },
            };
            sirChart.setOption(option);
        })
        .catch(error => console.error('Error:', error));
});




});
