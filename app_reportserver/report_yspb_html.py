# 示例：
# '''
#             <br>国际保健中心开通VIP专家门诊，预约电话:0574-83009619。
#             <br>周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;呼吸内科主任：纪成
#             <br>周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内一科主任：董勤勇
#             <br>周三下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;妇科主任：李宁宁
#             <br>周五下午:15:30-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内二科主任：吴汉平
#             <br>
# '''

pdf_html_yspb_page ='''
<div align="center">
    <div class="page_1">
        <div style="text-align:center;">
            <div class="tj_pb">
                <br>国际保健中心开通VIP专家门诊，预约电话:0574-83009619。
                <% datas = pbxx %>
                % for data in datas:
                    <br>${data}
                % endfor
                <br>
            </div>
        </div>
    </div>

'''

