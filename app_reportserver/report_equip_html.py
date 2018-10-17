# 设备项目

pdf_html_equip_page = '''
<div class="new_page">
        % for equip in equips:
            <div>
                <img src=${equip} class="image" />
            </div>
        % endfor
</div>
'''