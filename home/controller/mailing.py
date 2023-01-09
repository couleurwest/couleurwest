import ssl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dreamtools.cfgmng import CFGBases
from dreamtools.mailbot import CMailer

from home.controller.jarvis import CJarvis


class CMailing(CMailer):
    header = CFGBases.mailing_lib('header')

    @classmethod
    def send_mail(cls, subject, receivers, d_msg, to_receiver=None):
        """ Envoie du mail

        :param subject: Sujet du mail
        :param receivers: email destinataire
        :param d_msg: Message
        :param to_receiver: Nom destinataire
        :return:
        """
        CJarvis.flag("[dreamtools.mailbot] SEND_MAIL : Parametrage smtp")
        context = ssl.create_default_context()

        CJarvis.flag("[dreamtools.mailbot] SEND_MAIL:Parametrage message MIME")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = cls.SMTP_USERNAME
        message["To"] = to_receiver or receivers

        CJarvis.flag("[dreamtools.mailbot] SEND_MAIL:Parametrage contenu mail")
        content = cls.header['text'] + d_msg.get('text') + cls.footers['text']
        content = MIMEText(content)
        message.attach(content)

        if d_msg.get('html'):
            content = cls.header['html'] + d_msg.get('html') + cls.footers['html']
            content = MIMEText(content, "html")
            message.attach(content)

        CJarvis.flag("[dreamtools.mailbot] SEND_MAIL:Coonnexion SMTP")
        try:
            with smtplib.SMTP_SSL(cls.SMTP_HOST, cls.SMTP_PORT, context=context) as server:
                CJarvis.flag("[dreamtools.mailbot] SEND_MAIL:Authentification")
                server.login(cls.SMTP_AUTHMAIL, cls.SMTP_AUTHPWD)
                CJarvis.flag("[dreamtools.mailbot] SEND_MAIL: Sending")
                server.sendmail(cls.SMTP_AUTHMAIL, receivers, message.as_string())

                return True
        except Exception as ex:
            return CJarvis.exception_tracking(ex,"[dreamtools.mailbot] SEND_MAIL")


    @classmethod
    def send_code(cls, actors_email, code, link):
        return cls.presend(actors_email, "send_code", code_verification=code, link=link)

    @classmethod
    def send_code_enketo(cls, actors_email, code, title, link, code_enketo, name_enketo):
        return cls.presend(actors_email, "send_code_enketo", enketo_auth=code,
                           enketo_code=code_enketo, enketo_title=title, enketo_name=name_enketo,
                           link=link)

    @classmethod
    def send_action(cls, paraph, actors_name, actors_email, order, echeance, link):
        return cls.presend(actors_email, "send_action", name=actors_name, paraph=paraph, order=order,
                                echeance=echeance, link=link)

    @classmethod
    def send_comment(cls, paraph, actors_name, actors_email, comment_title, link):
        return CMailing.presend(actors_email, "send_comment", name=actors_name, paraph=paraph,
                                comment_title=comment_title, link=link)

    @classmethod
    def send_alert(cls, actors_name, actors_email, **features):
        return CMailing.presend(actors_email, "send_alert", name=actors_name, **features)

    @classmethod
    def send_inps_request(cls, actors_name, actors_email, **features):
        return CMailing.presend(actors_email, "send_inps_request", name=actors_name, **features)
