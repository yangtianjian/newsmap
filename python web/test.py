# coding: utf-8
from flask import Flask
from flask import request
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
    cur.execute("select title,province from news group by province")
    for row in cur.fetchall():
        str+= printme(row[0]+" 等" ,row[1],"0")

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
                <li><a href="/search">新闻列表搜索</a></li>
                <li><a href="/searchMap">新闻地图搜索</a></li>
                <li><a href="http://news.sina.com.cn/">新浪新闻</a></li>
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
        location.href = "/"+param.name;
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

def chengshiDetail(name):
    strresult = shengshiHead()
    db = mysql.connector.connect(user='root', passwd='1234', db='news', charset='utf8')
    cur = db.cursor()
    cur.execute("select title,content,link from news where province='"+name+"'")
    for row in cur.fetchall():
        strresult += prinNewsDetail(row[0], row[1], row[2])
    cur.close()
    db.close()
    return strresult + '''
                        </ul>
        ''' + shengshiEnd()

@app.route(u"/黑龙江", methods=['GET', 'POST'])
def heilongjiang():
    return chengshiDetail("黑龙江")

@app.route(u'/吉林', methods=['GET', 'POST'])
def jilin():
    return chengshiDetail("吉林")

@app.route(u'/辽宁', methods=['GET', 'POST'])
def liaoning():
    return chengshiDetail("辽宁")

@app.route(u'/河北', methods=['GET', 'POST'])
def hebei():
    return chengshiDetail("河北")

@app.route(u'/山西', methods=['GET', 'POST'])
def shanxi0():
    return chengshiDetail("山西")

@app.route(u'/陕西', methods=['GET', 'POST'])
def shanxi():
    return chengshiDetail("陕西")

@app.route(u'/山东', methods=['GET', 'POST'])
def shandong():
    return chengshiDetail("山东")

@app.route(u'/河南', methods=['GET', 'POST'])
def henan():
    return chengshiDetail("河南")

@app.route(u'/江苏', methods=['GET', 'POST'])
def jiangsu():
    return chengshiDetail("江苏")

@app.route(u'/安徽', methods=['GET', 'POST'])
def anhui():
    return chengshiDetail("安徽")

@app.route(u'/湖北', methods=['GET', 'POST'])
def hubei():
    return chengshiDetail("湖北")

@app.route(u'/四川', methods=['GET', 'POST'])
def sichuan():
    return chengshiDetail("四川")

@app.route(u'/重庆', methods=['GET', 'POST'])
def chongqing():
    return chengshiDetail("重庆")

@app.route(u'/浙江', methods=['GET', 'POST'])
def zhejiang():
    return chengshiDetail("浙江")

@app.route(u'/江西', methods=['GET', 'POST'])
def jiangxi():
    return chengshiDetail("江西")

@app.route(u'/湖南', methods=['GET', 'POST'])
def hunan():
    return chengshiDetail("湖南")

@app.route(u'/贵州', methods=['GET', 'POST'])
def guizhou():
    return chengshiDetail("贵州")

@app.route(u'/福建', methods=['GET', 'POST'])
def fujian():
    return chengshiDetail("福建")

@app.route(u'/广西', methods=['GET', 'POST'])
def guangxi():
    return chengshiDetail("广西")

@app.route(u'/广东', methods=['GET', 'POST'])
def guangdong():
    return chengshiDetail("广东")

@app.route(u'/海南', methods=['GET', 'POST'])
def hainan():
    return chengshiDetail("海南")


@app.route('/searchResult', methods=['POST'])
def searchResult():
    keyword=request.form['keyword']
    return shengshiHead()+prinNewsDetail(keyword,keyword,"http://www.baidu.com/")+prinNewsDetail("新闻标题2","新闻标题2","http://www.baidu.com/")+'''
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
    # 需要从request对象读取表单内容
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

@app.route('/search',  methods=['GET', 'POST'])
def indexSearch():
    return'''
    <!DOCTYPE HTML>
<html>
<head>
<title>新闻搜索</title>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="http://dreamspark.com.cn/style.css" rel="stylesheet" type="text/css" media="all" />
<script src="http://dreamspark.com.cn/jquery.min.js"></script>
    <link rel="stylesheet" href="http://dreamspark.com.cn/amazeui.min.css">
    <link rel="stylesheet" href="http://dreamspark.com.cn/public.css">

    <script src="http://dreamspark.com.cn/amazeui.min.js"></script>
