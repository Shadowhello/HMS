user_space="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

#<meta name=”viewport” content=”width=device-width, initial-scale=1″ />

# HTML 头信息
html_head = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="pragma" CONTENT="no-cache"> 
<meta http-equiv="Cache-Control" CONTENT="no-cache, must-revalidate"> 
<meta http-equiv="expires" CONTENT="0">
<link rel="stylesheet" type="text/css" href="file:///F:/HMS/reportserver/report.css" >
</head>
<body>
<div align="center">'''

# HTML 尾信息
html_tail='''</div></body></html>'''
#
#html_home_image ='''<img src="img01.jpg" border="0" style="position:absolute; left:0px;right:0px; top:0px; width:1240px; height:1754px;float:center;"/>'''

# 首页信息
html_home_page= '''
<div class="line">
    <div class="user">
        <div>
            <img src="file:///F:/HMS/reportserver/img0.jpg" class="image" />
        </div>
        <div class="user_tag">
            <div>
                <span> 体&nbsp;检&nbsp;编&nbsp;号 &emsp;{{user.id}}</span>
                <span> <hr class="user_line" /></span>
            </div>
            <div>
                <span> 姓{{user.user_space}}名 &emsp;{{user.name}}</span>
                <span> <hr class="user_line21" /></span>
                <span class="user_space"> 性{{user.user_space}}别 &emsp;{{user.sex}}<br></span>
                <span> <hr class="user_line2" /></span>
            </div>
            <div>
                <span> 年{{user.user_space}}龄 &emsp;{{user.age}} </span>
                <span> <hr class="user_line22" /></span>
                <span class="user_space"> 电{{user.user_space}}话 &emsp;{{user.tel}}<br> </span>
                <span> <hr class="user_line2" /></span>
            </div>
            <div>
                <span> 体&nbsp;检&nbsp;日&nbsp;期 &emsp;{{user.tjrq}} </span>
                <span> <hr class="user_line" /></span>
            </div>
            <div>
                <span> 单{{user.user_space}}位 &emsp;{{user.dwmc}} </span>
                <span> <hr class="user_line" /></span>
            </div>
        </div>
    </div>
</div>
'''
# 首页信息
html_home_page2= '''
<div>
    <div class="user">
        <div>
            <img src="file:///F:/HMS/reportserver/img0.jpg" class="image" />
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
'''

# 首页信息
html_second_page= '''
<div class="page_2">
    <div style="text-align:center;">
        <div class="tj_pb">
            <br>国际保健中心开通VIP专家门诊，预约电话:0574-83009619。
            <br>周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;呼吸内科主任：纪成
            <br>周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内一科主任：董勤勇
            <br>周三下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;妇科主任：李宁宁
            <br>周五下午:15:30-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内二科主任：吴汉平
            <br>
        </div>
    </div>
</div>
'''


# 小结
html_second_page_xj = '''
<div class="page_2">
    <div class="tj_xj">
        <h1>体检小结(Summary)</h1>
        <hr />
    </div>
    <div class="tj_xj_content">
        <ul>
            {% for summary in summarys %}
             <li>{{loop.index|string+"、"+summary}}</li>
             <br>
        {% endfor %}
        </ul>
    </div>
</div>

'''

# 建议
html_second_page_jy = '''
<div class="page_2">
    <div class="tj_xj">
        <h1>体检建议(Suggestions)</h1>
        <hr />
    </div>
    <div class="tj_xj_content">
        <ul>
            {% for suggestion in suggestions %}
             <li>{{loop.index|string+"、"+suggestion}}</li>
             <br>
        {% endfor %}
        </ul>
    </div>
</div>
'''

# 总检审核签字、电子章
html_second_page_sign ='''
<div class="page_2">
<%
zjys = sign['zjys'] 
shys = sign['shys'] 
describe = sign['describe'] 
%>
    <br>
    <table class="sign">
    <tr align="right">
    <td>总检医生：${zjys}</td>
    </tr>
    <tr><td></td></tr>
    <tr align="right">
    <td>审核医生：${shys}</td>
    </tr>
    <tr align="left">
    <td>${describe}</td>
    </tr>
    </table>
