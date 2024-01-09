

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
        if (currentWidth < 90) { // 限制随机增长到90%，以避免超过100%
            // 随机增加1-10%,数字保留整数
            let randomIncrease = Math.floor(Math.random(1, 10) * 5);
            
            updateProgressBar(Math.min(currentWidth + randomIncrease, 99));
        }
    }, 1000); // 每1秒随机增加进度
}
function stopRandomProgress() {
    clearInterval(progressInterval);
}
document.addEventListener('DOMContentLoaded', function() {
    var mainContainer = document.getElementById('main');
    var mainContainer2 = document.getElementById('main2');
    
    var chart;

    // 初始化图表
    function initChart() {
        if (chart) {
            chart.dispose();
        }
        chart = echarts.init(mainContainer);
        return chart;
    }

    // 初始化图表
    function initChart2() {
        if (chart) {
            chart.dispose();
        }
        chart = echarts.init(mainContainer2);
        return chart;
    }


    // 创建表格
    function createTable(data) {
        var container = document.getElementById('table-container-cenc');
        container.innerHTML = '';
        var table = document.createElement('table');
        table.className = 'table';
      
        var thead = document.createElement('thead');
        var headerRow = document.createElement('tr');
        var headers = ['节点名称','向心力中心性'];
        headers.forEach(function(header) {
            var th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
      
        var tbody = document.createElement('tbody');
        data.forEach(function(row) {
            var tr = document.createElement('tr');
            headers.forEach(function(header) {
                var td = document.createElement('td');
                // 如果是前十行且是第一个单元格（节点名称），则标红
                if (data.indexOf(row) < 10 && headers.indexOf(header) == 0) {
                    td.style.color = '#FF0000';
                }
                td.textContent = row[header.toLowerCase()]; 
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        container.appendChild(table);
    }

    // 获取图表数据并生成图表
    function fetchGraphData(withWeight) {
        fetch('get-edgelist-data-cenc')
            .then(response => response.json())
            .then(graph_data => {
               
                // 找出value值前十的节点
                var top10 = graph_data.nodes.sort((a, b) => b.value - a.value).slice(0, 10);
                // 为每个节点设置样式，前十的节点标红，其他节点标蓝
                graph_data.nodes.forEach(node => {
                    var isTop10 = top10.includes(node);
                    var nodeColor = isTop10 ? '#CD5C5C' : '#6495ED'
                    node.symbolSize = 10 + 30 * (node.value ); // 根据度值调整大小
                    node.label = {
                        normal: {
                            show: top10.includes(node) ? true : false,
                            // symbolSize: 12,
                            color: '#000000',
                            // 字体大小
                            fontSize: 16,
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
                            curveness: 0.3
                        }
                    };
                });
                var option1 = {
                    series: [{
                        type: 'graph',
                        layout: 'force',
                        data: graph_data.nodes,
                        links: graph_data.links,
                        focusNodeAdjacency: true,
                        draggable: false,
                        roam: true,
                        force: {
                            repulsion: 500,
                            edgeLength: 500,
                            gravity: 0.1,
                            layoutAnimation: false
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
                
                

                var myChart = initChart();
                myChart.setOption(option1);
            })
            .catch(error => console.error('Error:', error));
    }

    // 根据权重获取颜色
    function getWeightColor(weight, maxWeight) {
        var intensity = weight / maxWeight;
        var color = echarts.color.lerp(intensity, ['#FFFFFF', '#FF0000']);
        return color;
    }

    // 事件监听器
    document.getElementById('centripetal-btn').addEventListener('click', function() {
        var uid = document.getElementById('search-input').value;
        var progressBar = document.getElementById('progress-bar');
        progressBar.style.width = '0%'; // 重置进度条为0
        updateProgressBar(0); // 初始化进度条为0%
        startRandomProgress();
        fetchProgress(); // 启动进度条的更新
        fetch('get-cenc-data', {
            method: 'POST',
            body: new URLSearchParams({ 'uid': uid }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => {
            createTable(data);
            updateProgressBar(100); 
        })
        .catch(error => console.error('Error:', error));
    });

    // document.getElementById('1degree-topo-btn').addEventListener('click', function() {
    //     fetchGraphData(false);  // 无权重
    // });

    // 获取图表数据并生成图表
    function fetchGraphDatatop10(withWeight) {
        var selectedNodeIndex = document.getElementById('top10-select').value;
        var url = 'get-edgelist-data-cenc-top10?index=' + selectedNodeIndex;
        fetch(url)
            .then(response => response.json())
            .then(graph_data => {
                initChart2()
                var maxWeight = 0;

                // 找出value值不为0的节点
                var not_zero = graph_data.nodes.filter(node => node.value != 0);
                // 找出value值=graph_data长度的节点
                var top1 = graph_data.nodes.filter(node => node.value == graph_data.nodes.length);

                // 为每个节点设置样式，前十的节点标红，其他节点标蓝
                graph_data.nodes.forEach(node => {
                    node.symbolSize = top1.includes(node) ? 100 : 20;
                    node.label = {
                        normal: {
                            show: top1.includes(node) ? true : false,
                            // symbolSize: 12,
                            color: '#000000',
                            // 字体大小
                            fontSize: 16,
                            formatter: node.name
                        }
                    };
                    node.itemStyle = {
                        normal: {
                            color: not_zero.includes(node) ? '#CD5C5C' : '#6495ED',
                            borderWidth: 0.5,
                            borderColor: '#FFF',
                            shadowBlur: 5,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
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
                        focusNodeAdjacency: false,
                        draggable: false,
                        roam: true,
                        force: {
                            repulsion: 500,
                            edgeLength: 500,
                            gravity: 0.1,
                            layoutAnimation: false
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
                
                

                var myChart = initChart2();
                myChart.setOption(option1);
            })
            .catch(error => console.error('Error:', error));
    }

   
    // 事件监听器
    // document.getElementById('centripetal-btn').addEventListener('click', function() {
    //     var uid = document.getElementById('search-input').value;
    //     fetch('get-cenc-data', {
    //         method: 'POST',
    //         body: new URLSearchParams({ 'uid': uid }),
    //         headers: {
    //             'Content-Type': 'application/x-www-form-urlencoded',
    //         },
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         createTable(data);
    //     })
    //     .catch(error => console.error('Error:', error));
    // });



    document.getElementById('centripetal-topo-btn').addEventListener('click', function() {
        
        fetchGraphData(true);  // 带权重
    });

    document.getElementById('simulate-top10').addEventListener('click', function() {
        




        fetchGraphDatatop10(true); 
    });


});
