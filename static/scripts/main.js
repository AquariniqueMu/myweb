/*
 * @Description: 
 * @Author: Junwen Yang
 * @Date: 2023-11-06 10:43:19
 * @LastEditTime: 2023-11-13 23:48:42
 * @LastEditors: Junwen Yang
 */
// scripts/main.js
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
    progressBar.style.width = percentage + '%';
}

document.addEventListener('DOMContentLoaded', function() {
    
  document.getElementById('search-btn').addEventListener('click', function() {
      
      var uid = document.getElementById('search-input').value; // 获取输入的uid
      fetch('/crawl', {
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
  
  document.getElementById('download-btn').addEventListener('click', function() {
    var uid = document.getElementById('search-input').value; // 获取输入的uid
    // 下载表格
    fetch('/download-table', {
        method: 'POST',
        body: new URLSearchParams({ 'uid': uid }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.blob())
    .then(blob => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'repo_'+uid + '.xlsx';
        a.click();
    })
    .catch(error => console.error('Error:', error));
    
});

});

function createTable(data) {
  var container = document.getElementById('table-container');
  container.innerHTML = ''; // 清空现有的表格
  var table = document.createElement('table');
  table.className = 'table'; // 确保应用了之前定义的CSS样式

  // 添加表头
  var thead = document.createElement('thead');
  var headerRow = document.createElement('tr');
  var headers = ['发布时间','微博编号','文本内容','发布终端','转发数','评论数','点赞数','用户编号','昵称','发布地址', '转发微博编号', '转发微博文本', '转发微博作者编号', '转发微博作者昵称']; // 表头标题数组
  headers.forEach(function(header) {
      var th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // 添加表行
  var tbody = document.createElement('tbody');
  data.forEach(function(row) {
      var tr = document.createElement('tr');
      // 遍历每个属性并添加到行中
      headers.forEach(function(header) {
          var td = document.createElement('td');
          // 使用属性名从row对象中获取对应的值
          td.textContent = row[header.toLowerCase()]; // 假设后端返回的属性名与表头标题的小写匹配
          tr.appendChild(td);
      });
      tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  container.appendChild(table);
}

