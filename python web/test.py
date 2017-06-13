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
            text: ['500','0'],
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
    if(param.value>0)
        location.href = "/"+param.name;
    });
    myChart.setOption(option);
</script>

<div data-am-widget="gotop" class="am-gotop am-gotop-fixed" >
    <a href="#top" title="回到顶部">
        <span class="am-gotop-title">回到顶部</span>
        <i class="am-gotop-icon am-icon-chevron-up"></i>
    </a>
</div>

<footer>
    <div class="content">
        <ul class="am-avg-sm-5 am-avg-md-5 am-avg-lg-5 am-thumbnails">
            <li><a href="#">联系我们</a></li>
            <li><a href="#">加入我们</a></li>
            <li><a href="#">合作伙伴</a></li>
            <li><a href="#">广告及服务</a></li>
            <li><a href="#">友情链接</a></li>
        </ul>
        <p>数据库操作系统实践课小组出品<br>© 2017 AllMobilize, Inc. Licensed under MIT license.</p>
        <div class="w2div">
            <ul data-am-widget="gallery" class="am-gallery am-avg-sm-2
  am-avg-md-2 am-avg-lg-2 am-gallery-overlay" data-am-gallery="{ pureview: true }" >
            </ul>
        </div>
    </div>
</footer>
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
                <li><a href="/search">新闻列表搜索</a></li>
                <li><a href="/searchMap">新闻地图搜索</a></li>
                <li class="am-active"><a href="#">新闻列表</a></li>
            </ul>
        </div>
    </div>
</header>

<div class="am-g am-container newatype">
    <div class="am-u-sm-12 am-u-md-12 am-u-lg-8 oh">
        <div data-am-widget="titlebar" class="am-titlebar am-titlebar-default" style="border-bottom: 0px; margin-bottom: -10px">
            <h2 class="am-titlebar-title ">
                新闻列表
            </h2>
        </div>

        <div data-am-widget="list_news" class="am-list-news am-list-news-default news">
            <div class="am-list-news-bd">
                <ul class="am-list">

    '''
def shengshiEnd():
    return'''
</ul>
            </div>

        </div>
    </div>

    <div class="am-u-sm-12 am-u-md-12 am-u-lg-4">
        <div data-am-widget="titlebar" class="am-titlebar am-titlebar-default">
            <h2 class="am-titlebar-title ">
                广告
            </h2>
        </div>
        <div data-am-widget="list_news" class="am-list-news am-list-news-default right-bg" data-am-scrollspy="{animation:'fade'}">
                <ul class="am-list"  >
                    <li class="am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left">


                        <div class=" am-u-sm-8 am-list-main">
                            <h3 class="am-list-item-hd"><a href="http://news.sina.com.cn/">新浪新闻</a></h3>

                            <div class="am-list-item-text">新浪新闻由新浪官方出品，及时获取全球新闻资讯，国内国外要闻，精彩的体育赛事报道，金融财经动向，影视娱乐事件，还有独家微博“微”新闻，精彩随你看，新闻、星座、笑话一个都不少。</div>
                        </div>
                    </li>
                    <hr data-am-widget="divider" style="" class="am-divider am-divider-default" />
                    <li class="am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left">


                        <div class=" am-u-sm-8 am-list-main">
                            <h3 class="am-list-item-hd"><a href="http://news.qq.com/">腾讯新闻</a></h3>

                            <div class="am-list-item-text">《腾讯新闻》是腾讯团队用心打造的一款丰富、及时的新闻应用，本着精炼、轻便的目标，为用户提供高效、优质的阅读体验。全球视野，聚焦中国，一朝在手，博览天下。</div>

                        </div>
                    </li>
                    <hr data-am-widget="divider" style="" class="am-divider am-divider-default" />
                    <li class="am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left">


                        <div class=" am-u-sm-8 am-list-main">
                            <h3 class="am-list-item-hd"><a href="http://news.baidu.com/">百度新闻</a></h3>

                            <div class="am-list-item-text">百度新闻是百度公司推出的中文新闻搜索平台，每天发布多条新闻，新闻源包括500多个权威网站，热点新闻由新闻源网站和媒体每天“民主投票”选出，不含任何人工编辑成分，真实反映每时每刻的新闻热点</div>

                        </div>
                        
                    </li>
                    
                </ul>
        </div>
    </div>
