# coding: utf-8
from flask import Flask
from flask import request
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import mysql.connector

app = Flask(__name__)

def printme(title,city,num):
    str1="{ name:'"
    str1 = str1+title+"',"
    str2= """
        type: 'map',
        mapType: 'china',
        roam: false,
        label: {
        normal: {
        show: true
        },
        emphasis: {
        show: true
        }
        },
        data:[
        {name:'"""
    str2=str2+str(city)+"',value: '"+str(num) + "' },]},"
    return str1+str2

@app.route('/', methods=['GET', 'POST'])
def home():
    db = mysql.connector.connect(user='root',passwd='1234',db='news',charset='utf8')

    cur = db.cursor()
    #cur.execute('select title,province from news')
    cur.execute("select province,count(*) from news group by province")
    str=""
    for row in cur.fetchall():
        str+= printme("新闻：",row[0],row[1])
    cur.close()
    db.close()

    partHead = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>新闻地图</title>
  <script src="http://dreamspark.com.cn/echarts.js"></script>
  <script src="http://dreamspark.com.cn/china.js"></script>
</head>
<body>
<div id="main" style="width: 1800px;height:800px;"></div>
<script type="text/javascript">
    var myChart = echarts.init(document.getElementById('main'));
    
    function randomData() {
        return Math.round(Math.random()*1000);
    }
    option = {
        title: {
            text: 'NewMap',
            subtext: '新闻地图',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        visualMap: {
            min: 0,
            max: 500,
            left: 'left',
            top: 'bottom',
            text: ['300','0'],
            calculable: true
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        series: ['''

    partEnd = '''
    ]
    };

    myChart.on('click', function (param){
        var urlArr = ['http://www.baidu.com','http://www.baidu.com'];
        switch(param.name){
            case '河南':
                location.href = urlArr[0];
                break;
            case '重庆':
                location.href = urlArr[1];
                break;
            default:
                break;
        }
    });
    myChart.setOption(option);
</script>
</body>
</html>
'''
    return partHead+str+partEnd

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run()