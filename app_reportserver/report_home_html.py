# 首页信息
pdf_html_home_page= '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="pragma" CONTENT="no-cache"> 
    <meta http-equiv="Cache-Control" CONTENT="no-cache, must-revalidate"> 
    <meta http-equiv="expires" CONTENT="0">
    <link rel="stylesheet" type="text/css" href=${user['css']} >
</head>
<body>
<div class="sum">
    <div>
        <div class="user">
            <div>
                <img src=${user['head_pic']} class="image" />
            </div>
            <div class="user_tag">
                <table class="user_table">
                    <tr>
                        <td class="user_td">体&nbsp;检&nbsp;编&nbsp;号 &nbsp;<hr class="line2" /></td>
                        <td colspan="3"><img src=${user['tm']} /><hr class="line" /></td>
                    </tr>
                    <tr>
                        <td class="user_td">姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名&nbsp;&nbsp;<hr class="line2" /></td>
                        <td>${user['xm']}<hr class="line" /></td>
                        <td class="user_td">性&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;别&nbsp;&nbsp;<hr class="line2" /></td>
                        <td>${user['xb']}<hr class="line" /></td>
                    </tr>
                    <tr>
                        <td class="user_td">年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;龄&nbsp;&nbsp;<hr class="line2" /></td>
                        <td>${user['nl']}<hr class="line" /></td>
                        <td class="user_td">电&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话&nbsp;&nbsp;<hr class="line2" /></td>
                        <td>${user['sjhm']}<hr class="line" /></td>
                    </tr>
                    <tr>
                        <td class="user_td">体&nbsp;检&nbsp;日&nbsp;期 &nbsp;<hr class="line2" /></td>
                        <td colspan="3">${user['qdrq']}<hr class="line" /></td>
                    </tr>
                    <tr>
                        <td class="user_td">单&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;位&nbsp;&nbsp;<hr class="line2" /></td>
                        <td colspan="3">${user['dwmc']}<hr class="line" /></td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
</body>
</html>
'''