</div>

<div data-am-widget="gotop" class="am-gotop am-gotop-fixed" >
    <a href="#top" title="回到顶部">
        <span class="am-gotop-title">回到顶部</span>
        <i class="am-gotop-icon am-icon-chevron-up"></i>
    </a>
</div>

<footer>
    <div class="content">
        <ul class="am-avg-sm-5 am-avg-md-5 am-avg-lg-5 am-thumbnails">
            <li><a href="#">联系我们</a></li>
            <li><a href="#">加入我们</a></li>
            <li><a href="#">合作伙伴</a></li>
            <li><a href="#">广告及服务</a></li>
            <li><a href="#">友情链接</a></li>
        </ul>
        <p>数据库操作系统实践课小组出品<br>© 2017 AllMobilize, Inc. Licensed under MIT license.</p>
        <div class="w2div">
            <ul data-am-widget="gallery" class="am-gallery am-avg-sm-2
  am-avg-md-2 am-avg-lg-2 am-gallery-overlay" data-am-gallery="{ pureview: true }" >
            </ul>
        </div>
    </div>
</footer>

</body>
</html>
    '''

def prinNewsDetail(title, context,link,time):
    return '''
                        <li class="am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left" data-am-scrollspy="{animation:'fade'}">

                        <div class=" am-u-sm-9 am-list-main">
                            <h3 class="am-list-item-hd"><a target='_blank' href="'''+link+'''">''' + title + '''</a></h3>
                           <div class="am-list-item-text">''' + context + '''</div>
                        </div>

                    </li>
                    <div class="newsico am-fr">
                        <i class="am-icon-clock-o">'''+str(time)+'''</i>
                    </div>

    '''

def chengshiDetail(name):
    strresult = shengshiHead()
    db = mysql.connector.connect(user='root', passwd='1234', db='news', charset='utf8')
    cur = db.cursor()
    cur.execute("select title,content,link,time_happened from news where province='"+name+"' order by time_happened desc")
    for row in cur.fetchall():
        strresult += prinNewsDetail(row[0], row[1], row[2], row[3])
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

    strresult=""
    db = mysql.connector.connect(user='root', passwd='1234', db='news', charset='utf8')
    cur = db.cursor()
    cur.execute("select title,content,link,time_happened from news where title like '%"+keyword+"%' order by time_happened desc")
    for row in cur.fetchall():
        strresult += prinNewsDetail(row[0], row[1], row[2], row[3])
    cur.close()
    db.close()

    return shengshiHead()+strresult+'''
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
                <li class="am-active"><a href="#">新闻列表搜索</a></li>
                <li><a href="/searchMap">新闻地图搜索</a></li>
            </ul>
        </div>
    </div>
</header>

<div class="index-banner">

	    <div class="wmuSlider example1">
			   <article style="position: absolute; width: 100%; opacity: 0;"> 
				   	<div class="banner-wrap">
						<div class="cont span_2_of_3">
						    <h1>SEARCH NEWS</h1>
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
						   <h1>NEWS MAP, GET NEWS FROM MAP.</h1>
						</div>
					</div>
				 </article>
		  </div>
                  <script src="http://dreamspark.com.cn/jquery.wmuSlider.js"></script> 
					<script>
       				     $('.example1').wmuSlider();
   					</script>
   	   </div>
   	   
   	   <div data-am-widget="gotop" class="am-gotop am-gotop-fixed" >
    <a href="#top" title="回到顶部">
        <span class="am-gotop-title">回到顶部</span>
        <i class="am-gotop-icon am-icon-chevron-up"></i>
    </a>
</div>

