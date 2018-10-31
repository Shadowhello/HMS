# 项目结果
pdf_html_item_page = '''
<div class="new_page">
    <div class="tj_xj">
        <h3>体检项目结果</h3>
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
                                <tr height=35px>
                                    <td>${mxxm['xmmc']}</td>
                                    <td class="table_td">${mxxm['jg']+'&nbsp;&nbsp;&nbsp;'+mxxm['ycts']}</td>
                                    <td>${mxxm['xmdw']}</td>
                                    <td>${mxxm['ckfw']}</td>              
                                </tr>
                           % else:
                                <tr height=35px>
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
                                <tr height=35px>
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
                            % if pic.get(zhbh,[]):
                                % if len(pic[zhbh])>=2:
                                    <tr>
                                        <td colspan="2" align="center"><img src=${pic[zhbh][0]} width="99%"></td>
                                        <td colspan="2" align="center"><img src=${pic[zhbh][1]} width="99%"></td>
                                    </tr>
                                % else:
                                    <tr>
                                        <td colspan="4" align="left"><img src=${pic[zhbh][0]} width="49%"></td>
                                    </tr>   
                                % endif 
                            % endif
                        % elif ksbm == '0020':
                            % if pic.get(zhbh,[]):
                                % if len(pic[zhbh])>=2:
                                    <tr>
                                        <td colspan="2"><img src=${pic[zhbh][0]} width="99%"></td>
                                        <td colspan="2"><img src=${pic[zhbh][1]} width="99%"></td>
                                    </tr>
                                % else:
                                    <tr>
                                        <td colspan="4" align="left"><img src=${pic[zhbh][0]} width="49%"></td>
                                    </tr>   
                                % endif                                 
                            % endif
                        % elif ksbm == '0024':
                            % if pic.get(zhbh,[]):
                                % if len(pic.get(zhbh,[])) % 2 ==0:
                                    % for i in range(len(pic.get(zhbh,[])) // 2):
                                        <tr>
                                            <td colspan="2" align="center"><img src=${pic.get(zhbh,[])[i]} width="99%"></td>
                                            <td colspan="2" align="center"><img src=${pic.get(zhbh,[])[i+1]} width="99%"></td>
                                        </tr>
                                    %endfor
                                % else :
                                    % for i in range(len(pic.get(zhbh,[]))-1 // 2):
                                        <tr>
                                            <td colspan="2" align="center"><img src=${pic.get(zhbh,[])[i]} width="99%"></td>
                                            <td colspan="2" align="center"><img src=${pic.get(zhbh,[])[i+1]} width="99%"></td>
                                        </tr>
                                    %endfor
                                % endif
                            % endif
                        % endif
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