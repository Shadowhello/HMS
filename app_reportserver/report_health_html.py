# 保健处方

pdf_html_health_page = '''
<div class="page_2">
    <%
        health_title = health['title']
        health_stitle = health['stitle']
        health_body = health['body']
    %>
    <div class="tj_xj">
        <h1 class="bkcf_stitle">${health_title}</h1>
        <div class ="bkcf_sstitle">${health_stitle}</div>
    </div>
    <div class="tj_xj_content">
        % for title,content in health_body.items():
            <li><b>${title}</b></li>
            ${content}
        % endfor
    </div>
</div>
'''