<footer>
    <div class="content">
        <ul class="am-avg-sm-5 am-avg-md-5 am-avg-lg-5 am-thumbnails">
            <li><a href="#">联系我们</a></li>
            <li><a href="#">加入我们</a></li>
            <li><a href="#">合作伙伴</a></li>
            <li><a href="#">广告及服务</a></li>
            <li><a href="#">友情链接</a></li>
        </ul>
        <p>数据库操作系统实践课小组出品<br>© 2017 AllMobilize, Inc. Licensed under MIT license.</p>
        <div class="w2div">
            <ul data-am-widget="gallery" class="am-gallery am-avg-sm-2
  am-avg-md-2 am-avg-lg-2 am-gallery-overlay" data-am-gallery="{ pureview: true }" >
            </ul>
        </div>
    </div>
</footer>
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
                <li><a href="/search">新闻列表搜索</a></li>
                <li class="am-active"><a href="#">新闻地图搜索</a></li>
            </ul>
        </div>
    </div>
</header>

<div class="index-banner">

	    <div class="wmuSlider example1">
			   <article style="position: absolute; width: 100%; opacity: 0;"> 
				   	<div class="banner-wrap">
						<div class="cont span_2_of_3">
						    <h1>SEARCH NEWS</h1>
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
   	   
   	   <div data-am-widget="gotop" class="am-gotop am-gotop-fixed" >
    <a href="#top" title="回到顶部">
        <span class="am-gotop-title">回到顶部</span>
        <i class="am-gotop-icon am-icon-chevron-up"></i>
    </a>
</div>

<footer>
    <div class="content">
        <ul class="am-avg-sm-5 am-avg-md-5 am-avg-lg-5 am-thumbnails">
            <li><a href="#">联系我们</a></li>
            <li><a href="#">加入我们</a></li>
            <li><a href="#">合作伙伴</a></li>
            <li><a href="#">广告及服务</a></li>
            <li><a href="#">友情链接</a></li>
        </ul>
        <p>数据库操作系统实践课小组出品<br>© 2017 AllMobilize, Inc. Licensed under MIT license.</p>
        <div class="w2div">
            <ul data-am-widget="gallery" class="am-gallery am-avg-sm-2
  am-avg-md-2 am-avg-lg-2 am-gallery-overlay" data-am-gallery="{ pureview: true }" >
            </ul>
        </div>
    </div>
</footer>
</body>
</html>
    '''


@app.route('/searchMapResult', methods=['POST'])
def home2():
    keyword = request.form['keyword']
    db = mysql.connector.connect(user='root', passwd='1234', db='news', charset='utf8')

    cur = db.cursor()
    cur.execute("select province,count(*) from news where title like '%" + keyword + "%' group by province")
    str = ""
    for row in cur.fetchall():
        str += printme("新闻：", row[0], row[1])
    cur.execute("select title,province from news where title like '%" + keyword + "%' group by province")
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
                <li><a href="/">首页</a></li>
                <li><a href="/searchMap">新闻列表搜索</a></li>
                <li><a href="/search">新闻地图搜索</a></li>
                <li class="am-active"><a href="#">新闻地图搜索</a></li>
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
            max: 200,
            left: 'left',
            top: 'bottom',
            text: ['200','0'],
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

<div data-am-widget="gotop" class="am-gotop am-gotop-fixed" >
    <a href="#top" title="回到顶部">
        <span class="am-gotop-title">回到顶部</span>
        <i class="am-gotop-icon am-icon-chevron-up"></i>
    </a>
</div>

<footer>
    <div class="content">
        <ul class="am-avg-sm-5 am-avg-md-5 am-avg-lg-5 am-thumbnails">
            <li><a href="#">联系我们</a></li>
            <li><a href="#">加入我们</a></li>
            <li><a href="#">合作伙伴</a></li>
            <li><a href="#">广告及服务</a></li>
            <li><a href="#">友情链接</a></li>
        </ul>
        <p>数据库操作系统实践课小组出品<br>© 2017 AllMobilize, Inc. Licensed under MIT license.</p>
        <div class="w2div">
            <ul data-am-widget="gallery" class="am-gallery am-avg-sm-2
  am-avg-md-2 am-avg-lg-2 am-gallery-overlay" data-am-gallery="{ pureview: true }" >
            </ul>
        </div>
    </div>
</footer>
</body>
</html>
'''
    return partHead + str + partEnd

if __name__ == '__main__':
    app.run()