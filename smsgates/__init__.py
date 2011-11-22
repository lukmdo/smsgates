from collections import namedtuple
import twill.commands as web

__all__ = ['get_gate_class', 'Abstract_SMS_Gate',
           'Vodafone_Gate', 'Orange_Gate']


def get_gate_class(name):
    gate_imp_class = {
        'vodafone.ie':  Vodafone_Gate,
        'orange.pl':  Orange_Gate}
    return gate_imp_class[name.lower()]


class _LogSilencer(object):
    def write(self, msg):
        pass


class Abstract_SMS_Gate(object):
    """Abstract class for SMS gate

    Implements those public template methods that drive its behaviour.
    It is supposed to be used using the ``with`` statement:

        with MySMSGate() as gate:
            gate.send(some_text)
    """
    MY_HTTP_AGENT = "Mozilla/5.0"

    def __init__(self, verbose=False, **kwargs):
        if not verbose:
            from twill import browser
            browser.OUT = _LogSilencer()
        self.setup(**kwargs)

    def setup(self, *args, **kwargs):
        """
        :return: object ready to fire ``send``
        """
        return self

    def send(self, msg, to):
        raise NotImplementedError("Must be implemented by it subclass")

    def close(self, error_info=None):
        return True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """
        This method is supposed to:
        - handle the exceptions risen authentication or ``send``
        - make any finalization/logout

        :return: Boolean to indicate success default True
        """

        if type:
            ErrorInfo = namedtuple('ErrorInfo', 'type value traceback')
            error_info = ErrorInfo(type, value, traceback)
            val = self.close(error_info)
        else:
            val = self.close()

        return val if val is not None else True


class Orange_Gate(Abstract_SMS_Gate):
    """tested with orange.pl"""

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

    def send(self, msg, to):
        web.follow(self.SERVICE_URL)
        web.follow("newsms")
        web.formvalue("sendSMS", "smsBody", msg)
        web.formvalue("sendSMS", "smsTo", to)
        web.submit()
        web.code(200)
        web.find("newsms")

    def close(self, error_info=None):
        web.formvalue("logoutForm", "_dyncharset", None)
        web.submit()
        web.code(200)
        web.find("zaloguj")


class Vodafone_Gate(Abstract_SMS_Gate):
    """tested with vodafone.ie"""

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

    def send(self, msg, to):
        """
        @todo: add support for chunking the message
        @todo: add support for multiple recipients
        """
        web.follow(self.SERVICE_URL)
        web.formvalue("WebText", "message", msg)
        web.formvalue("WebText", "recipient_0", to)
        web.sleep(0.5)
        web.submit()
        web.code(200)
        web.find("Message sent!")

    def close(self, error_info=None):
        web.follow(self.LOGOUT_URL)
        web.code(200)
        web.find("Sign in to")
