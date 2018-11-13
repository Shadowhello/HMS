import zmail


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
server = zmail.server(
    user='772441084@qq.com',
    password='22215957343015',
    # smtp_host='smtp.163.com',
    # smtp_port=994,
    # smtp_ssl=True,
    # pop_host='pop.163.com',
    # pop_port=995,
    # pop_ssl=True
)

# 发送邮件
server.send_mail('245938515@qq.com', mail_content)