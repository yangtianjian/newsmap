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

    #cur.execute('select a.title,a.province from (select row_number()over(partition by menu_parentid order by province) as num,t.* from news t)a where num<=3')

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
  <link rel="stylesheet" href="http://dreamspark.com.cn/public.css">
      <link rel="stylesheet" href="http://dreamspark.com.cn/amazeui.min.css">
</head>
<body>

<header class="am-topbar am-topbar-fixed-top wos-header">
    <div class="am-container">
        <h1 class="am-topbar-brand">
            <a href="#"><img src="http://dreamspark.com.cn/images/logo.png" alt=""></a>
        </h1>
        <div class="am-collapse am-topbar-collapse" id="collapse-head">
            <ul class="am-nav am-nav-pills am-topbar-nav">
                <li class="am-active"><a href="#">首页</a></li>
                <li><a href="http://news.sina.com.cn/">新浪新闻</a></li>
                <li><a href="http://news.qq.com/">腾讯新闻</a></li>
            </ul>
        </div>
    </div>
</header>
<br/>
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
        var urlArr = ['http://www.baidu.com','/heilongjiang'];
        switch(param.name){
            case '河南':
                location.href = urlArr[0];
                break;
            case '黑龙江':
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

def shengshiHead():
    return'''
    <!doctype html>
<html class="no-js">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>

    <link rel="stylesheet" href="http://dreamspark.com.cn/amazeui.min.css">
    <link rel="stylesheet" href="http://dreamspark.com.cn/public.css">

    <script src="http://dreamspark.com.cn/jquery.min.js"></script>
    <script src="http://dreamspark.com.cn/amazeui.min.js"></script>
    
    <body>

<header class="am-topbar am-topbar-fixed-top wos-header">
    <div class="am-container">
        <h1 class="am-topbar-brand">
            <a href="#"><img src="http://dreamspark.com.cn/images/logo.png" alt=""></a>
        </h1>
        <div class="am-collapse am-topbar-collapse" id="collapse-head">
            <ul class="am-nav am-nav-pills am-topbar-nav">
                <li><a href="/">首页</a></li>
                <li class="am-active"><a href="#">省市新闻列表</a></li>
            </ul>
        </div>
    </div>
</header>

    <div class="am-g">
        <div class="am-u-sm-0 am-u-md-2 am-u-lg-3">&nbsp;</div>
        <div class="am-u-sm-12 am-u-md-8 am-u-lg-6">
            <div data-am-widget="list_news" class="am-list-news am-list-news-default ">
                <div class="am-list-news-bd">
                    <ul class="am-list">
</head>
    '''
def shengshiEnd():
    return'''
                    </div>
            </div>
        </div>
        <div class="am-u-sm-0 am-u-md-2 am-u-lg-3">&nbsp;</div>
    </div>

</body>
</html>
    '''

def prinNewsDetail(title, context,link):
    return '''

                        <li class="am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left">
                             <div class="am-u-md-12 am-u-lg-6 userface">
                                 <h3 class="am-list-item-hd"><a href="'''+link+'''">''' + title + '''</a></h3>
                             </div>
                            <div class=" am-u-sm-7 am-list-main">
                                <div class="am-list-item-text">''' + context + '''</div>
                            </div>
                        </li>

    '''


@app.route('/heilongjiang', methods=['GET', 'POST'])
def heilongjiang():
    return shengshiHead()+prinNewsDetail("新闻标题1","新闻标题1","http://www.baidu.com/")+prinNewsDetail("新闻标题2","新闻标题2","http://www.baidu.com/")+'''
                    </ul>
                    <ul data-am-widget="pagination" class="am-pagination am-pagination-default" style="text-align: center">
                        <li class="am-pagination-prev ">
                            <a href="#" class="">上一页</a>
                        </li>

                        <li class="am-pagination-next ">
                            <a href="#" class="">下一页</a>
                        </li>

                    </ul>
    '''+shengshiEnd()

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name= "password" type="password"></p>
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