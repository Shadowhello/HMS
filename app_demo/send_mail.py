import zmail
server = zmail.server('772441084@qq.com', '22215957343015')

# if server.smtp_able():
#     pass
#     print('SMTP function')
#     # SMTP function.
# if server.pop_able():
#     pass
#     print('POP function')
#     # POP function


# 你的邮件内容
mail_content = {
    'subject': 'Success!',  # 随便填写

    'content': 'This message from zmail!',  # 随便填写

    'attachments': r'C:\Users\Administrator\Desktop\pdf测试\149520265_08.pdf',  # 最好使用绝对路径，若你电脑没有这个文件会造成错
}

