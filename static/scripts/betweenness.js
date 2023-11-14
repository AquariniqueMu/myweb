
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
        var container = document.getElementById('table-container-bc');
        container.innerHTML = '';
        var table = document.createElement('table');
        table.className = 'table';
      
        var thead = document.createElement('thead');
        var headerRow = document.createElement('tr');
        var headers = ['节点名称','介数中心性'];
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
        fetch('get-edgelist-data-bc')
            .then(response => response.json())
            .then(graph_data => {
                
                var maxWeight = 0;
                if (withWeight) {
                    maxWeight = Math.max(...graph_data.nodes.map(node => node.value));
                }
                // 找出value值前十的节点
                var top10 = graph_data.nodes.sort((a, b) => b.value - a.value).slice(0, 10);
                // 为每个节点设置样式，前十的节点标红，其他节点标蓝
                graph_data.nodes.forEach(node => {
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
                            color: top10.includes(node) ? '#FF0000' : '#0000FF',
                            symbolSize:top10.includes(node) ? 100 : 12
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
                        symbolSize: 20,
                        focusNodeAdjacency: true,
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
    document.getElementById('betweenness-btn').addEventListener('click', function() {
        var uid = document.getElementById('search-input').value;
        fetch('get-bc-data', {
            method: 'POST',
            body: new URLSearchParams({ 'uid': uid }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => {
            createTable(data);
        })
        .catch(error => console.error('Error:', error));
    });

    // document.getElementById('1betweenness-topo-btn').addEventListener('click', function() {
    //     fetchGraphData(false);  // 无权重
    // });

    // 获取图表数据并生成图表
    function fetchGraphDatatop10(withWeight) {
        var selectedNodeIndex = document.getElementById('top10-select').value;
        var url = 'get-edgelist-data-bc-top10?index=' + selectedNodeIndex;
        fetch(url)
            .then(response => response.json())
            .then(graph_data => {
                initChart2()
                var maxWeight = 0;
                if (withWeight) {
                    maxWeight = Math.max(...graph_data.nodes.map(node => node.value));
                }
                // 找出value值不为0的节点
                var not_zero = graph_data.nodes.filter(node => node.value != 0);
                // 找出value值=graph_data长度的节点
                var top1 = graph_data.nodes.filter(node => node.value == graph_data.nodes.length);

                // 为每个节点设置样式，前十的节点标红，其他节点标蓝
                graph_data.nodes.forEach(node => {
                    node.label = {
                        normal: {
                            show: top1.includes(node) ? true : false,
                            // symbolSize: 12,
                            color: '#000000',
                            // 字体大小
                            fontSize: 8,
                            formatter: node.name
                        }
                    };
                    node.itemStyle = {
                        normal: {
                            color: not_zero.includes(node) ? '#FF0000' : '#0000FF',
                            symbolSize:top1.includes(node) ? 36 : 12
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
                
                

                var myChart = initChart2();
                myChart.setOption(option1);
            })
            .catch(error => console.error('Error:', error));
    }

   
    // 事件监听器
    document.getElementById('betweenness-btn').addEventListener('click', function() {
        var uid = document.getElementById('search-input').value;
        fetch('get-bc-data', {
            method: 'POST',
            body: new URLSearchParams({ 'uid': uid }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => {
            createTable(data);
        })
        .catch(error => console.error('Error:', error));
    });



    document.getElementById('betweenness-topo-btn').addEventListener('click', function() {
        fetchGraphData(true);  // 带权重
    });

    document.getElementById('simulate-top10').addEventListener('click', function() {
        





        fetchGraphDatatop10(true); 
    });


});
