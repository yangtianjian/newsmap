
<%--
  Created by IntelliJ IDEA.
  User: mark_liu
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>ECharts</title>
  <!-- 引入 echarts.js -->
  <script src="echarts.js"></script>
  <script src="china.js"></script>
</head>
<body>
<%!
    public String newNews(String city, String title, String num)
    {
        return "{\n" +
                "name: '"+title+"',\n" +
                "type: 'map',\n" +
                "mapType: 'china',\n" +
                "roam: false,\n" +
                "label: {\n" +
                "normal: {\n" +
                "show: true\n" +
                "},\n" +
                "emphasis: {\n" +
                "show: true\n" +
                "}\n" +
                "},\n" +
                "data:[\n" +
                "{name: '"+city+"',value: "+num+" },\n" +
                "]\n" +
                "},";
    }
%>
<!-- 为ECharts准备一个具备大小（宽高）的Dom -->
<div id="main" style="width: 1800px;height:800px;"></div>
<script type="text/javascript">
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));
    // 指定图表的配置项和数据
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
            text: ['500','0'],           // 文本，默认为数值文本
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
        series: [
            <%
                out.print(newNews("北京","车祸","10"));
                out.print(newNews("北京","哈哈","1"));
                out.print(newNews("北京","现场等等","1"));
                out.print(newNews("北京","1111111111","1"));
                out.print(newNews("北京","现场等等","1"));
                out.print(newNews("北京","等等一些","1"));
                out.print(newNews("北京","现场等等","1"));
                out.print(newNews("北京","现场等等","1"));
                out.print(newNews("北京","现场等等","1"));
                out.print(newNews("北京","现场等等","1"));
                out.print(newNews("北京","11","1"));
                out.print(newNews("北京","12","1"));
            %>
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
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
</script>
</body>
</html>