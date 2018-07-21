外链式样式表：
<head>
<link rel="stylesheet" href="report.css">
</head>

1、字体：
font-size: 50px;         /*文字大小*/
font-weight: 700;       /*值从100-900，文字粗细,700约等于Bold，不推荐使用font-weight:bold; */
font-family:微软雅黑;    /*文本的字体*/
font-style: normal | italic;  /*normal:默认值  italic:斜体*/
line-height: 50px            /*行高*/

2、背景属性
background-color：    /*背景颜色*/
background-image：    /*背景图片*/
Background-repeat：    repeat(默认)  |  no-repeat |   repeat-x   |  repeat-y     /*背景平铺*/
Background-position：  left  |  right  |  center（默认）  |  top  | bottom  /*背景定位*/
Background-attachment:   scroll（默认）  |  fixed   /*背景是否滚动*/

2.1 Background-position
background-position: right; // 方位值只写一个的时候，另外一个值默认居中。
background-position: right bottom // 写2个方位值的时候，顺序没有要求
background-position: 20px 30px // 写2个具体值的时候，第一个值代表水平方向，第二个值代表垂直方向

2.2 Background-attachment
scroll: 背景图的位置是基于盒子（假如是div）的范围进行显示
fixed：背景图的位置是基于整个浏览器body的范围进行显示，如果背景图定义在div里面，而显示的位置在浏览器范围内但是不在div的范围内的话，背景图无法显示。

3 行高
浏览器默认文字大小：16px

行高：是基线与基线之间的距离
行高 = 文字高度+上下边距

行高的单位
行高单位	文字大小	值
20px	20px	20px
2em	    20px	20px*2=40px
150%	20px	20px*150%=30px
2	    20px	20px*2=40px

总结:单位除了像素以外，行高 = 文字大小与前面数值的乘积。

行高单位	父元素文字大小（定义了行高）	子元素文字大小（子元素未定义行高时）	行高
40px	20px	                    30px	                            40px
2em	    20px	                    30px	                            40px
150%	20px	                    30px	                            30px
2	    20px	                    30px	                            60px

总结:不带单位时，行高是和子元素文字大小相乘，em和%的行高是和父元素文字大小相乘。行高以像素为单位，就是定义的行高值。

PS: 推荐行高使用像素为单位。

盒子模型
1、border（边框）
Border-top-style:  solid /*实线*/ dotted  /*点线*/ dashed  /*虚线*/  none /*无边框*/
Border-top-color   /*边框颜色*/
Border-top-width   /*边框粗细*/

除了有top系列外还有left,right,bottom系列
边框属性的连写
border-top: 1px solid #fff;

四个边框值相同的写法
border: 1px solid #fff;

2、padding（内边距）
padding-left   |   right    |  top  |  bottom
padding连写
Padding: 20px;   /*上右下左内边距都是20px*/
Padding: 20px 30px;   /*上下20px   左右30px*/
Padding: 20px  30px  40px;  /* 上内边距为20px  左右内边距为30px   下内边距为40px*/
Padding: 20px  30px   40px  50px;   /*上20px 右30px  下40px  左  50px*/

内边距撑大盒子的问题
盒子的宽度 = 定义的宽度 + 边框宽度 + 左右内边距

继承的盒子一般不会被撑大
包含（嵌套）的盒子，给子盒子设置左右内边距（内边距不大于子盒子宽度），不会撑大子盒子。
至于设置了上下内边距的话是会撑大子盒子的。（不管怎样父盒子永不变）

margin（外边距）
margin-left   | right  |  top  |  bottom
外边距连写
margin: 20px;    /*上下左右外边距20PX*/
margin: 20px 30px;   /*上下20px  左右30px*/
margin: 20px  30px  40px;     /*上20px  左右30px   下40px*/
margin: 20px  30px   40px  50px; /*上20px   右30px   下40px  左50px*/

