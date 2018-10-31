# 示例：
# '''
#             <br>国际保健中心开通VIP专家门诊，预约电话:0574-83009619。
#             <br>周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;呼吸内科主任：纪成
#             <br>周一下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内一科主任：董勤勇
#             <br>周三下午:14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;妇科主任：李宁宁
#             <br>周五下午:15:30-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内二科主任：吴汉平
#             <br>
# '''

pdf_html_yspb_page='''
<div align="center">
    <div class="page_1">
        <div class="tj_xj">
            <h3>VIP专家门诊</h3>
            <hr />
        </div>
        <div align="center">
            <table class="table_pb">
                <col style="width: 20%" />
                <col style="width: 20%" />
                <col style="width: 20%" />
                <col style="width: 20%" />
                <col style="width: 20%" />
                <tr class="tr_pb">
                    <td colspan="2" class="td_pb">日　　期</td>
                    <td class="td_pb">科　　室</td>
                    <td class="td_pb">专　家</td>
                    <td class="td_pb">职称</td>
                </tr>
                <tr class="tr_pb">
                    <td rowspan="2" class="td_pb2">星期一　下午</td>
                    <td class="td_pb2">14:00-16:00</td>
                    <td class="td_pb">呼吸内科</td>
                    <td class="td_pb">纪　成</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb">
                    <td class="td_pb2">15:00-16:00</td>
                    <td class="td_pb">消化内科</td>
                    <td class="td_pb">董勤勇</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb">
                    <td class="td_pb2">星期二　下午</td>
                    <td class="td_pb2">14:00-16:00</td>
                    <td class="td_pb">心&nbsp;&nbsp;内&nbsp;&nbsp;科</td>
                    <td class="td_pb">吴海宏</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb">
                    <td rowspan="2"  class="td_pb2">星期三　下午</td>
                    <td class="td_pb2">14:00-16:00</td>
                    <td class="td_pb">妇　　科</td>
                    <td class="td_pb">李宁宁</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb">
                    <td class="td_pb2">15:00-16:00</td>
                    <td class="td_pb">肝&nbsp;&nbsp;病&nbsp;&nbsp;科</td>
                    <td class="td_pb">徐长风</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb">
                    <td class="td_pb2">星期四　下午</td>
                    <td class="td_pb2">14:00-16:00</td>
                    <td class="td_pb">泌尿外科</td>
                    <td class="td_pb">温海涛</td>
                    <td class="td_pb">院长</td>
                </tr>
                <tr class="tr_pb">
                    <td rowspan="2" class="td_pb2">星期五　下午</td>
                    <td class="td_pb2">14:00-16:00</td>
                    <td class="td_pb">心胸外科</td>
                    <td class="td_pb">周耀洪</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb">
                    <td class="td_pb2">15:30-16:00</td>
                    <td class="td_pb">消化内科</td>
                    <td class="td_pb">吴汉平</td>
                    <td class="td_pb">主任</td>
                </tr>
                <tr class="tr_pb2">
                    <td colspan="5">
                    预约电话：0574-8300-9006
                    </td>
                </tr>
            </table>
        </div>
    </div>

'''

# 手工版本
pdf_html_yspb_page_old ='''
<div align="center">
    <div class="page_1">
        <div style="text-align:center;">
            <div class="tj_pb">
                <br>国际保健中心开通VIP专家门诊&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;预约电话：0574-8300-9006
                <br>星期一下午：14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;呼吸内科：纪成主任
                <br>星期一下午：15:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内科：董勤勇主任
                <br>星期二下午：14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;心&nbsp;内&nbsp;科：吴海宏主任
                <br>星期三下午：14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;妇&nbsp;&nbsp;&nbsp;&nbsp;科：李宁宁主任
                <br>星期三下午：14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;肝&nbsp;病&nbsp;科：徐长风主任
                <br>星期四下午：14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;泌尿外科：温海涛院长
                <br>星期五下午：14:00-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;心胸外科：周耀洪主任
                <br>星期五下午：15:30-16:00&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;消化内科：吴汉平主任
                <br>
            </div>
        </div>
    </div>

'''

# 最新要改
pdf_html_yspb_page2 ='''
    <div class="page_1">
        <div style="text-align:center;">
            <div class="tj_pb">
                <br>国际保健中心开通VIP专家门诊  预约电话:0574-8300-9006
                <table class="user_table">
                    <% datas = pbxx %>
                    % for data in datas:
                        <tr>
                            <td>${data['pbsj']}</td>
                            <td>${data['pbys']}</td>
                        </tr>
                    % endfor
                    <br>
                </table>
            </div>

'''

# 历史版本
pdf_html_yspb_page3 ='''
<div align="center">
    <div class="page_1">
        <div style="text-align:center;">
            <div class="tj_pb">
                <br>国际保健中心开通VIP专家门诊  预约电话:0574-8300-9006
                <% datas = pbxx %>
                % for data in datas:
                    <br>${data}
                % endfor
                <br>
            </div>
        </div>
    </div>

'''