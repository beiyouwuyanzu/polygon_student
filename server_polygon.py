# coding: utf-8
import json
from flask import Flask, redirect, url_for, request
import flask
from flask import render_template
import os
# from sign_tool import process
from datetime import timedelta
import time
import redis
from tools import read_excel


r = redis.Redis(host = 'localhost', port = 6379, db = 0, password = 'demaxiya')

app = Flask(__name__)
# 自动重载模板文件
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=30)

@app.route('/success/<pattern>')
def success(pattern):
    return 'welcome %s' % pattern

def execCmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    name = time.strftime('%Y-%m-%d.xlsx', time.localtime(time.time()))
    f = request.files['file']
    f.save("file/" + name)
    if read_excel("file/" + name):
        return "save_success"
    else:
        return "load wrong, please check format of excel"

@app.route('/get_polygon/<name>')
def get_polygon(name):
    res = r.lindex(f'polygon_{name}', 0)
    if not res:
        return "not found"
    items = res.decode('utf-8').split('|')
    items = [int(x) if x.isnumeric() else x for x in items]
    return json.dumps(items)


@app.route('/regex_match',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        pattern = request.form['pattern']
        match = execCmd("shuf -n 100000 20200910query | ./regex_tools '{}' | grep 'ED$' | head -n 100".format(pattern)) 
        nomatch = execCmd("shuf -n 100000 20200910query | ./regex_tools '{}' | grep 'NO$' | head -n 100".format(pattern)) 
        return 'match 100 line:\n\n'+match+'\n\n\n\n\n\n'+'unmatch 100 lines\n\n'+nomatch
    else:
        user = request.args.get('pattern')
        return redirect(url_for('success',pattern = pattern))

@app.route('/check')
def rerun_query():
    return render_template('signcheck.html')

@app.route('/')
def index_page():
    return "not found"

@app.route('/update')
def update():
    return render_template('index.html')

@app.route('/signcheck', methods = ['POST', 'GET'])
def signcheck():

    allname = request.form['allname']
    signinfo = request.form['signinfo']
    
    print(allname)
    print(signinfo)
    result = "请求成功"
    try:
        #result = process(allname, signinfo)
        pass
    except Exception as e:
        result = "失败啦！"
    return result

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/lol')
def lol():
    return render_template('web.html')

@app.route('/file/<name>')
def getfile(name):
    if name in os.listdir('templates'):
        return render_template(name)
    return "not found"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug = True, ssl_context=('8452336_req.wangyaqi.site.pem', '8452336_req.wangyaqi.site.key'))