注意:
margin: 0 auto; 盒子居中对齐
text-align:center 是盒子里面的内容居中

垂直方向外边距合并（取最大值）
两个盒子垂直布局，一个设置上外边距，一个设置下外边距，取的设置较大的值，而不是相加。

嵌套的盒子外边距塌陷
嵌套的盒子，直接给子盒子设置垂直方向外边距的时候，会发生外边距的塌陷（父盒子跟着移动）

解决方法:
1.给父盒子设置边框
2.给父盒子overflow:hidden;

浮动

1、文档流（标准流）
元素自上而下，自左而右，块元素独占一行，行内元素在一行上显示，碰到父集元素的边框换行。

2、浮动布局
float:  left   |   right /*浮动方向*/
特点：
1.元素浮动之后不占据原来的位置（脱标）
2.浮动的盒子在一行上显示
3.行内元素浮动之后自动转换为行内块元素。（不推荐使用，转行内元素最好使用display: inline-block;）

3、浮动的作用
1)文本绕图
2)制作导航（经常使用）
把无序列表 ul li 浮动起来做成的导航。
3)网页布局

4、清除浮动带来的问题

问题：当父盒子没有定义高度，嵌套的盒子浮动之后，下边的元素发生位置错误（占据父盒子的位置）。

方法一
额外标签法：在最后一个浮动元素后添加标签。

2、块内元素
/*典型代表:*/ div, h1-h6, p, ul, li
特点:
1）独占一行；
2）可以设置宽高；
3）嵌套（包含）下，子块元素宽度（没有定义情况下）和父块元素宽度默认一致。

3、行内元素
/*典型代表*/ span, a, strong, em, del, ins
特点：
1)在一行上显示；
2)不能直接设置宽高（需要转行内块）；
3)元素的宽和高就是内容撑开的宽高。

4、行内块元素(内联元素)
/*典型代表*/  input, img
特点：
1)在一行上显示；
2)可以设置宽高。

5、三者相互转换
1)块元素转行内元素 display:inline;

2)行内元素转块元素 display:block;

3)块和行内元素转行内块元素（用的最多） display:inline-block;


定位

定位有四个方向: left | right | top | bottom

1、静态定位（默认）
position: static; // 就是文档流模式的定位。
2、绝对定位
position:absolute;
然后使用left | right | top | bottom 来确定具体位置。

特点：
1.元素使用绝对定位之后不占据原来的位置（脱标）
2.元素使用绝对定位，位置是从浏览器出发。
3.嵌套的盒子，父盒子没有使用定位，子盒子绝对定位，子盒子位置是从浏览器出发。
4.嵌套的盒子，父盒子使用定位，子盒子绝对定位，子盒子位置是从父元素位置出发。
5.给行内元素使用绝对定位之后，转换为行内块。（不推荐使用，推荐使用display:inline-block;）

3、相对定位
position: relative;
特点：
1.使用相对定位，位置从自身出发。
2.不脱标，其他的元素不能占有其原来的位置。
3.子绝父相（父元素相对定位，子元素绝对定位），用的最多的场景。
4.行内元素使用相对定位不能转行内块元素。

4、固定定位
position:fixed;
特点：
1.固定定位之后，不占据原来的位置（脱标）
2.元素使用固定定位之后，位置从浏览器出发。
3.元素使用固定定位之后，会转化为行内块（不推荐，推荐使用display:inline-block;）

标签包含规范

div可以包含所有的标签。
p标签不能包含div， h1等标签（一般包含行内元素）。
h1可以包含p，div等标签（一般不这样）。
行内元素尽量包含行内元素，行内元素不要包含块元素。

如何规避脱标流
1)尽量使用标准流。
2)标准流解决不了的使用浮动。
3)浮动解决不了的使用定位。
margin-left:auto; //盒子一直往右冲，一直冲不动为止。也是 margin:0 auto; 的由来。

.child