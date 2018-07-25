import time
import pyautogui,pyperclip

# 心电图 根据坐标录入
def autoInputXDT(patient,pos):
    # ----------------------获取位置----------------------------------
    pos_add = pos.get('position_tj', [])
    pos_tjbh = pos.get('position_tjbh', [])
    pos_xm = pos.get('position_xm', [])
    pos_xb_m = pos.get('position_xb1', [])
    pos_xb_f = pos.get('position_xb2', [])
    pos_nl = pos.get('position_nl', [])
    pos_sure = pos.get('position_sure', [])
    pos_gx = pos.get('position_gx', [])
    pos_cj = pos.get('position_cj', [])
    # ---------------------获取人员信息--------------------------
    p_tjbh = patient.get('tjbh','000000000')
    p_xm = patient.get('xm', '000')
    p_xb = patient.get('xb', '男')
    p_nl = patient.get('nl', '0')
    # ---------------------录入顺序--------------------------
    # 打开添加按钮
    paste(pos_add, "添加按钮", 1)
    # 录入体检编号
    paste(pos_tjbh, p_tjbh, 2)
    # 录入姓名
    paste(pos_xm, p_xm, 2)
    # 录入性别
    if p_xb == '男':
        paste(pos_xb_m, "性别按钮", 1)
    elif p_xb == '女':
        paste(pos_xb_f, "性别按钮", 1)
    else:
        pass
    # 录入年龄
    paste(pos_nl, p_nl, 3)
    paste(pos_sure, "确定按钮", 4)
    paste(pos_gx, "勾选病人", 1)
    paste(pos_cj, "采集按钮", 1)


def get_position(position_dict,key):
    values=position_dict.get(key,False)
    if values:
        if "," in values:
            return values.split(",")
        elif "，" in values:
            return values.split("，")
        else:
            return []
    else:
        return []

def get_position2(values):
    if values:
        if "," in values:
            return values.split(",")
        elif "，" in values:
            return values.split("，")
        else:
            return []
    else:
        return []

def paste(position,context,flag=1):
    time.sleep(0.05)
    if position:
        if len(position)>=2:
            if flag==1:
                pyautogui.click(int(position[0]), int(position[1]),1)
                print("%s 打开成功！" %context)
            elif flag==2:
                #复制文本
                pyautogui.click(int(position[0]), int(position[1]))
                pyperclip.copy(context)
                pyautogui.hotkey('ctrl', 'v')
                print("%s 粘贴成功！" % context)
            elif flag==3:
                #键盘输入
                pyautogui.click(int(position[0]), int(position[1]))
                pyautogui.typewrite(context)
                print("%s 输入成功！" % context)
            elif flag==4:
                pyautogui.click(int(position[0]), int(position[1]))
                print("%s 打开成功！" % context)
            else:
                print("未开放的类型！")
        else:
            print("%s：指定坐标位置没有X,Y")

    else:
        print("%s：指定坐标位置没有X,Y")