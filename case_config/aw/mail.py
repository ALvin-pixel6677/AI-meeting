from assembly_base.action_statement.send_notes import Mail

# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
mail_list = "wufeilong"
cc_list = "lvqi,zhaozhilei"


class Mail_Pc(Mail):
    def __init__(self):
        super().__init__()
        self.smtp_server = 'smtp.163.com'
        self.sender = 'grepublic2021@163.com'
        self.accont = 'grepublic2021@163.com'
        self.password = 'UIZBZWWCLSQSGSUU'
        self.mail_domain = '@honor.com'

    def mail_send(self, product, html, files):
        self.send(mailto_list=mail_list, cc_list=cc_list, title="{}游戏测试报告".format(product), content=html,
                  attachment_file=files)
