from smsgates import BaseFactory
from smsgates import AbstractSMSGate
import twill.commands as web


class GateFactory(BaseFactory):
    @property
    def _choices(self):
        return {
            'vodafone.ie': VodafoneGate,
            'orange.pl': OrangeGate}

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
            web.formvalue("sendSMS", "smsTo", contact.mobile)
            web.submit()
            web.code(200)
            web.find("newsms")

    def close(self, error_info=None):
        web.formvalue("logoutForm", "_dyncharset", None)
        web.submit()
        web.code(200)
        web.find("zaloguj")

    def __str__(self):
        return "orange.pl"


class VodafoneGate(AbstractSMSGate):
    """Tested with vodafone.ie"""

    def setup(self,
              login=None,
              password=None,
              service_url="/myv/messaging/webtext/index.jsp",
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
        for contact in send_to:
            web.follow(self.SERVICE_URL)
            web.formvalue("WebText", "message", msg)
            to = getattr(contact, 'mobile', contact)
            web.formvalue("WebText", "recipient_0", to)
            web.sleep(3)
            web.submit()
            web.code(200)
            web.find("Message sent!")

    def close(self, error_info=None):
        web.follow(self.LOGOUT_URL)
        web.code(200)
        web.find("Sign in to")
        return False if error_info else True
