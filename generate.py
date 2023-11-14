'''
Description: 
Author: Junwen Yang
Date: 2023-09-09 00:10:36
LastEditTime: 2023-09-09 00:33:03
LastEditors: Junwen Yang
'''
from flask import Flask, render_template, request, send_from_directory
import os
from repost import repo_main
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # 获取用户输入的ID
    weibo_id = request.form.get('weibo_id')
    cookie = request.form.get('cookie')
    # 调用你的Python代码生成xlsx文件
    # 假设你的代码函数为generate_xlsx(weibo_id)，并返回文件路径
    file_path = repo_main(weibo_id, cookie)
    
    # 返回文件给用户
    return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
