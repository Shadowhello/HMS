# 设备项目

pdf_html_equip_page = '''
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