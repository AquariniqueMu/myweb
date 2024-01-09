/*
 * @Description: 
 * @Author: Junwen Yang
 * @Date: 2023-11-14 03:39:45
 * @LastEditTime: 2023-12-28 12:30:07
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
function fetchProgress() {
    fetch('/progress')
    .then(response => response.json())
    .then(data => {
        updateProgressBar(data.progress);
        if (data.progress < 100) {
            setTimeout(fetchProgress, 1000); // 每秒查询一次
        }
    });
}

function updateProgressBar(percentage) {
    var progressBar = document.getElementById('progress-bar');
    var percentageDisplay = document.getElementById('progress-bar-percentage');
    progressBar.style.width = percentage + '%';
    percentageDisplay.textContent = percentage + '%';

}
function startRandomProgress() {
    progressInterval = setInterval(() => {
        let progressBar = document.getElementById('progress-bar');
        let currentWidth = parseFloat(progressBar.style.width);
        if (currentWidth < 99) { // 限制随机增长到90%，以避免超过100%
            // 随机增加1-10%,数字保留整数
            let randomIncrease = Math.floor(Math.random(1, 10) * 2);
            
            updateProgressBar(Math.min(currentWidth + randomIncrease, 99));
        }
    }, 1000); // 每1秒随机增加进度
}
function stopRandomProgress() {
    clearInterval(progressInterval);
}
var ifsavedlayout = false;

document.addEventListener('DOMContentLoaded', function() {
    // 初始化每个图表

    var sirChart = echarts.init(document.getElementById('sir-chart-container'));

    var dcChart = echarts.init(document.getElementById('dc-chart'));
    var bcChart = echarts.init(document.getElementById('bc-chart'));
    var ccChart = echarts.init(document.getElementById('cc-chart'));
    var cencChart = echarts.init(document.getElementById('cenc-chart'));
    var seedCount = document.getElementById('seed-number').value;
    var infectionRate = document.getElementById('infection-rate').value;
    var recoveryRate = document.getElementById('recovery-rate').value;
    

    

    
    
    
    


    // 设置按钮事件监听器
    document.getElementById('dc-btn').addEventListener('click', function() {
        var weiboid = document.getElementById('search-input').value;
    
        var networkName = document.getElementById('network-name').value;
        if (networkName == 'weibo') {
            networkName = 'repo_' + weiboid;
        }
        var dc_url = 'get-edgelist-data-dc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
        fetchGraphDataForChart(dcChart, dc_url);
    });
    document.getElementById('bc-btn').addEventListener('click', function() {

        var weiboid = document.getElementById('search-input').value;
    
        var networkName = document.getElementById('network-name').value;
        if (networkName == 'weibo') {
            networkName = 'repo_' + weiboid;
        }
        var bc_url = 'get-edgelist-data-bc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
        fetchGraphDataForChart(bcChart, bc_url);
    });
    document.getElementById('cc-btn').addEventListener('click', function() {



        var weiboid = document.getElementById('search-input').value;
    
        var networkName = document.getElementById('network-name').value;
        if (networkName == 'weibo') {
            networkName = 'repo_' + weiboid;
        }
        var cc_url = 'get-edgelist-data-cc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
        fetchGraphDataForChart(ccChart, cc_url);
    });
    document.getElementById('cenc-btn').addEventListener('click', function() {


        var weiboid = document.getElementById('search-input').value;
    
        var networkName = document.getElementById('network-name').value;
        if (networkName == 'weibo') {
            networkName = 'repo_' + weiboid;
        }
        var cenc_url = 'get-edgelist-data-cenc-top10-2?seedCount=' + seedCount + '&networkName=' + networkName + '&infectionRate=' + infectionRate + '&recoveryRate=' + recoveryRate;
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
            var top10 = graph_data.nodes.sort((a, b) => b.value - a.value).slice(0, 10);
            // 为每个节点设置样式，前十的节点标红，其他节点标蓝
            graph_data.nodes.forEach(node => {
                var isTop10 = top10.includes(node);
                var nodeColor = isTop10 ? '#CD5C5C' : '#6495ED'

                node.symbolSize = top10.includes(node) ? 20 : 10;
                node.label = {
                    normal: {
                        show: top_1.includes(node) ? true : false,
                        // symbolSize: 12,
                        color: 'black',
                        // 字体大小
                        fontSize: 10,
                        formatter: node.name
                    }
                };
                node.itemStyle = {
                    normal: {
                        color: nodeColor,
                            borderWidth: 0.5,
                            borderColor: '#FFF',
                            shadowBlur: 5,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                };
            });

            // 设置边的属性
            graph_data.links.forEach(link => {
                var targetColor = graph_data.nodes.find(node => node.name === link.target).itemStyle.normal.color;
                link.lineStyle = {
                    normal: {
                        width: 0.3,
                        color: targetColor,
                        curveness: 0
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
                    
                    draggable: false,
                    roam: true,
                    
                    force: {
                        repulsion: 1000,
                        layoutAnimation: false,
                        // edgeLength: 800
                        // gravity: 0.8
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
        var weiboid = document.getElementById('search-input').value;
        var progressBar = document.getElementById('progress-bar');
        progressBar.style.width = '0%'; // 重置进度条为0
        updateProgressBar(0); // 初始化进度条为0%
        startRandomProgress();
        fetchProgress(); // 启动进度条的更新
        if (networkName === 'weibo') {
            networkName = 'repo_' + weiboid;
        }

        

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
            updateProgressBar(100);
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('network-name').addEventListener('change', function() {
    var selectedNetwork = this.value;
    var weiboInputContainer = document.getElementById('weibo-input-container');
    if (selectedNetwork === 'weibo') {
        weiboInputContainer.style.display = 'block';
    } else {
        weiboInputContainer.style.display = 'none';
    }
});


});