</div>
'''

# 项目结果
html_tj_xmjg = '''
<div class="page_2">
    <div class="tj_xj">
        <h1>体检项目结果</h1>
        <hr />
        <br>
    </div>
    <div class="tj_xj_content">
        <ul>
        <%
            zhxms = items['zhxm']
            mxxms = items['mxxm']
            jcjl = items['jcjl']
            pic = items['pic']
        %>
        % for item in zhxms.keys():
            <% 
                xmlx = jcjl[zhxms[item]]['xmlx'] 
                kslx = jcjl[zhxms[item]]['kslx']
                ksbm = jcjl[zhxms[item]]['ksbm'].strip()
                zhbh = zhxms[item]
            
            %>
            % if kslx=='2' or (kslx=='1' and ksbm in['0001','0038']):
                <table>
                <caption>${item}</caption>
                  <thead>
                    <tr height=35px>
                    <th>项目名称</th>
                    <th>检查结果</th>
                    <th>单位</th>
                    <th>参考范围</th>
                    </tr>
                  </thead>
                  <tbody>
                    % for mxxm in mxxms[zhxms[item]]:
                       % if mxxm['ycbz']=='1':
                        %   if mxxm['ycts']:
                                <tr height=35px bgcolor="#fafad2">
                                    <td>${mxxm['xmmc']}</td>
                                    <td class="table_td">${mxxm['jg']+'&nbsp;&nbsp;&nbsp;'+mxxm['ycts']}</td>
                                    <td>${mxxm['xmdw']}</td>
                                    <td>${mxxm['ckfw']}</td>              
                                </tr>
                           % else:
                                <tr height=35px bgcolor="#fafad2">
                                    <td>${mxxm['xmmc']}</td>
                                    <td class="table_td">${mxxm['jg']}</td>
                                    <td>${mxxm['xmdw']}</td>
                                    <td>${mxxm['ckfw']}</td>              
                                </tr>
                        %endif 
                      %  else:
                            <tr height=35px>
                                <td>${mxxm['xmmc']}</td>
                                <td>${mxxm['jg']}</td>
                                <td>${mxxm['xmdw']}</td>
                                <td>${mxxm['ckfw']}</td>              
                            </tr>
                     %endif
                    % endfor
                    <tr height=2px>
                        <td colspan="4">
                            <hr style="height:1px;border-top:2px solid #000;"/>
                        </td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr valign="top" height=25px;>
                        <td colspan="4">
                        <%
                            if jcjl[zhxms[item]]['shrq']:
                                jl = "检验医生：%s &nbsp;&nbsp;检验日期：%s &nbsp;&nbsp;&nbsp;&nbsp;审核医生：%s &nbsp;&nbsp;审核日期：%s" %(jcjl[zhxms[item]]['jcys'],jcjl[zhxms[item]]['jcrq'],jcjl[zhxms[item]]['shys'],jcjl[zhxms[item]]['shrq'])
                            else:
                                jl = "检查医生：%s &nbsp;&nbsp;检查日期：%s " %(jcjl[zhxms[item]]['jcys'],jcjl[zhxms[item]]['jcrq'])
                        %>
                        ${jl}
                        </td>
                    </tr>
                  </tfoot>
                </table>

            % elif kslx=='1':
                <table>
                <caption>${item}</caption>
                  <thead>
                    <tr height=35px>
                    <th>项目名称</th>
                    <th>检查结果</th>
                    <th>项目名称</th>
                    <th>检查结果</th>
                    </tr>
                  </thead>
                  <tbody>
                    % for i,mxxm in enumerate(mxxms[zhxms[item]]):
                        % if i % 2 ==0:
                            % if mxxm['ycbz']=='1':
                                <tr height=35px bgcolor="#fafad2">
                                    <td>${mxxm['xmmc']}</td>
                                    <td class="table_td">${mxxm['jg']}</td>
                            % else:
                                <tr height=35px>
                                    <td>${mxxm['xmmc']}</td>
                                    <td>${mxxm['jg']}</td>
                            % endif 
                            
                            % if len(mxxms[zhxms[item]]) % 2 ==0:
                            
                                % if mxxms[zhxms[item]][i+1]['ycbz']=='1':
                                        <td>${mxxms[zhxms[item]][i+1]['xmmc']}</td>
                                        <td class="table_td">${mxxms[zhxms[item]][i+1]['jg']}</td>
                                % else:
                                        <td>${mxxms[zhxms[item]][i+1]['xmmc']}</td>
                                        <td>${mxxms[zhxms[item]][i+1]['jg']}</td>
                                % endif 
                            % else:
                                % if i+1 < len(mxxms[zhxms[item]]):
                                    % if mxxms[zhxms[item]][i+1]['ycbz']=='1':
                                            <td>${mxxms[zhxms[item]][i+1]['xmmc']}</td>
                                            <td class="table_td">${mxxms[zhxms[item]][i+1]['jg']}</td>
                                    % else:
                                            <td>${mxxms[zhxms[item]][i+1]['xmmc']}</td>
                                            <td>${mxxms[zhxms[item]][i+1]['jg']}</td>
                                    % endif 
                                % endif
                            % endif    
                        % endif
                        </tr>
                    % endfor
                    <tr height=2px>
                        <td colspan="4">
                            <hr style="height:1px;border-top:2px solid #000;"/>
                        </td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr>
                        <td colspan="4">
                        <%
                            if jcjl[zhxms[item]]['shrq']:
                                jl = "检验医生：%s &nbsp;&nbsp;检验日期：%s &nbsp;&nbsp;&nbsp;&nbsp;审核医生：%s &nbsp;&nbsp;审核日期：%s" %(jcjl[zhxms[item]]['jcys'],jcjl[zhxms[item]]['jcrq'],jcjl[zhxms[item]]['shys'],jcjl[zhxms[item]]['shrq'])
                            else:
                                jl = "检查医生：%s &nbsp;&nbsp;检查日期：%s " %(jcjl[zhxms[item]]['jcys'],jcjl[zhxms[item]]['jcrq'])
                        %>
                        ${jl}
                        </td>
                    </tr>
                  </tfoot>
                </table>
            
            % elif kslx=='3':
                <table>
                    <caption>${item}</caption>
                    <tbody>
                    % for mxxm in mxxms[zhxms[item]]:
                        <tr>
                            <td colspan="4" class="table_td_pacs">检查所见：</td>
                        </tr>
                        <tr>
                            <td colspan="4">${mxxm['jg']}</td>
                        </tr>
                        <tr>
                            <td colspan="4" class="table_td_pacs">诊断意见：</td>
                        </tr>
                        <tr>
                            <td colspan="4">${mxxm['zd']}</td>
                        </tr>
                        % if ksbm == '0026':
                            <tr>
                                <td colspan="2" align="center"><img src=${pic[zhbh][0]} width="99%"></td>
                                <td colspan="2" align="center"><img src=${pic[zhbh][0]} width="99%"></td>
                            </tr>
                        % elif ksbm == '0020':
                            <tr>
                                <td colspan="2"><img src=${pic[zhbh][0]} width="99%"></td>
                                <td colspan="2"><img src=${pic[zhbh][1]} width="99%"></td>
                            </tr>
                        % endif
                        <tr height=5px>
                            <td colspan="4">
                                <hr style="height:1px;border-top:2px solid #000;"/>
                            </td>
                        </tr>
                    %endfor
                    </tbody>
                      <tfoot>
                        <tr>
                            <td colspan="4">
                            <%
                                if jcjl[zhxms[item]]['shrq']:
                                    jl = "检验医生：%s &nbsp;&nbsp;检验日期：%s &nbsp;&nbsp;&nbsp;&nbsp;审核医生：%s &nbsp;&nbsp;审核日期：%s" %(jcjl[zhxms[item]]['jcys'],jcjl[zhxms[item]]['jcrq'],jcjl[zhxms[item]]['shys'],jcjl[zhxms[item]]['shrq'])
                                else:
                                    jl = "检查医生：%s &nbsp;&nbsp;检查日期：%s " %(jcjl[zhxms[item]]['jcys'],jcjl[zhxms[item]]['jcrq'])
                            %>
                            ${jl}
                            </td>
                        </tr>
                      </tfoot>
                </table>
                    
            % endif 
        <br>
        % endfor
        </ul>
    
    </div>
</div>
'''

# PDF 载入 <embed src="C:/Users/Administrator/Desktop/pdf测试/165560254_04.pdf" width="1240" height="1754">


# 项目结果
html_tj_equip = '''
<div class="page_2">
    <div class="tj_xj_content">
        % for equip in equips:
            <div>
                <img src=${equip} class="image" />
            </div>
        % endfor
    </div>
</div>
'''

# 项目结果
html_tj_health_care = '''
<div class="page_2">
    <%
        health_title = healths['title']
        health_body = healths['body']
    %>
    <div class="tj_xj">
        <h1>${health_title['title']}</h1>
        <hr />
    </div>
    <div class="tj_xj_content">
        <table>
        <tr><td></td></tr>
        </table>
    </div>
</div>
'''
