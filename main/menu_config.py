from collections import OrderedDict

#对象树,菜单栏->菜单->界面->按钮
#每个对象都有唯一ID、唯一父ID、不定子ID，标题title，提示tip，状态status,
SYS_MENU_TREE = {   # 系统
    'pid':None,
    'sid':1,
    'title':'体检系统',
    'tip':None,
    'state':True,
    'childs':OrderedDict([  # 菜单栏
        # 系统架构维护
        ('系统管理',
         {
            'pid':1,
            'sid':100,
            'title':'系统管理',
            'tip':None,
            'state':True,
            'childs':OrderedDict([  # 菜单
                ('用户管理',{'pid':100,'sid':1001,'title':'用户管理','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('角色权限',{'pid':100,'sid':1002,'title':'角色权限','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('密码修改',{'pid':100,'sid':1003,'title':'密码修改','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('系统日志',{'pid':100,'sid':1004,'title':'系统日志','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('系统参数',{'pid':100,'sid':1004,'title':'系统参数','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('代码字典',{'pid':100,'sid':1005,'title':'代码字典','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('版本控制',{'pid':100,'sid':1006,'title':'版本控制','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('界面设计',{'pid':100,'sid':1007,'title':'界面设计','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('注    销',{'pid':100,'sid':1007,'title':' 注  销 ','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('退    出',{'pid':100,'sid':1008,'title':' 退  出 ','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None})
            ])
         }),
        # 基础资料维护
        ('基础资料',
         {
             'pid': 1,
             'sid': 200,
             'title': '基础维护',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                  # ('体检项目',{'pid': 200, 'id': 2001, 'title': '体检项目', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('体检套餐',{'pid': 200, 'id': 2002, 'title': '体检套餐', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('体检项目类别',{'pid': 200, 'id': 2003, 'title': '体检项目类别', 'tip': None, 'state': True, 'icon':'','is_tool':False,'class':None,'childs': None}),
                  # ('导检单项目',{'pid': 200, 'id': 2004, 'title': '导检单项目', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('导检单',{'pid': 200, 'id': 2005, 'title': '导检单', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('员工信息',{'pid': 200, 'id': 2006, 'title': '员工信息', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('体检科室',{'pid': 200, 'id': 2007, 'title': '体检科室', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('发票号码',{'pid': 200, 'id': 2008, 'title': '发票号码', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None})

            ])
         }),
        # 外围系统 WEB、app、微信、电话、短信、HIS、LIS、PACS
        ('接口管理',
         {
             'pid': 1,
             'sid': 300,
             'title': '接口管理',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                  #     ('HIS收费项目对照',
                  #      {'pid': 400, 'id': 4001, 'title': 'HIS收费项目对照', 'tip': None, 'state': True, 'icon': '',
                  #       'is_tool': False, 'class': None, 'childs': None}),
                  #     ('LIS检验项目对照',
                  #      {'pid': 400, 'id': 4002, 'title': 'LIS检验项目对照', 'tip': None, 'state': True, 'icon': '',
                  #       'is_tool': False, 'class': None, 'childs': None}),
                  #     ('PACS项目对照', {'pid': 400, 'id': 4003, 'title': 'PACS项目对照', 'tip': None, 'state': True, 'icon': '',
                  #                   'is_tool': False, 'class': None, 'childs': None}),
                  #     ('HIS接口',
                  #      {'pid': 400, 'id': 4004, 'title': 'HIS接口', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,
                  #       'class': None, 'childs': None}),
                  #     ('LIS接口',
                  #      {'pid': 400, 'id': 4005, 'title': 'LIS接口', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,
                  #       'class': None, 'childs': None}),
                  #     ('PACS接口', {'pid': 400, 'id': 4006, 'title': 'PACS接口', 'tip': None, 'state': True, 'icon': '',
                  #                 'is_tool': False, 'class': None, 'childs': None}),
                  #     ('设备接口',
                  #      {'pid': 400, 'id': 4007, 'title': '设备接口', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,
                  #       'class': None, 'childs': None})
                  ])}),
        # 体检检中管理
        ('检中管理',
         {
             'pid': 1,
             'sid': 400,
             'title': '检中管理',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
             # ('体检预约',{'pid': 300, 'sid': 3001, 'title': '体检预约', 'tip': None, 'state': True, 'icon':'预约','is_tool':True,'shortcut':None}),
             # ('体检登记',{'pid': 300, 'sid': 3002, 'title': '体检登记', 'tip': None, 'state': True, 'icon':'登记','is_tool':True,'shortcut':None}),
             # ('体检收费',{'pid': 300, 'sid': 3003, 'title': '体检收费', 'tip': None, 'state': True, 'icon':'收费','is_tool':True,'shortcut':None}),
             ('结果录入',{'pid': 400, 'sid': 4004, 'title': '结果录入', 'tip': None, 'state': True, 'icon':'结果录入','is_tool':True,'shortcut':None}),
             # ('医生总检',{'pid': 300, 'sid': 3005, 'title': '医生总检', 'tip': None, 'state': True, 'icon':'预约','is_tool':True,'shortcut':None}),
             # ('智能导检',{'pid': 300, 'sid': 3006, 'title': '智能导检', 'tip': None, 'state': False, 'icon':'导检','is_tool':True,'shortcut':None}),
             # ('短信平台',{'pid': 300, 'sid': 3007, 'title': '短信平台', 'tip': None, 'state': False, 'icon':'短信','is_tool':True,'shortcut':None})
                ('采血留样',{'pid': 400, 'sid': 4008, 'title': '采血台', 'tip': None, 'state': True, 'icon':'采血台','is_tool':True,'shortcut':None}),
                ('呼气试验',{'pid': 400, 'sid': 4009, 'title': '呼气室', 'tip': None, 'state': True, 'icon':'呼气室','is_tool':True,'shortcut':None}),
            ])}),
        # 体检检后管理
        ('检后管理',
         {
             'pid': 1,
             'sid': 500,
             'title': '检后管理',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                ('报告中心',{'pid': 500, 'sid': 5001, 'title': '报告中心', 'tip': None, 'state': True, 'icon':'报告中心','is_tool':True,'shortcut':None}),
                ('慢病管理',{'pid': 500, 'sid': 5002, 'title': '慢病管理', 'tip': None, 'state': True, 'icon':'慢病管理','is_tool':True,'shortcut':None}),
            ])}),
        # 管理人员 用到的
        ('主任平台',
         {
             'pid': 1,
             'sid': 600,
             'title': '主任平台',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                 ('医护绩效',{'pid': 600, 'sid': 6001, 'title': '医护绩效', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
             # ('科室工作量',{'pid': 500, 'id': 5002, 'title': '科室工作量', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
             # ('工作效率统计',{'pid': 500, 'id': 5003, 'title': '工作效率统计', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
             # ('日签到统计',{'pid': 500, 'id': 5004, 'title': '日签到统计', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
             # ('预约明细',{'pid': 500, 'id': 5005, 'title': '预约明细', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None})
            ])}),
        # 自带财务模块
        ('财务管理',
         {
             'pid': 1,
             'sid': 700,
             'title': '经营',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
             # ('用户管理',{'pid': 600, 'id': 6001, 'title': '用户管理', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('权限管理',{'pid': 600, 'id': 6002, 'title': '权限管理', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('密码修改',{'pid': 600, 'id': 6003, 'title': '密码修改', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('系统参数',{'pid': 600, 'id': 6004, 'title': '系统参数', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('系统字典',{'pid': 600, 'id': 6005, 'title': '系统字典', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('系统版本',{'pid': 600, 'id': 6006, 'title': '系统版本', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('注销',{'pid': 600, 'id': 6007, 'title': '注销', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
             # ('退出',{'pid': 600, 'id': 6008, 'title': '退出', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None})
            ])}),
        # 数据统计 对所有人开放
        ('查询统计',
         {
             'pid': 1,
             'sid': 800,
             'title': '查询统计',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                 ('检查结果',{'pid': 800, 'sid': 8001, 'title': '检查结果', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,'shortcut':None})
            ])})
    ])
}
# 系统菜单模块对象
SYS_MENU_MODULE_CLASS = {
    1001: {'module': None, 'class': None, 'enabled': False},
    1002: {'module': None, 'class': None, 'enabled': False},
    1003: {'module': None, 'class': None, 'enabled': False},
    1004: {'module': None, 'class': None, 'enabled': False},
    1005: {'module': None, 'class': None, 'enabled': False},
    1006: {'module': None, 'class': None, 'enabled': False},
    1007: {'module': None, 'class': None, 'enabled': False},
    1008: {'module': None, 'class': None, 'enabled': False},
    2001: {'module': None, 'class': None, 'enabled': False},
    2002: {'module': None, 'class': None, 'enabled': False},
    2003: {'module': None, 'class': None, 'enabled': False},
    2004: {'module': None, 'class': None, 'enabled': False},
    2005: {'module': None, 'class': None, 'enabled': False},
    2006: {'module': None, 'class': None, 'enabled': False},
    2007: {'module': None, 'class': None, 'enabled': False},
    2008: {'module': None, 'class': None, 'enabled': False},
    3001: {'module': None, 'class': None, 'enabled': False},
    3002: {'module': None, 'class': None, 'enabled': False},
    3003: {'module': None, 'class': None, 'enabled': False},
    3004: {'module': None, 'class': None, 'enabled': False},
    3005: {'module': None, 'class': None, 'enabled': False},
    3006: {'module': None, 'class': None, 'enabled': False},
    3007: {'module': None, 'class': None, 'enabled': False},
    3008: {'module': None, 'class': None, 'enabled': False},
    4001: {'module': None, 'class': None, 'enabled': False},
    4002: {'module': None, 'class': None, 'enabled': False},
    4003: {'module': None, 'class': None, 'enabled': False},
    4004: {'module': 'result', 'class': 'ResultManager', 'enabled': True},
    4005: {'module': None, 'class': None, 'enabled': False},
    4006: {'module': None, 'class': None, 'enabled': False},
    4007: {'module': None, 'class': None, 'enabled': False},
    4008: {'module': 'lis', 'class': 'SampleManager', 'enabled': True},       # 采血台
    4009: {'module': 'C13', 'class': 'BreathManager', 'enabled': True},    # 呼气室
    5001: {'module': 'report', 'class': 'ReportManager', 'enabled': True},    # 报告中心
    5002: {'module': 'mbgl', 'class': 'NCDManager', 'enabled': True},                  # 慢病管理
    5003: {'module': None, 'class': None, 'enabled': False},
    5004: {'module': None, 'class': None, 'enabled': False},
    5005: {'module': None, 'class': None, 'enabled': False},
    5006: {'module': None, 'class': None, 'enabled': False},
    5007: {'module': None, 'class': None, 'enabled': False},
    5008: {'module': None, 'class': None, 'enabled': False},
    6001: {'module':'datastatistics.meritpay', 'class':'DN_MeritPay', 'enabled': True}, #医护绩效
    6002: {'module': None, 'class': None, 'enabled': False},
    6003: {'module': None, 'class': None, 'enabled': False},
    6004: {'module': None, 'class': None, 'enabled': False},
    6005: {'module': None, 'class': None, 'enabled': False},
    6006: {'module': None, 'class': None, 'enabled': False},
    6007: {'module': None, 'class': None, 'enabled': False},
    6008: {'module': None, 'class': None, 'enabled': False},
    7001: {'module': None, 'class': None, 'enabled': False},
    7002: {'module': None, 'class': None, 'enabled': False},
    7003: {'module': None, 'class': None, 'enabled': False},
    7004: {'module': None, 'class': None, 'enabled': False},
    7005: {'module': None, 'class': None, 'enabled': False},
    7006: {'module': None, 'class': None, 'enabled': False},
    7007: {'module': None, 'class': None, 'enabled': False},
    7008: {'module': None, 'class': None, 'enabled': False},
    8001: {'module': None, 'class': None, 'enabled': False},
    8002: {'module': None, 'class': None, 'enabled': False},
    8003: {'module': None, 'class': None, 'enabled': False},
    8004: {'module': None, 'class': None, 'enabled': False},
    8005: {'module': None, 'class': None, 'enabled': False},
    8006: {'module': None, 'class': None, 'enabled': False},
    8007: {'module': None, 'class': None, 'enabled': False},
    8008: {'module': None, 'class': None, 'enabled': False}
}