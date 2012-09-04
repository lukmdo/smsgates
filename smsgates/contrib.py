"""
Implements ``SMSGates`` using a simple and common framework

All SmsGates should implement three methods:

- setup
- send
- close

@todo: Consider adding generic class SMSGate that would encapsulate GateFactory
"""

import os
import tempfile
import twill.errors
import twill.commands as web
from smsgates import BaseFactory
from smsgates import AbstractSMSGate


class GateFactory(BaseFactory):
    @property
    def _choices(self):
        return {
            'vodafone.ie': VodafoneGate,
            'orange.pl': OrangeGate,
            'twilio.com': TwilioGate}

    @classmethod
    def get_class(cls, name=None):
        return cls()._choices[name.lower()]


class OrangeGate(AbstractSMSGate):
    """Tested with orange.pl"""

    def setup(self,
              login=None,
              password=None,
              service_url="/portal/map/map/message_box",
              login_url="http://www.orange.pl/zaloguj.phtml"):

        self.SERVICE_URL = service_url
        self.LOGIN_URL = login_url
        self.MY_PHONE_NUMBER = login
        self.MY_PASSWORD = password

        web.agent(self.MY_HTTP_AGENT)
        web.go(self.LOGIN_URL)
        web.code(200)
        web.formvalue("loginForm", "login", self.MY_PHONE_NUMBER)
        web.formvalue("loginForm", "password", self.MY_PASSWORD)
        web.submit()
        web.code(200)
        web.find(self.SERVICE_URL)

    def send(self, msg, *send_to):
        for contact in send_to:
            web.follow(self.SERVICE_URL)
            web.follow("newsms")
            web.formvalue("sendSMS", "smsBody", msg)
            to = getattr(contact, 'mobile', contact)
            web.formvalue("sendSMS", "smsTo", to)
            web.submit()
            web.code(200)
            web.find("newsms")

    def close(self, error_info=None):
        web.formvalue("logoutForm", "_dyncharset", None)
        web.save_html()
        web.submit()
        web.code(200)
        web.find("zaloguj")


class VodafoneGate(AbstractSMSGate):
    """Tested with vodafone.ie"""

    def setup(self,
              login=None,
              password=None,
              service_url="/myv/messaging/webtext/",
              login_url="https://www.vodafone.ie/myv/services/login/index.jsp",
              logout_url="/myv/services/logout/Logout.shtml"):

        self.SERVICE_URL = service_url
        self.LOGIN_URL = login_url
        self.LOGOUT_URL = logout_url
        self.MY_PHONE_NUMBER = login
        self.MY_PASSWORD = password

        web.agent(self.MY_HTTP_AGENT)
        web.go(self.LOGIN_URL)
        web.code(200)
        web.formvalue("Login", "username", self.MY_PHONE_NUMBER)
        web.formvalue("Login", "password", self.MY_PASSWORD)
        web.submit()
        web.code(200)
        web.notfind("check your details")
        web.find(self.SERVICE_URL)

    def send(self, msg, *send_to):
        """
        @todo: make use of native vodafone multi-recipients functionality
        """
        for contact in send_to:
            web.follow(self.SERVICE_URL)

            try:
                web.find('/myv/messaging/webtext/Challenge.shtml')
            except twill.errors.TwillAssertionError, e:
                pass
            else:
                web.go('/myv/messaging/webtext/Challenge.shtml')
                with tempfile.NamedTemporaryFile(suffix=".jpeg") as captcha:
                    web.save_html(captcha.name)
                    web.back()
                    os.system("open %s " % captcha.name)
                    web.formvalue("WebText", "jcaptcha_response",
                                  raw_input("Captcha: "))

            web.formvalue("WebText", "message", msg)
            to = getattr(contact, 'mobile', contact)
            web.formvalue("WebText", "recipient_0", to)

            web.sleep(2)
            web.submit()
            web.code(200)
            web.find("Message sent!")

    def close(self, error_info=None):
        web.follow(self.LOGOUT_URL)
        web.code(200)
        web.find("Sign in to")


class TwilioGate(AbstractSMSGate):
    """Twilio messaging from cloud http://www.twilio.com"""

    def setup(self, sender=None, login=None, password=None):
        from twilio.rest import TwilioRestClient

        self.SENDER = sender
        self.ACCOUNT = login
        self.TOKEN = password
        self.client = TwilioRestClient(self.ACCOUNT, self.TOKEN)

    def send(self, msg, *send_to):
        for contact in send_to:
            to = getattr(contact, 'mobile', contact)
            self.client.sms.messages.create(to=to, from_=self.SENDER, body=msg)

    def close(self, error_info=None):
        pass
