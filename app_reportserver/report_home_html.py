# 首页信息
pdf_html_home_page= '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="pragma" CONTENT="no-cache"> 
    <meta http-equiv="Cache-Control" CONTENT="no-cache, must-revalidate"> 
    <meta http-equiv="expires" CONTENT="0">
    <link rel="stylesheet" type="text/css" href=${user['cover_css']} >
</head>
<body style="background-image:url(${user['head_pic']});
             background-repeat:no-repeat;
             background-size:1240px 1680px;
             background-position:top center;">

<div class="user">
    <div class="user_tag">
        <table class="user_table">
            <tr>
                <td class="user_td_label">姓名：</td>
                <td class="user_td_value">${user['xm']}</td>
            </tr>
            <tr>
                <td class="user_td_label">ID号：</td>
                <td class="user_td_value"><img src=${user['tm']} /></td>
            </tr>
            <tr>
                <td class="user_td_label">单位：</td>
                <td class="user_td_value">${user['dwmc']}</td>
            </tr>
            <tr>
                <td class="user_td_label">性别：</td>
                <td class="user_td_value">${user['xb']}</td>
            </tr>
            <tr>
                <td class="user_td_label">年龄：</td>
                <td colspan="3" class="user_td_value">${user['nl']}</td>
            </tr>
            <tr>
                <td class="user_td_label">电话：</td>
                <td class="user_td_value">${user['sjhm']}</td>
            </tr>
            <tr>
                <td class="user_td_label">日期：</td>
                <td class="user_td_value">${user['qdrq']}</td>
            </tr>

        </table>
    </div>
</div>
</body>
</html>
'''

# 首页信息：历史
pdf_html_home_page2= '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="pragma" CONTENT="no-cache"> 
    <meta http-equiv="Cache-Control" CONTENT="no-cache, must-revalidate"> 
    <meta http-equiv="expires" CONTENT="0">
    <link rel="stylesheet" type="text/css" href=${user['cover_css']} >
</head>
<body style="background-image:url(${user['head_pic']});
             background-repeat:no-repeat;
             background-size:1240px 1680px;
             background-position:top center;">
<div class="sum">
    <div>
        <div class="user">
            <div class="user_tag">
                <table class="user_table">
                    <tr>
                        <td class="user_td_label">体&nbsp;检&nbsp;编&nbsp;号 &nbsp;</td>
                        <td colspan="3" class="user_td_value2"><img src=${user['tm']} /></td>
                    </tr>
                    <tr>
                        <td class="user_td_label">姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名&nbsp;&nbsp;</td>
                        <td class="user_td_value">${user['xm']}</td>
                        <td class="user_td_label">性&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;别&nbsp;&nbsp;</td>
                        <td class="user_td_value">${user['xb']}</td>
                    </tr>
                    <tr>
                        <td class="user_td_label">年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;龄&nbsp;&nbsp;</td>
                        <td class="user_td_value">${user['nl']}</td>
                        <td class="user_td_label">电&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话&nbsp;&nbsp;</td>
                        <td class="user_td_value">${user['sjhm']}</td>
                    </tr>
                    <tr>
                        <td class="user_td_label">体&nbsp;检&nbsp;日&nbsp;期 &nbsp;<hr class="line2" /></td>
                        <td colspan="3" class="user_td_value">${user['qdrq']}</td>
                    </tr>
                    <tr>
                        <td class="user_td_label">单&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;位&nbsp;&nbsp;</td>
                        <td colspan="3" class="user_td_value">${user['dwmc']}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
</body>
</html>
'''