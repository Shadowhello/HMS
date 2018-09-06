# 小结
pdf_html_summary_page = '''
<div class="page_2">
    <div class="tj_xj">
        <h1>体检小结(Summary)</h1>
        <hr />
    </div>
    <div class="tj_xj_content">
        <ul>
            {% for summary in summarys %}
             <li class="tj_xj_li">{{loop.index|string+"、"+summary}}</li>
        {% endfor %}
        </ul>
        <br />
    </div>
</div>
'''


# 建议
pdf_html_suggest_page = '''
<div class="page_2">
    <div class="tj_xj">
        <h1>体检建议(Suggestions)</h1>
        <hr />
    </div>
    <div class="tj_jy_content">
        <ul>
            {% for suggestion in suggestions %}
             <li class="tj_xj_li">{{loop.index|string+"、"+suggestion}}</li>
        {% endfor %}
        </ul>
        <br />
    </div>
</div>
'''

# 总检审核签字、电子章
pdf_html_cachet_page ='''
<div class="page_2">
    <%
        zjys = cachet['zjys'] 
        shys = cachet['shys'] 
        syys = cachet['syys'] 
        warn = cachet['warn'] 
    %>
    <br>
    <table class="cachet">
        <tr>
            <td></td>
        </tr>
        <tr align="right">
            <td>总检医生：<img src=${zjys} height="50" width="100" /></td>
        </tr>
        <tr align="right">
            <td>审核医生：<img src=${shys} height="50" width="100" /></td>
        </tr>
        <tr align="left">
            <td>${warn}</td>
        </tr>
    </table>
</div>
'''

# 总检审核签字、电子章
pdf_html_cachet_page2 ='''
<div class="page_2">
    <%
        zjys = cachet['zjys'] 
        shys = cachet['shys'] 
        syys = cachet['syys'] 
        warn = cachet['warn'] 
    %>
    <br>
    <table class="cachet">
        <tr>
            <td></td>
        </tr>
        <tr align="right">
            <td>总检医生：<img src=${zjys} height="50" width="100" /></td>
        </tr>
        <tr align="right">
            <td>审核医生：<img src=${shys} height="50" width="100" /></td>
        </tr>
        <tr align="right">
            <td>三审护士：<img src=${syys} height="50" width="100" /></td>
        </tr>
        <tr align="left">
            <td>${warn}</td>
        </tr>
    </table>
</div>
'''

warn = '''
说明:<br />
1.你过去患的疾病，因这次体检范围所限未能发现的情况，仍按原诊断及治疗。<br />
2.查出的疾病请及时治疗,异常项目请到医院复查。<br />
3.尽管我们会尽最大的努力，但因为医学的局限性和检查方式不同，有些疾病仍难以发现。<br />
4.请详细阅读各项检查结果，如与总检结论不符或有疑惑，请及时与总检医生联系，联系电话:0574-83009689。<br />
5.宁波明州医院国际保健中心总台联系电话:0574-83009619。<br />
'''