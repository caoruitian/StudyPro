# coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from common import config,logger


class Mail:
    """
        powered by Mr Will
        at 2018-12-22
        用来获取配置并发送邮件
    """
    def __init__(self):
        self.mail_info = {}

        self.mail_info['from'] = config.config['mail']#发件人
        self.mail_info['username'] = config.config['mail']#发件人
        self.mail_info['hostname'] = 'smtp.' + config.config['mail'][config.config['mail'].rfind('@') + 1:config.config['mail'].__len__()]#smtp服务器域名       self.mail_info['password'] = config.config['pwd']
        self.mail_info['password'] = config.config['pwd']#SMTP服务授权码，需短信验证获取
        self.mail_info['to'] = str(config.config['mailto']).split(',')#收件人
        self.mail_info['cc'] = str(config.config['mailcopy']).split(',')#抄送人
        self.mail_info['mail_subject'] = config.config['mailtitle']#邮件标题
        self.mail_info['mail_encoding'] = config.config['mail_encoding']#设置发送内容的编码格式

    def send(self, text):
        # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587（smtp = SMTP_SSL(self.mail_info['hostname'],port=587)）
        smtp = SMTP_SSL(self.mail_info['hostname'])
        smtp.set_debuglevel(0)#1显示调试信息，0不显示

        ''' SMTP 'ehlo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        '''
        smtp.ehlo(self.mail_info['hostname'])#设置smtp地址
        smtp.login(self.mail_info['username'], self.mail_info['password'])#登陆发件人的邮件

        msg = MIMEText(text, 'html', self.mail_info['mail_encoding'])#邮件正文，'html'就是发送网页，'text'就是发送文本
        msg['Subject'] = Header(self.mail_info['mail_subject'], self.mail_info['mail_encoding'])#设置标题为config.config['mailtitle']和设置标题的编码格式
        msg['from'] = self.mail_info['from']#发件人

        logger.debug(self.mail_info)
        logger.debug(text)
        #注意，收件人和抄送人要设置成字符串然后保存到recieve里面
        msg['to'] = ','.join(self.mail_info['to'])
        msg['cc'] = ','.join(self.mail_info['cc'])
        receive = self.mail_info['to']
        receive += self.mail_info['cc']

        try:
            smtp.sendmail(self.mail_info['from'], receive, msg.as_string())#msg.as_string()指收件人和抄送人
            smtp.quit()
            logger.info('邮件发送成功')
        except Exception as e:
            logger.error('邮件发送失败：')
            logger.exception(e)


# if __name__ == '__main__':
#     config.get_config('../lib/conf/conf.txt')
#     mail = Mail()
#     mail.send(config.config['mailtext'])
