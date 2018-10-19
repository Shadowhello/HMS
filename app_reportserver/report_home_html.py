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
                <td class="user_td_value">${user['nl']}</td>
            </tr>
            <tr>
                <td class="user_td_label">电话：</td>
                <td class="user_td_value">${user['sjhm']}</td>
            </tr>
            <tr>
                <td class="user_td_label">日期：</td>
                <td class="user_td_value">${user['qdrq']}</td>
            </tr> 
            % if user['film']:
                <tr>
                    <td class="user_td_label">胶片：</td>
                    <td class="user_td_value"><img src=${user['film']} /></td>
                </tr>   
            % endif         
        </table>
    </div>
</div>
</body>
</html>
'''
# 循环定义
'''
        <%
            user_lable = OrderedDict([
                                        ('姓名：','xm'),
                                        ('ID号：','tjbh'),
                                        ('单位：','dwmc'),
                                        ('性别：','xb'),
                                        ('年龄：','nl'),
                                        ('电话：','sjhm'),
                                        ('日期：','qdrq'),
                                        ('胶片：','film')
                                    ])
            user = user
        %>
        % for user_key,user_value in user_lable.items():
            % if user_value == 'tjbh':
                <tr>
                    <td class="user_td_label">user_key</td>
                    <td class="user_td_value"><img src=${user[user_value]} /></td>
                </tr>
            % elif user_value == 'film':
                % if user[user_value]:
                   <tr>
                        <td class="user_td_label">user_key</td>
                        <td class="user_td_value"><img src=${user[user_value]} /></td>
                    </tr>
                % endif
            % else:
                <tr>
                    <td class="user_td_label">user_key</td>
                    <td class="user_td_value"><img src=${user[user_value]} /></td>
                </tr>
            % endif  
        % endfor     
'''
# '''

# '''

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