</head>
<body>
<header class="am-topbar am-topbar-fixed-top wos-header">
    <div class="am-container">
        <h1 class="am-topbar-brand">
            <a href="#"><img src="http://dreamspark.com.cn/images/logo.png" alt=""></a>
        </h1>
        <div class="am-collapse am-topbar-collapse" id="collapse-head">
            <ul class="am-nav am-nav-pills am-topbar-nav">
                <li><a href="/">首页</a></li>
                <li class="am-active"><a href="#">新闻搜索</a></li>
            </ul>
        </div>
    </div>
</header>

<div class="index-banner">

	    <div class="wmuSlider example1">
			   <article style="position: absolute; width: 100%; opacity: 0;"> 
				   	<div class="banner-wrap">
						<div class="cont span_2_of_3">
						    <h1>SEARCH NEWS.</h1>
						     <div class="search_box">
								<form action="/searchResult" method="post">
								   <input name="keyword" type="text"><input type="submit" value="">
							    </form>
			 				</div>
						</div>
					</div>
				 </article>
				 <article style="position: absolute; width: 100%; opacity: 0;"> 
				   	<div class="banner-wrap">
						<div class="cont span_2_of_3">
						   <h1>NEWS MAP, A NEW WAY TO GET NEWS.</h1>
						</div>
					</div>
				 </article>
		  </div>
                  <script src="http://dreamspark.com.cn/jquery.wmuSlider.js"></script> 
					<script>
       				     $('.example1').wmuSlider();         
   					</script> 	           	      
   	   </div>
</body>
</html>
    '''

@app.route('/searchMap',  methods=['GET', 'POST'])
def indexSearch2():
    return'''
    <!DOCTYPE HTML>
<html>
<head>
<title>新闻搜索</title>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="http://dreamspark.com.cn/style.css" rel="stylesheet" type="text/css" media="all" />
<script src="http://dreamspark.com.cn/jquery.min.js"></script>
    <link rel="stylesheet" href="http://dreamspark.com.cn/amazeui.min.css">
    <link rel="stylesheet" href="http://dreamspark.com.cn/public.css">

    <script src="http://dreamspark.com.cn/amazeui.min.js"></script>
</head>
<body>
<header class="am-topbar am-topbar-fixed-top wos-header">
    <div class="am-container">
        <h1 class="am-topbar-brand">
            <a href="#"><img src="http://dreamspark.com.cn/images/logo.png" alt=""></a>
        </h1>
        <div class="am-collapse am-topbar-collapse" id="collapse-head">
            <ul class="am-nav am-nav-pills am-topbar-nav">
                <li><a href="/">首页</a></li>
                <li class="am-active"><a href="#">新闻搜索</a></li>
            </ul>
        </div>
    </div>
</header>

<div class="index-banner">

	    <div class="wmuSlider example1">
			   <article style="position: absolute; width: 100%; opacity: 0;"> 
				   	<div class="banner-wrap">
						<div class="cont span_2_of_3">
						    <h1>SEARCH NEWS.</h1>
						     <div class="search_box">
								<form action="/searchMapResult" method="post">
								   <input name="keyword" type="text"><input type="submit" value="">
							    </form>
			 				</div>
						</div>
					</div>
				 </article>
				 <article style="position: absolute; width: 100%; opacity: 0;"> 
				   	<div class="banner-wrap">
						<div class="cont span_2_of_3">
						   <h1>NEWS MAP, A NEW WAY TO GET NEWS.</h1>
						</div>
					</div>
				 </article>
		  </div>
                  <script src="http://dreamspark.com.cn/jquery.wmuSlider.js"></script> 
					<script>
       				     $('.example1').wmuSlider();         
   					</script> 	           	      
   	   </div>
</body>
</html>
    '''


@app.route('/searchMapResult', methods=['POST'])
def home2():
    keyword = request.form['keyword']
    db = mysql.connector.connect(user='root', passwd='1234', db='news', charset='utf8')

    cur = db.cursor()
    # cur.execute('select title,province from news')
    cur.execute("select province,count(*) from news group by province")
    str = ""
    for row in cur.fetchall():
        str += printme("新闻：", row[0], row[1])
    cur.execute("select title,province from news group by province")
    for row in cur.fetchall():
        str += printme(row[0] + " 等", row[1], "0")

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
                <li><a href="/search">新闻列表搜索</a></li>
                <li><a href="/searchMap">新闻地图搜索</a></li>
                <li><a href="http://news.sina.com.cn/">新浪新闻</a></li>
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
        location.href = "/"+param.name;
    });
    myChart.setOption(option);
</script>
</body>
</html>
'''
    return partHead + str + partEnd

if __name__ == '__main__':
    app.run()