# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/9 12:59
# @Description   : 邮件工具箱
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple, Union, List, Dict, Any, Optional

from jinja2 import Environment, PackageLoader, select_autoescape

from stardew.settings import settings
from stardew.common.constants import Constant


class EmailUtil:

    """ 邮件工具集 """

    env = Environment(loader=PackageLoader("stardew"), autoescape=select_autoescape())

    @staticmethod
    def send_mail(
        *,
        subject: str,
        html_content: str,
        receivers: Union[Tuple, List],
        sender_alias: Optional[str] = None
    ) -> None:
        """
        发送邮件。邮件应当使用Jinja2模板进行渲染。
        :param sender_alias: 发送者昵称
        :param receivers: 接收者
        :param subject: 邮件主题
        :param html_content: 已经渲染好的html文本
        :return:
        """

        mm = MIMEMultipart()

        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        mm["From"] = f"{sender_alias}<{settings.EMAIL_FROM_NAME}>" if sender_alias else settings.EMAIL_SENDER
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        mm["To"] = ",".join([f"<{receiver}>" for receiver in receivers])
        # 设置邮件主题
        mm["Subject"] = Header(subject, Constant.UTF8)

        # 构造邮件文本
        message_text = MIMEText(_text=html_content, _subtype="html", _charset=Constant.UTF8)
        # 向MIMEMultipart对象中添加文本对象
        mm.attach(message_text)

        # 创建SMTP对象，使用SSL加密
        if settings.SMTP_TLS:
            stp = smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT)
        else:
            stp = smtplib.SMTP(host=settings.SMTP_HOST, port=settings.SMTP_PORT)
        stp.set_debuglevel(1)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        stp.login(settings.EMAIL_SENDER, settings.SMTP_LICENCE)
        # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：内容转纯字符串
        stp.sendmail(settings.EMAIL_SENDER, receivers, mm.as_string())
        # 关闭SMTP对象
        stp.quit()

    @classmethod
    def render_template(cls, template_name, content: Dict[str, Any]) -> str:
        """
        渲染html模板，用于邮件正文部分的构建
        :param template_name: 模板名称
        :param content: 邮件正文内容
        :return:
        """
        template = cls.env.get_template(template_name)
        return template.render(**content)