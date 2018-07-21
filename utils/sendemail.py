from zmail import server

# 你的邮件内容
mail_content = {
    'subject':'Success!',
    'content':'This message from zmail!',
    'attachments': 'D://145400144.pdf',
}

# 使用你的邮件账户名和密码登录服务器
qq_server = server(user='772441084@qq.com',password='22215957343015')
# 发送邮件
qq_server.send_mail('245938515@qq.com', mail_content)